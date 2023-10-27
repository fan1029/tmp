import abc
from typing import List, Type, Union
from utils.store import Store
from utils.utils import md5Encode
from type.types import Asset
from dataclasses import fields
from utils.notify import Notify
from funboost import boost, BrokerEnum


class AbstractPlugin():

    def __init__(self, assets):
        self.pluginName = None
        self.processNum = None
        self.threadNum = None
        self.hasMoreInfoPage = False
        self.hasSingleInfoPage = False
        self.hasColumn = False
        self.assets = []
        self.columns = None
        self.MoreInfoPageContent = None
        self.perUrlTimeOut = None
        self.store = Store()
        self.assets = []
        self.notify = Notify(self.pluginName)
        for _ in assets:
            self.assets.append(Asset(assetOriginal=_, assetFiltered=self.filter(_)))

    def __plugin_lock(self, asset: Asset):
        pass
        self.store.lpush('lock' + md5Encode(asset.assetFiltered), self.pluginName)

    def __pluginUnlock(self, asset: Asset):
        self.store.lrem('lock' + md5Encode(asset.assetFiltered), 0, self.pluginName)

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
        return url

    def setData(self, url):
        # todo: 从数据库中放入插件执行数据
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
            obj(**var).pluginRun(asset)

        return tmp

    def runAll(self) -> None:
        '''
        执行所有url,去重数据，添加未完成队列
        :return:
        '''
        # todo:最终将所有url执行pluginRun

        self.pluginStatusOn()
        tmpFun = self.getFunction()
        a = boost(self.pluginName, broker_kind=BrokerEnum.REDIS_STREAM, concurrent_num=1)(tmpFun)
        runList = []
        # self.tmprun=[]
        for _ in self.assets:
            if _.assetFiltered in runList:
                continue
            else:
                self.store.lpush('undo' + self.pluginName, _.assetFiltered)
                runList.append(_.assetFiltered)
                a.push(_)
                # self.pluginRun(_)

    def pluginRun(self, asset: Asset):
        # todo: 单个url执行pluginRun的流程
        # 送到队列中，等待执行
        self.__plugin_lock(asset)
        finished, error = self.run(asset)
        if finished:
            self.store.lrem('undo' + self.pluginName, 0, asset.assetFiltered)
            self.__pluginUnlock(asset)
            self.__checkAllFinished()
            return True
        else:
            self.__pluginUnlock(asset)
            self.store.lrem('undo' + self.pluginName, 0, asset.assetFiltered)
            self.__checkAllFinished()
            self.notify.error('资产执行失败\n+' + asset.assetOriginal + '\n' + error)
            return False
        pass

    def run(self, asset: Asset) -> (bool, str):
        '''
        执行插件
        :param asset:
        :return:
        '''
        pass

    def pluginStop(self):
        # todo: 停止运行
        return False

    def pluginRestart(self):
        # todo: 插件服务重启
        return False

    def onLoad(self):
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

    def __call__(self, *args, **kwargs):
        attrs = vars(self)
        return type(self)(**attrs).runAll()
