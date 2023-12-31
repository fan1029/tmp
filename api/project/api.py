import copy

from ..project import project_blue
from dataclasses import dataclass,field
from utils.sqlHelper import PostgresConnectionContextManager
from quart_schema import validate_request, validate_response
import datetime
from typing import List
import traceback
from core.pluginManager import PluginManager
from urllib.parse import urlparse


@dataclass
class GetProjectListRequest:
    pass


@dataclass
class Project:
    id: int
    name: str
    description: str
    create_time: datetime.datetime
    tags: None
    plugin_used:list

@dataclass
class GetProjectListResponse:
    status: int
    data: List[Project]


@project_blue.route('/getProjectList')
async def getProjectList():
    query = "SELECT row_to_json(project) FROM project"
    with PostgresConnectionContextManager() as cur:
        cur.execute(query)
        rows = cur.fetchall()
    projectList = []
    for i in rows:
        projectList.append(Project(**i[0]))
    return GetProjectListResponse(200, projectList)



@dataclass
class GetProjectInfoRequest:
    id: int


@dataclass
class GetProjectInfoResponse:
    id: int
    name: str
    description: str
    create_time: datetime.datetime
    tags: None
    plugin_used: list


@project_blue.post('/getProjectInfo')
@validate_request(GetProjectInfoRequest)
async def getProjectInfo(data: GetProjectInfoRequest):
    query = "SELECT row_to_json(project) FROM project WHERE id=%s"
    with PostgresConnectionContextManager() as cur:
        cur.execute(query, (data.id,))
        rows = cur.fetchone()
        print(rows)
        return GetProjectInfoResponse(**rows[0])


@dataclass
class CreateProjectRequest:
    name: str
    description: str
    assets: List[str]
    createUser: str = field(default='admin')


@dataclass
class CreateProjectResponse():
    status: bool
    msg: str
    create_time: str
    project_id:int



def filter_url(url):
    try:
        if "://" not in url:
            url = "http://" + url
        result = urlparse(url)
        hostname = result.hostname
        if ":" in hostname:
            hostname = hostname.split(":")[0]
        return hostname
    except Exception as e:
        print(f"An error occurred: {e}")
        return None



def filterAsset(assetList: List[str]):
    '''
    过滤资产，去除重复资产，将所有资产转为domain或ip
    :param assetList:
    :return:
    '''
    tmpList = []
    for _ in assetList:
        tmp = {"asset_name": '', "original_assets": [], "type": ''}
        find = 0
        filtered = filter_url(_)
        for _2 in tmpList:
            if filtered == _2["asset_name"]:
                _2["original_assets"].append(_)
                find = 1
                break
        if find == 0:
            tmp["asset_name"] = filtered
            tmp["original_assets"].append(_)
            #判断filtered是ip还是domain
            if filtered.replace('.','').isdigit():
                tmp["type"] = 'ip'
            else:
                tmp["type"] = 'domain'
            tmpList.append(copy.deepcopy(tmp))
    return tmpList






@project_blue.post('/createProject')
@validate_request(CreateProjectRequest)
async def createProject(data: CreateProjectRequest):
    # 检查是否存在同名项目
    try:
        query = "SELECT * FROM project WHERE name=%s"
        with PostgresConnectionContextManager() as cur:
            cur.execute(query, (data.name,))
            rows = cur.fetchone()
            if rows:
                return CreateProjectResponse(False,'存在同名项目', str(datetime.datetime.now()))
        # 创建项目
        query = "INSERT INTO project (name,description,create_time) VALUES (%s,%s,%s) RETURNING id"
        # query="INSERT INTO project (name,description,create_time) VALUES (%s,%s,%s)"
        with PostgresConnectionContextManager() as cur:
            cur.execute(query, (data.name, data.description, datetime.datetime.now()))
        #取刚刚insert数据的id，以name查询
        query = "SELECT id FROM project WHERE name=%s"
        with PostgresConnectionContextManager() as cur:
            cur.execute(query, (data.name,))
            rows = cur.fetchone()
            project_id = rows[0]
        #插入记录到taginfo表返回插入后的id
        query = "INSERT INTO taginfo (project_id,tag_name,create_time,description,create_user) VALUES (%s,%s,%s,%s,%s) RETURNING id"
        with PostgresConnectionContextManager() as cur:
            cur.execute(query, (project_id, '全部资产', datetime.datetime.now(), '本项目所有资产标签', data.createUser))
            rows = cur.fetchone()
            tag_id = rows[0]
        #插入assets，其中tag_ids为数组
        # query = "INSERT INTO asset (project_id,asset_name,tag_ids) VALUES (%s,%s,%s)"
        filteredAssetList = filterAsset(data.assets)
        query = "INSERT INTO asset (project_id,asset_name,tag_ids,original_assets,asset_type) VALUES (%s,%s,%s,%s,%s)"
        with PostgresConnectionContextManager() as cur:
            for _ in filteredAssetList:
                cur.execute(query, (project_id, _['asset_name'], [tag_id], _['original_assets'], _['type']))
    except Exception as e:
        print(traceback.format_exc())
        print(e)
        return CreateProjectResponse(False,'创建失败,发生未知错误', str(datetime.datetime.now()))
    return CreateProjectResponse(True,'创建成功', str(datetime.datetime.now()),project_id)


@dataclass
class DeleteProjectRequest:
    id: int


@dataclass
class DeleteProjectResponse:
    status: bool


@project_blue.post('/deleteProject')
@validate_request(DeleteProjectRequest)
async def deleteProject(data: DeleteProjectRequest):
    query = "DELETE FROM project WHERE id=%s"
    with PostgresConnectionContextManager() as cur:
        cur.execute(query, (data.id,))
    return DeleteProjectResponse(True)

@dataclass
class getProjectTagRequest:
    projectId: int

@dataclass
class TagInfo:
    id: int
    project_id: int
    tag_name: str
    create_time: datetime.datetime
    description: str
    create_user: str
    used_plugin: list

@dataclass
class getProjectTagResponse:
    status: bool
    msg:str
    data: List[TagInfo]




@project_blue.post('/getProjectTag')
@validate_request(getProjectTagRequest)
async def getProjectTag(data: getProjectTagRequest):
    query = "SELECT row_to_json(t) FROM (SELECT * FROM taginfo WHERE project_id=%s) as t"
    try:
        with PostgresConnectionContextManager() as cur:
            cur.execute(query, (data.projectId,))
            rows = cur.fetchall()
    except:
        return getProjectTagResponse(False,'数据请求失败', [])
    newRows = [_[0] for _ in rows]
    # print(newRows)
    return getProjectTagResponse(True,'success', newRows)


@dataclass
class getProjectHeaderRequest:
    projectId: int

@project_blue.post('getProjectHeader')
async def getProjectHeader(data: getProjectHeaderRequest):
    query = "SELECT plugin_used FROM project WHERE id=%s"
    with PostgresConnectionContextManager() as cur:
        cur.execute(query, (data.projectId,))
        rows = cur.fetchone()
        print(rows)
    if rows:
        plugin_array = rows[0]
        pm = PluginManager()
        tl = pm.getPluginTableList()
        for _ in tl:
            if _['plugin_name'] in plugin_array:
                return _['column']




