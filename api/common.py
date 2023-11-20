from utils.sqlHelper import PostgresConnectionContextManager


def getProjectUsedPlugins(project_id: int) -> list:
    with PostgresConnectionContextManager() as cur:
        cur.execute("SELECT plugin_used FROM project WHERE id=%s", (project_id,))
        rows = cur.fetchall()
        res = rows[0][0]
    plugin_names = []
    if not res:
        return []
    for _ in res:
        plugin_names.append(_)
    return plugin_names


def sqlInjectCheck(string: str):
    if string.find('\'') != -1:
        return False
    if string.find('\"') != -1:
        return False
    if string.find('\\') != -1:
        return False
    if string.find(')') != -1:
        return False
    if string.find('(') != -1:
        return False
    if string.find('#') != -1:
        return False
    if string.find('-') != -1:
        return False
    return True
