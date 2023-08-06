from singer import metadata

from macrometa_source_snowflake.connection import SnowflakeConnection
import singer
import macrometa_source_snowflake.sync_strategies.common as common

LOGGER = singer.get_logger('macrometa_source_snowflake')


# pylint: disable=invalid-name,missing-function-docstring,too-many-locals,duplicate-code
def fetch_view(conn_config, catalog_entry, columns):
    samples = []
    snowflake_conn = SnowflakeConnection(conn_config)
    with snowflake_conn.connect_with_backoff() as open_conn:
        with open_conn.cursor() as cur:
            select_sql = common.generate_select_sql(catalog_entry, columns)
            cur.execute(select_sql)
            count = 0
            for rec in cur:
                rec_msg = common.row_to_singer_record(catalog_entry, None, rec, columns, None)
                samples.append(rec_msg.record)
                count += 1
                if count >= 10:
                    break
    return samples

# pylint: disable=too-many-statements,duplicate-code
def fetch_table(conn_config, catalog_entry, columns):
    samples = []
    snowflake_conn = SnowflakeConnection(conn_config)
    with snowflake_conn.connect_with_backoff() as open_conn:
        with open_conn.cursor() as cur:
            select_sql = common.generate_select_sql(catalog_entry, columns)
            LOGGER.info('DEBUG SAMPLE 10: %s', str(catalog_entry))
            select_sql += " LIMIT 10"
            LOGGER.info('DEBUG SAMPLE 11: %s', select_sql)
            cur.execute(select_sql)
            for rec in cur:
                rec_msg = common.row_to_singer_record(catalog_entry, None, rec, columns, None)
                LOGGER.info('DEBUG SAMPLE 12: %s', rec_msg.record)
                samples.append(rec_msg.record)
    LOGGER.info('DEBUG SAMPLE 13: %s', samples)
    return samples

def fetch_samples(conn_config, catalog_entry):
    """
    Fetch samples for the stream.
    """
    md_map = metadata.to_map(catalog_entry.metadata)
    conn_config['dbname'] = md_map.get(()).get('database-name')
    LOGGER.info('DEBUG SAMPLE 131: %s', conn_config)
    columns = [c for c in catalog_entry.schema.properties.keys() if common.property_is_selected(catalog_entry, c)]
    LOGGER.info('DEBUG SAMPLE 141: %s', columns)
    columns.sort() 
    LOGGER.info('DEBUG SAMPLE 151: %s', columns)
    if len(columns) == 0:
        # There are no columns selected for stream. So, skipping it.
        return []
    if md_map.get((), {}).get('is-view'):
        LOGGER.info('DEBUG SAMPLE 14')
        state = fetch_view(conn_config, catalog_entry, columns)
        LOGGER.info('DEBUG SAMPLE 15: %s', str(state))
    else:
        LOGGER.info('DEBUG SAMPLE 16')
        state = fetch_table(conn_config, catalog_entry, columns)
        LOGGER.info('DEBUG SAMPLE 17: %s', str(state))
    # Appending _ to keys for preserving values of reserved keys in source data
    reserved_keys = ['_key', '_id', '_rev']
    if md_map.get((), {}).get('table-key-properties'):
        key_properties = md_map.get((), {}).get('table-key-properties')
        if key_properties[0] == '_key':
                reserved_keys.remove('_key')
    if any(key in set(columns) for key in reserved_keys):
        for record in state:
            record = modify_reserved_keys(record, reserved_keys)
    return state

def modify_reserved_keys(record, reserved_keys):
    for reserved_key in reserved_keys:
        if record.get(reserved_key):
            new_key = "_" + reserved_key
            while True:
                if record.get(new_key):
                    new_key = "_" + new_key
                else:
                    break
            record[new_key] = record.pop(reserved_key)
    return record