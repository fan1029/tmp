from utils.redis_manager import RedisMixin
from nb_log import LoggerMixin
import json
from core.asset import Asset
from typing import List, Union
import time
import uuid


class Service(RedisMixin, LoggerMixin):

    def __init__(self, pluginName):
        self.pluginName = pluginName
        self.taskQueueName = pluginName + '-task'
        self.resultQueueName = pluginName + '-result'
        self.pluginServices = []
        self.initServices()

    def initServices(self):
        allServices = self.getAllService()
        for _ in allServices:
            if self.pluginName in _:
                self.pluginServices.append(_)

    def _getServiceInfo(self, serviceName) -> dict:
        tmp = self.redis_db_service.hget('plugin-center', serviceName)
        if not tmp:
            return {}
        return json.loads(tmp)

    def getAllService(self):
        allServices = self.redis_db_service.hkeys('plugin-center')
        return allServices

    def stopService(self, serviceName: str):

        serviceInfo = self._getServiceInfo(serviceName)
        if not serviceInfo:
            return False
        serviceInfo['stopFlag'] = True
        self.redis_db_service.hset('plugin-center', serviceName, json.dumps(serviceInfo))
        return True

    def continueService(self, serviceName):
        serviceInfo = self._getServiceInfo(serviceName)
        if serviceInfo:
            serviceInfo['stopFlag'] = False
            self.redis_db_service.hset('plugin-center', serviceName, json.dumps(serviceInfo))
        else:
            return False

    @staticmethod
    def getTaskCount(serviceName):
        '''
        获取任务队列中的任务数量
        :param serviceName:
        :return:
        '''
        return RedisMixin().redis_db_service.xlen(serviceName + '-task')

    @staticmethod
    def getTasks(serviceName):
        '''
        获取任务队列中的任务
        :param serviceName:
        :return:
        '''
        return RedisMixin().redis_db_service.xrange(serviceName + '-task')

    def addProgress(self, assetId, msgId):
        tmp = self.redis_db_service.hget('pluginTaskProgress', assetId)
        if tmp:
            tmp = json.loads(tmp)
            tmp.append(str(msgId) + '@' + self.pluginName)
            self.redis_db_service.hset('pluginTaskProgress', assetId, json.dumps(tmp))
        else:
            self.redis_db_service.hset('pluginTaskProgress', assetId, json.dumps([str(msgId) + '@' + self.pluginName]))
        pass

    def delProgress(self, assetId, msgId):
        tmp = self.redis_db_service.hget('pluginTaskProgress', assetId)
        if tmp:
            tmp = json.loads(tmp)
            try:
                tmp.remove(str(msgId) + '@' + self.pluginName)
            except:
                return False
            if tmp:
                self.redis_db_service.hset('pluginTaskProgress', assetId, json.dumps(tmp))
            else:
                self.redis_db_service.hdel('pluginTaskProgress', assetId)
        else:
            return False

    def delProgressByMsgId(self, msgId):
        '''
        通过msgId删除进度
        :param msgId:
        :return:
        '''
        tmp = self.redis_db_service.hgetall('pluginTaskProgress')
        for _ in tmp:
            if msgId in json.loads(tmp[_]):
                self.delProgress(_, msgId)

    def addTask(self, asset: Union[dict, List[dict]], config=None):
        if config is None:
            config = {}
        AssetsList = []
        SendList = []
        if isinstance(asset, list):
            AssetsList = asset
        else:
            AssetsList.append(asset)
        for _ in AssetsList:
            SendList.append(_['target'])

        msgId = self.redis_db_service.xadd(self.taskQueueName,
                                           {"targets": json.dumps(SendList), "publishTime": str(int(time.time())),
                                            "config": json.dumps(config)})
        for _ in AssetsList:
            self.addProgress(_['assetId'], msgId)  # 显示进度用的
        return msgId

    def delTask(self, msgId):
        '''
        加上检测是否被拿去消费了
        :param msgId:
        :return:
        '''
        # 检测stream任务是否被取走，没有被取走则删除
        self.redis_db_service.xdel(self.taskQueueName, msgId)

    def setMaxThread(self, serviceName, threadNum: int):
        '''
        设置最大线程
        :param threadNum:
        :return:
        '''
        serviceInfo = self._getServiceInfo(serviceName)
        serviceInfo['maxThread'] = threadNum
        self.redis_db_service.hset('plugin-center', self.pluginName, json.dumps(serviceInfo))
        return True


class ServiceMixIn():

    def getService(self, pluginName):
        return Service(pluginName)


if __name__ == '__main__':
    a = RedisMixin().redis_db_service.hkeys('plugin-center')
    print(a)
