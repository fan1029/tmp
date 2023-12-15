import time

import nb_log

from ..tags import tag_blue
from dataclasses import dataclass
from typing import List, Union
from utils.sqlHelper import PostgresConnectionContextManager
from quart_schema import validate_request, validate_response
import datetime
from ..common import getProjectUsedPlugins, sqlInjectCheck
from core.table import Table
from core.row import Row
from copy import deepcopy
from quart import websocket
import json


@dataclass
class GetTagListRequest():
    project_id: int


@dataclass
class TagList():
    tag_name: str
    project_id: int
    id: int
    description: str
    create_user: str
    create_time: str


@dataclass
class GetTagListResponse():
    project_id: int
    data: List[TagList]


@tag_blue.post('/getTagList')
@validate_request(GetTagListRequest)
@validate_response(GetTagListResponse)
async def getTagList(data: GetTagListRequest):
    query = "SELECT row_to_json(taginfo) FROM taginfo WHERE project_id=%s"
    with PostgresConnectionContextManager() as cur:
        cur.execute(query, (data.project_id,))
        rows = cur.fetchall()
    tmp = []
    for _ in rows:
        tmp.append(_[0])
    print(tmp)
    return GetTagListResponse(data.project_id, tmp)


@dataclass
class CreateTagRequest():
    project_id: int
    tag_name: str
    create_user: str
    description: str
    asset: List[str]


@dataclass
class CreateTagResponse():
    status: bool
    msg: str
    data: Union[CreateTagRequest, dict]


@tag_blue.post('/createTag')
@validate_request(CreateTagRequest)
async def createTag(data: CreateTagRequest):
    # 检测tag_name是否存在
    query = "SELECT id FROM taginfo WHERE project_id=%s AND tag_name=%s"
    with PostgresConnectionContextManager() as cur:
        cur.execute(query, (data.project_id, data.tag_name))
        rows = cur.fetchone()
        if rows:
            return CreateTagResponse(False, '重复命名', data=data)
    # 如果不存在则插入
    query = "INSERT INTO taginfo (project_id,tag_name,create_time,description,create_user) VALUES (%s,%s,%s,%s,%s) RETURNING id"
    with PostgresConnectionContextManager() as cur:
        cur.execute(query,
                    (data.project_id, data.tag_name, datetime.datetime.now(), data.description, data.create_user))
        rows = cur.fetchone()
        tag_id = rows[0]
        for asset in data.asset:
            # 判断asset存不存在表中
            cur.execute("SELECT id FROM asset WHERE asset_name=%s AND project_id =%s", (asset, data.project_id))
            rows = cur.fetchone()
            ##优化流程
            if rows:
                # 如果存在asset则使用update更新表中的tag_ids
                cur.execute("UPDATE asset SET tag_ids = tag_ids || %s WHERE asset_name = %s AND project_id=%s",
                            (tag_id, asset, data.project_id))
            else:
                # 如果不存在asset则使用insert插入表中
                cur.execute(
                    "INSERT INTO asset (asset_name,project_id,tag_ids) VALUES (%s,%s,%s)",
                    (asset, data.project_id, [tag_id]))
    return CreateTagResponse(True, '创建成功', data=data)


@dataclass
class DeleteTagRequest():
    project_id: int
    tag_id: int
    tag_name: str


@tag_blue.post('/deleteTag')
@validate_request(DeleteTagRequest)
async def deleteTag(data: DeleteTagRequest):
    # 删除tag
    query = "DELETE FROM taginfo WHERE id=%s and project_id=%s"
    with PostgresConnectionContextManager() as cur:
        cur.execute(query, (data.tag_id, data.project_id))
    # 删除asset中的tag_ids
    query = "UPDATE asset SET tag_ids = array_remove(tag_ids,%s) WHERE project_id=%s"
    with PostgresConnectionContextManager() as cur:
        cur.execute(query, (data.tag_id, data.project_id))
    return "ok"
    pass


@dataclass
class GetTagAssetListRequest():
    project_id: int
    tag_id: int


@dataclass
class Asset():
    id: int
    asset_original: str
    plugin_using: List[str]


@dataclass
class getTagAssetListResponse():
    project_id: int
    tag_id: int
    data: List[Asset]


@tag_blue.post('/getTagAssetList')
@validate_request(GetTagAssetListRequest)
async def getTagAssetList(data: GetTagAssetListRequest):
    with PostgresConnectionContextManager() as cur:
        cur.execute(
            "SELECT row_to_json(t) FROM (SELECT id,asset_name FROM asset WHERE project_id=%s AND tag_ids@>'{%s}') t; ",
            (data.project_id, data.tag_id)
        )
        rows = cur.fetchall()
        tmp = []
        for row in rows:
            tmp.append(row[0])
        return getTagAssetListResponse(data.project_id, data.tag_id, tmp)


@dataclass
class GetTagUsedPluginColumnsRequest():
    project_id: int
    tag_id: int


@dataclass
class PluginColumn():
    plugin_name: str
    column_config: dict


@dataclass
class GetTagUsedPluginColumnsResponse():
    status: bool
    project_id: int
    tag_id: int
    data: List[PluginColumn]


