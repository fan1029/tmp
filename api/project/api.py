from ..project import project_blue
from dataclasses import dataclass,field
from utils.sqlHelper import PostgresConnectionContextManager
from quart_schema import validate_request, validate_response
import datetime
from typing import List
import asyncpg
import json
import asyncio


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
    tags: list


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
        query = "INSERT INTO asset (project_id,asset_original,tag_ids) VALUES (%s,%s,%s)"
        with PostgresConnectionContextManager() as cur:
            for asset in data.assets:
                cur.execute(query, (project_id, asset, [tag_id]))
    except:
        return CreateProjectResponse(False,'创建失败,发生未知错误', str(datetime.datetime.now()))
    return CreateProjectResponse(True,'创建成功', str(datetime.datetime.now()))


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
