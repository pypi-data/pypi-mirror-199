from singer import metadata

from macrometa_source_snowflake.connection import SnowflakeConnection

import macrometa_source_snowflake.sync_strategies.common as common


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
            select_sql += "LIMIT 10"
            cur.execute(select_sql)
            for rec in cur:
                rec_msg = common.row_to_singer_record(catalog_entry, None, rec, columns, None)
                samples.append(rec_msg.record)
    return samples

def fetch_samples(conn_config, catalog_entry):
    """
    Fetch samples for the stream.
    """
    md_map = metadata.to_map(catalog_entry.metadata)
    conn_config['dbname'] = md_map.get(()).get('database-name')
    columns = [c for c in catalog_entry.schema.properties.keys() if common.property_is_selected(md_map, c)]
    columns.sort()
    if len(columns) == 0:
        # There are no columns selected for stream. So, skipping it.
        return []
    if md_map.get((), {}).get('is-view'):
        state = fetch_view(conn_config, catalog_entry, columns)
    else:
        state = fetch_table(conn_config, catalog_entry, columns)
    return state