# #废除  删除used_plugin移到project表
# @tag_blue.post('/getTagUsedPluginColumns')
# @validate_request(GetTagUsedPluginColumnsRequest)
# async def getTagUsedPlugin(data: GetTagUsedPluginColumnsRequest):
#     with PostgresConnectionContextManager() as cur:
#         cur.execute("SELECT used_plugin FROM taginfo WHERE id=%s AND project_id=%s", (data.tag_id, data.project_id))
#         rows = cur.fetchall()
#         res = rows[0][0]
#     plugin_names = []
#     if not res:
#         return GetTagUsedPluginColumnsResponse(False, data.project_id, data.tag_id, [])
#     for _ in res:
#         plugin_names.append(_)
#     print(plugin_names)
#     columnsConfigList = []
#     for i2 in plugin_names:
#         print(i2)
#         with PostgresConnectionContextManager() as cur:
#             cur.execute("SELECT column_config from plugin where plugin_name= %s", (i2,))
#             rows = cur.fetchall()
#             rows[0][0]['plugin_name'] = i2
#             columnsConfigList.append(rows[0][0])
#
#     return GetTagUsedPluginColumnsResponse(True, data.project_id, data.tag_id, columnsConfigList)


@dataclass
class GetTagAssetDataRequest():
    project_id: int
    tag_id: int
    tag_name: str
    size: int
    page: int
    sortColumn: str
    sort: str
    current_table: List[str]


@dataclass
class GetTagAssetDataResponse():
    status: bool
    data: List[dict]
    msg: str
    info: dict


@tag_blue.post('/getAssetData')
@validate_request(GetTagAssetDataRequest)
async def getAssetData(data: GetTagAssetDataRequest):
    '''
    获取指定tag标签内的所有资产数据，支持翻页，size为每页的数量，page为页数,sort排序方式，asc为升序，desc为降序
    :return:
    '''
    if data.tag_id == -1:
        # 根据tag_name获取tag_id
        with PostgresConnectionContextManager() as cur:
            cur.execute("SELECT id FROM taginfo WHERE tag_name=%s AND project_id=%s", (data.tag_name, data.project_id))
            rows = cur.fetchone()
            data.tag_id = rows[0]
    a1 = sqlInjectCheck(data.sortColumn)
    a2 = sqlInjectCheck(data.sort)
    if not a1 or not a2:
        return GetTagAssetDataResponse(False, [], 'sql注入', data)
    plugin_table = []
    from core.pluginManager import PluginManager
    pm = PluginManager()
    tableInfoList = pm.getPluginTableList()
    tableListUsed = {}
    if not data.current_table:
        data.current_table = getProjectUsedPlugins(data.project_id)
    current_table = [_ + '_table' for _ in data.current_table]
    for _ in tableInfoList:
        tmp = _.popitem()
        if tmp[0] in current_table:
            plugin_table.append(tmp[0])
            tableListUsed[tmp[0]] = list(tmp[1].keys())
    nb_log.info(plugin_table)
    select_clauses = [f"{plugin_table[0]}.asset_original"]  # 首先选择第一个表的 asset_original
    for table in plugin_table:
        select_clauses.extend([f"{table}.{col}" for col in tableListUsed[table]])

    # 构建 JOIN 子句
    joins = " JOIN ".join(
        [f"{table} ON {plugin_table[0]}.asset_original = {table}.asset_original" for table in plugin_table[1:]])
    if len(plugin_table) > 1:
        joins = "JOIN " + joins
    # 完整的查询语句
    query = f"""
    SELECT row_to_json(t) FROM (
        SELECT
            {' , '.join(select_clauses)}
        FROM
            {plugin_table[0]}
        {joins}
        JOIN
            asset a
        ON
            {plugin_table[0]}.asset_original = a.asset_original
        WHERE
            %s = ANY(a.tag_ids)
            AND a.project_id=%s
        ORDER BY
            {plugin_table[0]}.{data.sortColumn} {data.sort}
        LIMIT
            %s
        OFFSET
            %s )t;
    """
    # nb_log.info(query)
    with PostgresConnectionContextManager() as cur:
        # 参数只包含数据值
        params = (data.tag_id, data.project_id, data.size, (data.page - 1) * data.size)
        cur.execute(query, params)
        rows = cur.fetchall()
    # if rows:
    #     rows = rows[0]
    resData = []
    for _ in rows:
        _ = _[0]
        tmp = {'asset_original': _['asset_original'], 'columnInfo': []}
        for k, v in _.items():
            if k != 'asset_original':
                v['column_name'] = k
                tmp['columnInfo'].append(v)
        resData.append(tmp)

    return GetTagAssetDataResponse(True, resData, 'ok', data)


