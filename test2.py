
from utils.sqlHelper import PostgresConnectionContextManager


if __name__ == '__main__':
    # importPlugins()
    # a = Plugin_Goby_old(["10.1.72.121"], {})
    # a.onLoad()
    # a.runAll()
    def getProjectUsedPlugins(project_id):
        with PostgresConnectionContextManager() as cur:
            cur.execute("SELECT plugin_used FROM project WHERE id=%s", (project_id,))
            rows = cur.fetchall()
            print(rows)
            res = rows[0][0]
        plugin_names = []
        if not res:
            return []
        for _ in res:
            plugin_names.append(_)
        return plugin_names


    sortkey = 'asset_original'
    page_number = 1
    page_size = 10
    sort_order = 'asc'
    plugins = getProjectUsedPlugins(10)
    plugin_table = ["plugin_goby_table", "plugin_test_table"]
    table_columns = {
        "plugin_goby_table": ["vul", "tag","port"],
        "plugin_test_table": ["c1", "c2"]
    }
    query = f"""
    SELECT
        %s
    FROM
        %s
    %s
    JOIN
        asset a
    ON
        %s.asset_original = a.asset_original
    WHERE
        %s = ANY(a.tag_ids)
        AND a.project_id=%s
    ORDER BY
        %s.%s %s
    LIMIT
        %s
    OFFSET
        %s;
    """

    print(query)
    with PostgresConnectionContextManager() as cur:
        cur.execute(query, (' , '.join(select_clauses),
                            SELECT_FROM,
                            joins
                            , SELECT_FROM,
                            data.tag_id,
                            data.project_id,
                            SELECT_FROM, sortkey, sort_order,
                            page_size
                            , (page_number - 1) * page_size))
        rows = cur.fetchall()
    print(rows)
    # 构建 SELECT 子句
    # select_clauses = [f"{plugin_table[0]}.asset_original"]  # 首先选择第一个表的 asset_original
    # for table in plugin_table:
    #     select_clauses.extend([f"{table}.{col}" for col in table_columns[table]])
    #
    # # 构建 JOIN 子句
    # joins = " JOIN ".join([f"{table} ON {plugin_table[0]}.asset_original = {table}.asset_original" for table in plugin_table[1:]])
    # if len(plugin_table) > 1:
    #     joins = "JOIN " + joins
    # # 完整的查询语句
    # query = f"""
    # SELECT
    #     {' , '.join(select_clauses)}
    # FROM
    #     {plugin_table[0]}
    # {joins}
    # JOIN
    #     asset a
    # ON
    #     {plugin_table[0]}.asset_original = a.asset_original
    # WHERE
    #     12 = ANY(a.tag_ids)
    #     AND a.project_id=10
    # ORDER BY
    #     {plugin_table[0]}.asset_original asc
    # LIMIT
    #     10
    # OFFSET
    #     0;
    # """
    #
    # print(query)