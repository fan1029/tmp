from ..project import project_blue
from dataclasses import dataclass
from utils.sqlHelper import PostgresConnectionContextManager
from quart_schema import  validate_request, validate_response
import datetime
import asyncpg
import json
import asyncio


@project_blue.route('/getProjectList')
async def getProjectList():

    pass

@dataclass
class GetProjectInfoRequest:
    id:int

@dataclass
class GetProjectInfoResponse:
    id:int
    name:str
    description:str
    create_time:datetime.datetime
    tags:list

@project_blue.post('/getProjectInfo')
@validate_request(GetProjectInfoRequest)
async def getProjectInfo(data:GetProjectInfoRequest):
    query = "SELECT row_to_json(project) FROM project WHERE id=%s"
    with PostgresConnectionContextManager() as cur:
        cur.execute(query,(data.id,))
        rows = cur.fetchone()
        print(rows)
        return GetProjectInfoResponse(**rows[0])


@dataclass
class CreateProjectRequest:
    name:str
    description:str

@dataclass
class CreateProjectResponse(CreateProjectRequest):
    status:bool
    create_time:str

@project_blue.post('/createProject')
@validate_request(CreateProjectRequest)
async def createProject(data:CreateProjectRequest):
    #检查是否存在同名项目
    query = "SELECT * FROM project WHERE name=%s"
    with PostgresConnectionContextManager() as cur:
        cur.execute(query,(data.name,))
        rows = cur.fetchone()
        if rows:
            return CreateProjectResponse(data.name,data.description,False,str(datetime.datetime.now()))
    #创建项目
    query = "INSERT INTO project (name,description,create_time) VALUES (%s,%s,%s) RETURNING id"
    # query="INSERT INTO project (name,description,create_time) VALUES (%s,%s,%s)"
    with PostgresConnectionContextManager() as cur:
        cur.execute(query,(data.name,data.description,datetime.datetime.now()))
    return CreateProjectResponse(data.name,data.description,True,str(datetime.datetime.now()))


@dataclass
class DeleteProjectRequest:
    id:int

@dataclass
class DeleteProjectResponse:
    status:bool


@project_blue.post('/deleteProject')
@validate_request(DeleteProjectRequest)
async def deleteProject(data:DeleteProjectRequest):
    query = "DELETE FROM project WHERE id=%s"
    with PostgresConnectionContextManager() as cur:
        cur.execute(query,(data.id,))
    return DeleteProjectResponse(True)