@tag_blue.post('/getAssetData2')
@validate_request(GetTagAssetDataRequest)
async def getAssetData2(data: GetTagAssetDataRequest):
    '''
    获取指定tag标签内的所有资产数据，支持翻页，size为每页的数量，page为页数,sort排序方式，asc为升序，desc为降序
    :return:
    '''
    if data.tag_id == -1:
        # 根据tag_name获取tag_id
        with PostgresConnectionContextManager() as cur:
            cur.execute("SELECT id FROM taginfo WHERE tag_name=%s AND project_id=%s", (data.tag_name, data.project_id))
            rows = cur.fetchone()
            data.tag_id = rows[0]
    if data.tag_name == '':
        with PostgresConnectionContextManager() as cur:
            cur.execute("SELECT tag_name FROM taginfo WHERE id=%s AND project_id=%s", (data.tag_id, data.project_id))
            rows = cur.fetchone()
            data.tag_name = rows[0]
    a1 = sqlInjectCheck(data.sortColumn)
    a2 = sqlInjectCheck(data.sort)
    if not a1 or not a2:
        return GetTagAssetDataResponse(False, [], 'sql注入', data)
    from core.pluginManager import PluginManager
    pm = PluginManager()
    if not data.current_table:
        # data.current_table = getProjectUsedPlugins(data.project_id)
        data.current_table = ['plugin_goby']
    table = Table(data.current_table)
    query = f"""
    SELECT asset_name,id,original_assets FROM asset WHERE project_id = %s AND %s = ANY(tag_ids) ORDER BY asset.asset_name {data.sort} LIMIT %s OFFSET %s 
    """
    with PostgresConnectionContextManager() as cur:
        # 参数只包含数据值
        params = (data.project_id, data.tag_id, data.size, (data.page - 1) * data.size)
        cur.execute(query, params)
        rows = cur.fetchall()
    if rows:
        # print(rows)
        for _ in rows:
            row = Row(_[0], _[1], _[2], table.getColumnList())
            table.addRow(row)
    resData = table.generateTable()
    query = "SELECT count(id) FROM asset WHERE project_id = %s AND %s = ANY(tag_ids)"
    with PostgresConnectionContextManager() as cur:
        # 参数只包含数据值
        params = (data.project_id, data.tag_id)
        cur.execute(query, params)
        rows = cur.fetchone()
        total = rows[0]
    tmpdata = deepcopy(data.__dict__)
    tmpdata['total'] = total

    return GetTagAssetDataResponse(True, resData, 'ok', tmpdata)


async def getAssetDataFunc(data: GetTagAssetDataRequest):
    if data.tag_id == -1:
        # 根据tag_name获取tag_id
        with PostgresConnectionContextManager() as cur:
            cur.execute("SELECT id FROM taginfo WHERE tag_name=%s AND project_id=%s", (data.tag_name, data.project_id))
            rows = cur.fetchone()
            data.tag_id = rows[0]
    if data.tag_name == '':
        with PostgresConnectionContextManager() as cur:
            cur.execute("SELECT tag_name FROM taginfo WHERE id=%s AND project_id=%s", (data.tag_id, data.project_id))
            rows = cur.fetchone()
            data.tag_name = rows[0]
    a1 = sqlInjectCheck(data.sortColumn)
    a2 = sqlInjectCheck(data.sort)
    if not a1 or not a2:
        return GetTagAssetDataResponse(False, [], 'sql注入', data)
    from core.pluginManager import PluginManager
    pm = PluginManager()
    if not data.current_table:
        # data.current_table = getProjectUsedPlugins(data.project_id)
        data.current_table = ['plugin_goby']
    table = Table(data.current_table)
    query = f"""
    SELECT asset_name,id,original_assets FROM asset WHERE project_id = %s AND %s = ANY(tag_ids) ORDER BY asset.asset_name {data.sort} LIMIT %s OFFSET %s 
    """
    with PostgresConnectionContextManager() as cur:
        # 参数只包含数据值
        params = (data.project_id, data.tag_id, data.size, (data.page - 1) * data.size)
        cur.execute(query, params)
        rows = cur.fetchall()
    if rows:
        # print(rows)
        for _ in rows:
            row = Row(_[0], _[1], _[2], table.getColumnList())
            table.addRow(row)
    resData = table.generateTable()
    query = "SELECT count(id) FROM asset WHERE project_id = %s AND %s = ANY(tag_ids)"
    with PostgresConnectionContextManager() as cur:
        # 参数只包含数据值
        params = (data.project_id, data.tag_id)
        cur.execute(query, params)
        rows = cur.fetchone()
        total = rows[0]
    tmpdata = deepcopy(data.__dict__)
    tmpdata['total'] = total


    return (True, resData, 'ok', tmpdata)


@tag_blue.websocket('/syncTable')
async def syncTable():
    await websocket.send(json.dumps({"msg":"hello"}))
    while True:
        try:
            dataJson = await websocket.receive_json()
        except:
            await websocket.send('error')
            continue
        data = GetTagAssetDataRequest(project_id=dataJson['project_id'], tag_name=dataJson['tag_name'],
                                      tag_id=dataJson['tag_id'],
                                      size=dataJson['size'], page=dataJson['page'], sortColumn=dataJson['sortColumn'],
                                      sort=dataJson['sort'],
                                      current_table=dataJson['current_table'])
        tableData = await getAssetDataFunc(data)
        result =  {"status":tableData[0],"data":tableData[1],"msg":tableData[2],"info":tableData[3]}
        await websocket.send(json.dumps(result))

