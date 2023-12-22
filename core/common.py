# 部分功能的数据库操作函数
from utils.sqlHelper import PostgresConnectionContextManager


def submitOneRowDB(pluginName, asset_id, columnName, cellJson):
    with PostgresConnectionContextManager() as db_cursor:
        # 检查存不存在对应的行，有则更新，没有则添加
        # inject vul
        db_cursor.execute(
            "SELECT * FROM " +
            pluginName +
            '_table' +
            " WHERE asset_id = %s",
            (asset_id,
             ))
        a = db_cursor.fetchone()
        if a:
            db_cursor.execute(
                "UPDATE " +
                pluginName +
                '_table' +
                " SET " +
                columnName +
                " = %s WHERE asset_id = %s",
                (cellJson,
                 asset_id))
        else:
            db_cursor.execute(
                "INSERT INTO " +
                pluginName +
                '_table' +
                " (asset_id," +
                columnName +
                ") VALUES (%s,%s)", (asset_id, cellJson))


def submitRowColorDB(asset_original, color):
    with PostgresConnectionContextManager() as db_cursor:
        db_cursor.execute(
            "UPDATE asset SET row_color = %s WHERE asset_name = %s",
            (color,
             asset_original))


def getAllColumnDB(pluginName):
    with PostgresConnectionContextManager() as db_cursor:
        db_cursor.execute(
            "SELECT row_to_json(t) FROM (SELECT * FROM column_attribute WHERE plugin_name=%s) as t",
            (pluginName,))
        a = db_cursor.fetchall()
    return a


def getAllColumnNameDB(pluginName):
    with PostgresConnectionContextManager() as db_cursor:
        db_cursor.execute(
            "SELECT row_to_json(t) FROM (SELECT name FROM column_attribute WHERE plugin_name=%s) as t",
            (pluginName,))
        a = db_cursor.fetchall()
    return a


def getColumnDB(pluginName, columnName):
    with PostgresConnectionContextManager() as db_cursor:
        db_cursor.execute(
            "SELECT row_to_json(t) FROM (SELECT * FROM column_attribute WHERE plugin_name=%s AND name=%s) as t",
            (pluginName, columnName,))
        a = db_cursor.fetchone()
    return a


def initColumnValueDB(pluginName, asset_id, columnName):
    with PostgresConnectionContextManager() as db_cursor:
        # inject vul
        db_cursor.execute(
            "SELECT " +
            columnName +
            " FROM " +
            pluginName +
            '_table' +
            " WHERE asset_id = %s",
            (asset_id,
             ))
        a = db_cursor.fetchone()  # (,None),None查不到和查出来什么都没有是不一样的
    return a


def is_basic_type(obj):
    basic_types = [int, bool, float, str, list, dict, tuple]
    return type(obj) in basic_types


def idToAsset(id: int):
    pass
