from ..service import service_blue
from dataclasses import dataclass, field
from quart_schema import validate_request, validate_response
from utils.redis_manager import RedisMixin
from utils.sqlHelper import PostgresConnectionContextManager
from core.pluginManager import PluginManager
import json


@service_blue.get('/getServiceSatatus')
async def getServiceSatatus():
    redisClient = RedisMixin().redis_db_service
    # 获取'plugin-center'哈希表中的所有value
    serviceList = redisClient.hvals('plugin-center')
    # 将json字符串转化为python对象
    serviceList = [json.loads(i) for i in serviceList]
    for _ in serviceList:
        _['consumer_name'] = _['consumer_identification'].split('-')[0] + '-' + _['consumer_identification'].split('-')[
            1]
    return {'status': 200, 'data': serviceList}


@dataclass
class changeServiceStatusRequest:
    consumerName: str
    status: str = ''
    maxThread: int = -1


@dataclass
class changeServiceStatusResponse:
    status: int
    msg: str


@service_blue.post('/changeServiceStatus')
@validate_request(changeServiceStatusRequest)
async def changeServiceStatus(data: changeServiceStatusRequest):
    redisClient = RedisMixin().redis_db_service
    serviceList = redisClient.hget('plugin-center', data.consumerName + '-info')
    serviceInfo = json.loads(serviceList)
    if data.status:
        serviceInfo['status'] = data.status
    if data.maxThread != -1:
        serviceInfo['maxThread'] = data.maxThread
    redisClient.hset('plugin-center', data.consumerName + '-info', json.dumps(serviceInfo))
    return changeServiceStatusResponse(200, '修改成功')


@dataclass
class runPluginRequest:
    tagId: int
    pluginName: str
    assetId: int
    config: dict


@service_blue.post('/runPlugin')
@validate_request(runPluginRequest)
async def runPlugin(data: runPluginRequest):
    pluginManager = PluginManager()
    pluginObj = pluginManager.getPlugin(data.pluginName)
    if not pluginObj:
        return {'status': 400, 'msg': '插件不存在'}
    if data.assetId == -1:
        return {'status': 400, 'msg': '请选择资产'}
    elif data.assetId == -2:
        # 根据tagId获取资产
        with PostgresConnectionContextManager() as cur:
            cur.execute('SELECT id from asset WHERE %s = ANY (tag_ids)', (data.tagId,))
            assetList = cur.fetchall()
            ids = [i[0] for i in assetList]
    else:
        ids = [data.assetId]
    pluginObj().run(ids, data.config)
    return {'status': 200, 'msg': '任务已提交'}


@dataclass
class getPluginInfoRequest:
    pluginName: str


@dataclass
class getPluginInfoResponseData:
    pluginName: str
    description: str
    scanTargetType: list
    columnDict: dict
    author: str
    version: str


@dataclass
class getPluginInfoResponse:
    status: int
    data: getPluginInfoResponseData


@service_blue.post('/getPluginInfo')
@validate_request(getPluginInfoRequest)
async def getPluginInfo(data: getPluginInfoRequest):
    pluginManager = PluginManager()
    pluginObj = pluginManager.getPlugin(data.pluginName)
    if not pluginObj:
        return {'status': 400, 'msg': '插件不存在'}
    # pluginObj = pluginObj()
    return getPluginInfoResponse(200, getPluginInfoResponseData(pluginObj.pluginName, pluginObj.description,
                                                                pluginObj.scanTargetType, pluginObj.columnDict,
                                                                pluginObj.author, pluginObj.version))
