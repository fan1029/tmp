from nb_log import  LoggerMixin
from utils.redis_manager import RedisMixin
import abc
from typing import List, Union
from utils.utils import md5Encode
from type.myTypes import Asset
from plugins.common import pluginLock, pluginUnlock, pushUndoQueue, removeUndoQueue, checkAllFinished, getComputerName, \
    registerAsset, addAssetOriginalToTable,checkAndCreatePlutinTable
from lib.service import ServiceMixIn


class BasePlugin(LoggerMixin, RedisMixin, ServiceMixIn, metaclass=abc.ABCMeta):
    pluginName = 'basePlugin'
    tableName = pluginName + '_table'
    author = 'maple'
    version = '1.0'
    description = ''
    columnDict = {
    }
    runMode = 1
    #postgreSql创建表格语句.主键为asset character varying(255) NOT NULL，第二个是screen_img 对于text类型的字段,第三个字段是时间，默认当前时间
    postgreSqlTableCreatteSql = f'''
    '''

    def __init__(self):
        self.consumers: List[str] = self.getService(self.pluginName).getAllService()
        self.databaseCheck()
        self.createPluginTable()
        pass


    def onLoad(self):
        pass

    def databaseCheck(self):
        '''
        数据库检测，如果不存在则创建
        :return:
        '''
        res  = checkAndCreatePlutinTable(self.postgreSqlTableCreatteSql,self.pluginName)
        if res:
            self.logger.info('初次运行未检测到数据库表格，已创建')
        else:
            self.logger.info('数据库表格已存在,跳过创建')


    def createPluginTable(self):
        '''
        创建插件自定义表格
        :return:
        '''
        pass

    def init_plugin_table(self, asset_origianl: str):
        '''
        初始化插件表格表，pluginname_table.添加asset_original
        :return:
        '''
        addAssetOriginalToTable(self.pluginName, asset_origianl)

    def startService(self):
        '''
        每个插件必须实现。服务的启动方式
        :return:
        '''
        pass

    def filter(self, target: str) -> str:
        '''
        资产过滤器，将资产转换为想要的格式
        :param target:
        :return:
        '''
        return target

    def run(self, urls):
        assets = []
        for _ in urls:
            assets.append(self.filter(_))  # 将资产过滤后添加到assets中
            self.logger.debug(assets)
        for _ in assets:
            registerAsset(self.pluginName, Asset(assetOriginal=_,assetFiltered=self.filter(_)))  # 注册资产过滤前后映射关系
            self.init_plugin_table(_)  # 添加资产到插件表格中。
        if self.runMode == 0:
            for _ in assets:
                msgId = self.getService(self.pluginName).addTask(_)
        elif self.runMode == 1:
            urlList = [_ for _ in assets]
            msgId = self.getService(self.pluginName).addTask(urlList)
        else:
            self.logger.error('运行类型匹配失败')

    def onResult(self, url: str, result: dict):
        '''
        总控回调函数，用于处理插件返回的结果
        {"url":"","data":{}}//根据自己定义的数据返回，自己处理
        :param result:
        :return:
        '''
        pass
