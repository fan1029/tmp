import random
import time
from typing import List, Union
import pickle
from lib.pluginManager import PluginManager
from utils.store import Store
from utils.utils import md5Encode
from type.types import Asset
from lib.notify import Notify
from funboost import boost, BrokerEnum
from plugins.common import pluginLock, pluginUnlock, pushUndoQueue, removeUndoQueue, checkAllFinished, getComputerName, \
    registerAsset, addAssetOriginalToTable


class AbstractPlugin():
    pluginName='AbstractPlugin'
    tableName=pluginName+'_table'
    author = 'maple'
    version = '1.0'
    description = ''
    columnDict = {
    }
    runLocal = False
    def __init__(self, assets: list, settings: dict):
        self.checkQueueName = ""
        # self.runLocal: bool = False
        self.computerName: str = ''
        # self.pluginName: str = ''
        self.assets: list = []
        self.store = Store()
        self.config = {}
        self.assets: List[Asset] = []
        self.runMode = 'run'
        self.notify = Notify(self.pluginName, self.config.get('projectId'))  # 初始化通知类
        for _ in assets:
            self.assets.append(Asset(assetOriginal=_, assetFiltered=self.filter(_)))  # 将资产过滤后添加到assets中
        for _ in self.assets:
            registerAsset(self.pluginName, _)  # 注册资产过滤前后映射关系
            self.init_plugin_table(_.assetOriginal)  # 添加资产到插件表格中。

        self.__setConfig(settings)
        self.computerName = getComputerName()  # 获取主机名
        self.checkQueueName = self.getCheckQueueName()  # 获取检查队列名，部分轮询结果的插件可使用。

    def init_plugin_table(self, asset_origianl: str):
        '''
        初始化插件表格表，pluginname_table.添加asset_original
        :return:
        '''
        addAssetOriginalToTable(self.pluginName, asset_origianl)

    def onRemoteNew(self):
        '''
        远程实例化该组建后要做的事情
        :return:
        '''
        # 恢复无法序列化过来的对象
        if self.store is None:
            self.store = Store()

    def __setConfig(self, settings: dict):
        self.config = settings

    def getSelfQueueName(self):
        if self.runLocal:
            return self.pluginName + self.computerName
        else:
            return self.pluginName

    def cacheAssetExist(self, asset: Asset) -> None:
        '''
        将资产缓存到Redis中,同插件再次扫描到该资产时直接跳过
        :param asset:
        :param url:
        :return:
        '''
        self.store.hset('assetExist' + self.pluginName, md5Encode(asset.assetFiltered), asset.assetFiltered)

    def checkAssetExistCache(self, asset: Asset) -> bool:
        '''
        检查资产是否存在缓存中
        :param url:
        :return:
        '''

        return self.store.hexists('assetExist' + self.pluginName, md5Encode(asset.assetFiltered))

    def getUnCachedAsset(self, assets: List[Asset]):
        unCachedAsset = []
        for _ in assets:
            if not self.checkAssetExistCache(_):
                unCachedAsset.append(_)

    def sendDataToFront(self, data: Union[dict, list]) -> None:
        # 如果有实时返回扫描结果的需求，使用该方法将未扫描完成的但是出来了一点结果的数据发送到前端
        # 结果放入redis,前端轮询获取redis中需要的url的结果

        pass

    def filter(self, url: str) -> str:
        '''
        url过滤器
        :param urls:
        :return:
        '''
        pass

    def pluginStatusOn(self):
        self.onStartLocal()
        self.notify.info('插件启动')
        pass

    def pluginStatusOff(self):
        self.onFinish()
        self.notify.info('插件运行结束')
        pass

    def __checkAllFinished(self):
        queueLen = self.store.llen('undo' + self.pluginName)
        if queueLen == 0:
            self.pluginStatusOff()
            return True

    def getFunction(self):
        obj = type(self)
        var = vars(self)

        def tmp(asset):
            obj.getNewObj(var)

        return tmp

    def getFunctionCheck(self):
        obj = type(self)
        var = vars(self)

        def tmp():
            obj.getNewObj(var)

        return tmp

    @staticmethod
    def getFunctionCheck2(objName, var):
        obj = globals()[objName]
        var['assets'] = [Asset(**_) for _ in var['assets']]

    def getCheckQueueName(self):
        '''
        获取检查队列名称
        :return:
        '''
        queueName = self.pluginName + str(random.randint(1, 22222))
        return queueName

    def addCheckQueue(self):
        '''
        向检查队列添加未完成标志
        :return:
        '''

        self.store.set(self.checkQueueName, '1')
        return True

    def delCheckQueue(self):
        '''
        删除未完成标志
        :return:
        '''
        self.store.delete(self.checkQueueName)

    def getCheckQueue(self):
        '''
        获取未完成标志
        :return:
        '''
        return self.store.get(self.checkQueueName)

    def runAll(self) -> None:
        '''
        执行所有url,去重数据，添加未完成队列
        :return:
        '''
        # todo:最终将所有url执行pluginRun

        self.pluginStatusOn()
        if self.runMode == 'run':  # 细粒度能达到单个url的
            tmpFun = self.getFunction()  # 获取run函数
            if not self.runLocal:
                a = boost(self.pluginName.lower(), broker_kind=BrokerEnum.REDIS_STREAM, concurrent_num=1)(tmpFun)
            else:
                a = boost(self.pluginName.lower() + self.computerName, broker_kind=BrokerEnum.REDIS_STREAM, concurrent_num=10)(
                    tmpFun)
            runList = []
            for _ in self.assets:  # 去重资产
                if _.assetFiltered in runList:
                    continue
                else:  # 添加到未完成队列
                    pushUndoQueue(self.pluginName, _)
                    runList.append(_.assetFiltered)
                    # 注意序列化
                    a.push(_.serialize())  # 推送任务

        elif self.runMode == 'check':  # 使用第三方扫描软件，需要一开始就将所有资产推送到队列中,用该方法轮询结果。
            pluginManager = PluginManager()
            tmpFun = pluginManager.getPluginRunFunction(self.pluginName)  # 调用注册函数列表获取函数
            if not self.runLocal:
                a = boost(self.pluginName.lower(), broker_kind=BrokerEnum.REDIS_STREAM, concurrent_num=1)(tmpFun)
            else:
                a = boost(self.pluginName.lower() + self.computerName, broker_kind=BrokerEnum.REDIS_STREAM, concurrent_num=10)(
                    tmpFun)
            self.addCheckQueue()  # 设置未完成标记 1
            runList = []
            for _ in self.assets:
                if _.assetFiltered in runList:
                    continue
                else:
                    pluginLock(_, self.pluginName)  # 加锁
                    pushUndoQueue(self.pluginName, _)  # 添加到未完成资产列表
            while True:
                if self.getCheckQueue() == '1':  # 检测第三方软件是否完成
                    self.store = None  # 删除无法序列化的对象   #此处要写一个函数，将无法序列化的对象删除
                    a.publish({"obj":pickle.dumps(self).hex()})  # 推送队列
                    self.store = Store()  # 恢复环境
                    time.sleep(5)
                else:
                    for _ in self.assets:
                        pluginUnlock(_, self.pluginName)
                        removeUndoQueue(self.pluginName, _)  # 删除未完成资产列表
                    break

    def pluginRun(self, asset: dict):
        # todo: 单个url执行pluginRun的流程
        # 送到队列中，等待执行
        asset = Asset(**asset)
        pluginLock(asset, self.pluginName)
        finished, error = self.run(asset)
        if finished:
            removeUndoQueue(self.pluginName, asset)
            pluginUnlock(asset, self.pluginName)
            if checkAllFinished(self.pluginName):
                self.pluginStatusOff()
                return True
            else:
                return False
        else:
            # self.pluginUnlock(asset)
            pluginUnlock(asset, self.pluginName)
            removeUndoQueue(self.pluginName, asset)
            self.__checkAllFinished()
            self.notify.error('资产执行失败\n+' + asset.assetOriginal + '\n' + error)
            return False


    def pluginStop(self):
        # todo: 停止运行
        return False

    def pluginRestart(self):
        # todo: 插件服务重启
        return False

    @staticmethod
    def onLoad(self):
        '''
        插件加载时执行，此时插件还没实例化
        :param self:
        :return:
        '''
        pass



    def onStartLocal(self):
        # 插件本地启动时执行，只会在主服务端上运行，其他执行脚本的插件运行端不会运行
        pass

    def onStartRemote(self):
        # 插件启动时执行，在运行该插件的机器上执行
        pass

    def onFinish(self):
        pass

    def cleanData(self):
        pass

    def reSendToMQ(self):
        pass

    def getRes(self, asset: Asset):
        pass
