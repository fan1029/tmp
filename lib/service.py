from utils.redis_manager import RedisMixin
from nb_log import LoggerMixin
import json
from typing import Union
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

    def addTask(self, url: Union[str, list]):
        urls = []
        if type(url) == list:
            urls = url
        else:
            urls.append(url)
        msgId = self.redis_db_service.xadd(self.taskQueueName, {"url": json.dumps(urls), "publishTime": str(int(time.time()))})
        return msgId


    def delTask(self,msgId):
        '''
        加上检测是否被拿去消费了
        :param msgId:
        :return:
        '''
        #检测stream任务是否被取走，没有被取走则删除
        self.redis_db_service.xdel(self.taskQueueName,msgId)



    def setMaxThread(self,serviceName,threadNum:int):
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

    def getService(self,pluginName):
        return Service(pluginName)

if __name__ == '__main__':
    a = RedisMixin().redis_db_service.hkeys('plugin-center')
    print(a)