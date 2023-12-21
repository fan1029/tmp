from ..service import service_blue
from dataclasses import dataclass, field
from quart_schema import validate_request, validate_response
from utils.redis_manager import RedisMixin,AioRedisManager
import psutil
from quart import websocket
import asyncio
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


def getSystemInfo():
    '''获取CPU使用率，内存使用率，返回整数'''

    # 获取当前系统CPU利用率
    cpu = psutil.cpu_percent(None)
    mem = psutil.virtual_memory().percent
    return {"status": 200, "data": {"cpu": cpu, "mem": mem},"from": "getSystemInfo"}


async def getRunningTaskCount():
    '''获取正在运行的任务数量'''
    # 获取pluginTaskProgress哈希表中的所有value，每个value中为一个列表，列表中为任务msgId@插件名。
    # 获取assetRunning(LIST)的所有value，每个value为一个msgId。遍历assetRunning列表，如果value在pluginTaskProgress中的value中，则为正在运行的任务计算总数量
    # redisClient = RedisMixin().redis_db_service
    redisClient = AioRedisManager().get_redis()
    runningTaskCount = 0
    pluginTaskProgress = await redisClient.hvals('pluginTaskProgress')
    pluginTaskProgress = [json.loads(i) for i in pluginTaskProgress]
    assetRunning = await redisClient.lrange('assetRunning', 0, -1)
    # print(assetRunning)
    # print(pluginTaskProgress)
    for _ in assetRunning:
        for i in pluginTaskProgress:
            if _ in i[0]:
                runningTaskCount += 1
    return runningTaskCount


def getOperateLog():
    '''
    获取Log库中的日志
    :return:
    '''
    with PostgresConnectionContextManager() as cur:
        cur.execute('SELECT * FROM log ORDER BY id DESC LIMIT 30')
        operateLog = cur.fetchall()
    return operateLog


async def getAllTaskCount():
    '''获取所有任务数量'''
    redisClient = AioRedisManager().get_redis()
    # 获取pluginTaskProgress哈希表中的个数
    return await redisClient.hlen('pluginTaskProgress')


def getAssetCount(projectId):
    '''获取资产数量'''
    with PostgresConnectionContextManager() as cur:
        cur.execute('SELECT COUNT(*) FROM asset WHERE project_id = %s', (projectId,))
        assetCount = cur.fetchall()
    return assetCount[0][0]


async def getTaskCount(projectId: int):
    '''获取任务数量'''
    runningTaskCount = await getRunningTaskCount()
    allTaskCount = await getAllTaskCount()
    if projectId == -1:
        allAsset = 0
    else:
        allAsset = getAssetCount(projectId)
    return {"status": 200,
            "data": {"runningTaskCount": runningTaskCount, "allTaskCount": allTaskCount, "allAsset": allAsset},
            "from": "getTaskCount"}


async def getServiceStatus():
    '''获取服务状态'''
    redisClient = AioRedisManager().get_redis()
    # 获取'plugin-center'哈希表中的所有value
    serviceList = await redisClient.hvals('plugin-center')
    # 将json字符串转化为python对象
    serviceList = [json.loads(i) for i in serviceList]
    for _ in serviceList:
        _['consumer_name'] = _['consumer_identification'].split('-')[0] + '-' + _['consumer_identification'].split('-')[
            1]
    return {'status': 200, 'data': serviceList, 'from': "getServiceStatus"}


@service_blue.websocket('/menuIndexInfo')
async def menuIndexInfo():
    while True:
        receiveCommand = await websocket.receive()
        tmpJson = json.loads(receiveCommand)
        if tmpJson['command'] == 'getSystemInfo':
            await websocket.send(json.dumps(getSystemInfo()))
        elif tmpJson['command'] == 'getOperateLog':
            await websocket.send(json.dumps(getOperateLog()))
        elif tmpJson['command'] == 'getTaskCount':
            await websocket.send(json.dumps(await getTaskCount(tmpJson['projectId'])))
        elif tmpJson['command'] == 'getServiceStatus':
            await websocket.send(json.dumps(await getServiceStatus()))
        else:
            await websocket.send('error')
