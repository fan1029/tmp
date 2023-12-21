import time
import abc
from utils.redis_manager import RedisMixin
from pluginService.flexibleThreadPool import FlexibleThreadPool
from pluginService.lifeCycleFuntion_manager import LifeCycle
import threading
import socket
import nb_log
import json


class PlguinService(RedisMixin, LifeCycle):
    plugin_name = 'plugin_base'
    maxThread = 3
    mode = 1

    def __init__(self, pluginConfig: dict):
        self.pluginCenterName = 'plugin-center'
        self.plugin_name = pluginConfig.get('pluginName')
        self.redis_result_queue_Name = 'plugin-result'
        self.taskMqName = self.plugin_name.lower() + '-task'
        self.consumer_identification = self.plugin_name.lower() + '-' + socket.gethostname() + '-consumer'
        self.consume_info_key = self.plugin_name.lower() + '-' + socket.gethostname() + '-info'
        self.maxThread = pluginConfig.get('maxThread')
        self.stopFlag = False  # 暂停标志
        self.threadPool = None
        self.info = {"status": "close", "maxThread": self.maxThread, "runningThreadCount": 0,
                     "stopFlag": self.stopFlag, "closeFlag": False, "mode": self.mode, "pluginName": self.plugin_name
            , "hostName": socket.gethostname(), "consumer_identification": self.consumer_identification,
                     "heartBeatTime": int(time.time()), "respondFlag": None}
        self.getMessageCount = self.maxThread
        self.threadLocalObject = threading.local()

    def sendRedisHeartBeat(self):
        self.info["heartBeatTime"] = int(time.time())
        self.updateInfo()

    def initAll(self):
        self.setInfo(status="init")
        self.initThreadPool()
        self.initCount()
        self.initService()
        self.setInfo(status="running")

    def respondToCenter(self):
        self.setInfo(respondFlag=True)

    def setInfo(self, **kwargs):
        self.info.update(kwargs)
        self.updateInfo()

    def initThreadPool(self):
        self.threadPool = FlexibleThreadPool(self.maxThread)

    def initCount(self):
        if self.mode == 2:
            self.getMessageCount = self.maxThread
        elif self.mode == 1:
            self.getMessageCount = 5 * self.maxThread
        else:
            self.getMessageCount = self.maxThread

    def initResultQueue(self):
        # 检测是否有结果队列，没有则创建
        if not self.redis_db_frame.exists(self.redis_result_queue_Name):
            self.redis_db_frame.lpush(self.redis_result_queue_Name, None)

    def getInfo(self):
        try:
            tmp = json.loads(self.redis_db_frame.get(self.consume_info_key))
            return tmp
        except:
            return self.info

    def updateInfo(self):
        self.redis_db_frame.hset(self.pluginCenterName, self.consume_info_key, json.dumps(self.info))

    def updateThreadCount(self):
        self.info["runningThreadCount"] = self.threadPool.num_threads()
        # self.updateInfo()

    def stopService(self):
        self.stopFlag = True
        self.setInfo(stopFlag=True)

    def handleNewInfo(self, Info):
        Info = json.loads(Info)
        if Info.get('closeFlag'):
            self.closeService()
        if Info.get('stopFlag'):
            self.stopService()
        if self.maxThread != Info.get('maxThread'):
            self.maxThread = int(Info.get('maxThread'))
            self.threadPool.set_max_workers(self.maxThread)
        pass

    def setAssetRunningStatus(self, msgId):
        self.redis_db_frame.lpush('assetRunning', msgId)  # 设置状态正在运行

    def delAssetRunningStatus(self, msgId):
        self.redis_db_frame.lrem('assetRunning', 0, msgId)

    def listenBroadCastMessageQueue(self):
        oldInfo = ''
        while True:
            time.sleep(5)
            self.updateThreadCount()
            newInfo = self.getInfo()
            if newInfo != oldInfo:
                self.handleNewInfo(newInfo)
            self.sendRedisHeartBeat()

    def toolRunningWrapper(self,msg_id: str, msg: dict):
        self.threadLocalObject.msgId = msg_id
        self.setAssetRunningStatus(msg_id)  # 设置运行中
        for _ in json.loads(msg.get('targets')):
            nb_log.info(msg.get('targets'))
            self.redis_db_service.set(_+self.plugin_name, msg_id)
        self.getFun('toolRunning')(json.loads(msg.get('targets')), json.loads(msg.get('config')))

    def _submit_task(self, msg_id: str, msg: dict):
        # msgDict = json.loads(msg)
        self.threadPool.submit(self.toolRunningWrapper, msg_id, msg)
        self.updateInfo()

    def listenMessageQueue(self):
        try:
            self.redis_db_frame.xgroup_create(self.taskMqName, self.plugin_name, mkstream=True, id=0)
        except Exception as e:
            nb_log.error(e)

        while True:
            print('开始监听中')
            stopFlag = self.getInfo().get("stopFlag")
            if not stopFlag:
                # if self.threadPool.threads_free_count > 0:
                results = self.redis_db_frame.xreadgroup(self.plugin_name, self.consumer_identification,
                                                         {self.taskMqName: ">"}, count=self.maxThread,
                                                         block=60 * 1000)
                if results:
                    for msg_id, msg in results[0][1]:

                        self._submit_task(msg_id, msg)  # 提交运行
                        time.sleep(1)

    def initService(self):
        self.getFun('toolInit')()
        pass

    def closeService(self):
        exit(0)
        pass

    def reStartService(self):
        pass

    def getConfig(self):
        pass

    def getThread(self):
        pass

    def ackMsg(self):
        '''
        消息确认
        :param msgId:
        :return:
        '''
        self.redis_db_frame.xack(self.taskMqName, self.plugin_name, self.threadLocalObject.msgId)
        self.redis_db_frame.xdel(self.taskMqName, self.threadLocalObject.msgId)
        self.delAssetRunningStatus(self.threadLocalObject.msgId)  # 删除运行中

    def reportError(self, msg:str,targets:list):
        try:
            msgId = self.threadLocalObject.msgId
        except:
            msgId = self.redis_db_service.get(targets[0] + self.plugin_name)
            self.threadLocalObject.msgId = msgId
        self.redis_db_frame.lpush(self.redis_result_queue_Name, json.dumps({'pluginName': self.plugin_name,
                                                                            'msgId': self.threadLocalObject.msgId, 'error': True,
                                                                            'msg': msg,
                                                                            'targets': targets}))
        self.ackMsg()

    def setResult(self, url, res, finish=True):
        try:
            msgId = self.threadLocalObject.msgId
        except:
            msgId = self.redis_db_service.get(url + self.plugin_name)
            self.threadLocalObject.msgId = msgId
        resStruct = {"pluginName": self.plugin_name, "url": url, "data": res, "finish": finish, "msgId": self.threadLocalObject.msgId}
        RedisMixin().redis_db_frame.lpush(self.redis_result_queue_Name, json.dumps(resStruct))
        if finish:
            self.ackMsg()

    def regPluginCenter(self):
        self.redis_db_service.hset(self.pluginCenterName, self.consume_info_key, json.dumps(self.info))

    def runService(self):
        self.setInfo(status="opening")
        self.initAll()
        self.listenMessageQueue()
        threading.Thread(target=self.listenBroadCastMessageQueue, daemon=True).start()
