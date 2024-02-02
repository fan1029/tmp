from utils.sqlHelper import PostgresConnectionContextManager
from core.pluginManager import PluginManager




if __name__ == '__main__':

    data={}
    data['current_table'] = ['plugin_goby_table']
    base_query = "SELECT row_to_json(t) FROM(SELECT asset.*,{table_columns} FROM asset {joins} "
    joins = []
    table_columns = []
    for table in data['current_table']:
        joins.append(f"LEFT JOIN {table} ON asset.id = {table}.asset_id")
        table_columns.append(f"{table}.*")

    joins_str = ' '.join(joins)
    table_columns_str = ', '.join(table_columns)
    query = base_query.format(table_columns=table_columns_str, joins=joins_str)
    sort = "desc"
    size = 10
    offset = 0
    project_id = 26
    tag_id = 31
    query += f"WHERE asset.project_id = {project_id} AND {tag_id} = ANY(asset.tag_ids) ORDER BY asset.id {sort} LIMIT {size} OFFSET {offset})t"
    column = []
    rows = []
    with PostgresConnectionContextManager() as cur:
        #获取column_attribute表
        cur.execute("SELECT row_to_json(t) FROM (SELECT * FROM column_attribute)t ")
        columnRes = cur.fetchall()
        for _ in columnRes:
            column.append(_[0])
        cur.execute(query)
        rowsTmp = cur.fetchall()
        if rowsTmp:
            for _ in rowsTmp:
                rows.append(_[0])
        cur.execute
