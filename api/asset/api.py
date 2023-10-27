from ..asset import asset_blue
from dataclasses import dataclass
from typing import List
from utils.sqlHelper import PostgresConnectionContextManager
from quart_schema import validate_request, validate_response
import datetime

@dataclass
class DeleteAssetRequest():
    original_name: str
    project_id: int
    tag_id: int

@dataclass
class DeleteAssetResponse():
    status: bool

@asset_blue.post('/deleteAsset')
@validate_request(DeleteAssetRequest)
@validate_response(DeleteAssetResponse)
async def deleteAsset(data: DeleteAssetRequest):
    #删除aset表中对于asset_original行的tag_ids字段中的对于的tag_id，tag_ids字段为数组类型
    query = "UPDATE asset SET tag_ids = array_remove(tag_ids,%s) WHERE project_id=%s AND asset_original=%s"
    with PostgresConnectionContextManager() as cur:
        cur.execute(query, (data.tag_id,data.project_id,data.original_name))
    return DeleteAssetResponse(True)


@dataclass
class AddAssetRequest():
    project_id: int
    tag_id: int
    asset: List[str]

@dataclass
class AddAssetResponse():
    status: bool

@asset_blue.post('/addAsset')
@validate_request(AddAssetRequest)
@validate_response(AddAssetResponse)
async def addAsset(data: AddAssetRequest):
    #向asset中添加新的记录，遍历asset中的元素为original_name，插入时将tag_id插入到tag_ids字段中
    #先检测是否有同project_id下存在asset_origianl存在即向其tag_ids中添加tag_id
    query = "SELECT * FROM asset WHERE project_id=%s AND asset_original=%s"
    with PostgresConnectionContextManager() as cur:
        for asset in data.asset:
            cur.execute(query, (data.project_id,asset))
            rows = cur.fetchone()
            if rows:
                query = "UPDATE asset SET tag_ids = array_append(tag_ids,%s) WHERE project_id=%s AND asset_original=%s"
                cur.execute(query, (data.tag_id,data.project_id,asset))
            else:
                query = "INSERT INTO asset (project_id,asset_original,tag_ids) VALUES (%s,%s,%s)"
                cur.execute(query, (data.project_id,asset,[data.tag_id]))
    return AddAssetResponse(True)