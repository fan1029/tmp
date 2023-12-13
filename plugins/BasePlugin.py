from nb_log import LoggerMixin
from utils.redis_manager import RedisMixin
import abc
from typing import List, Union
from core.asset import Asset
from plugins.common import pluginLock, pluginUnlock, pushUndoQueue, removeUndoQueue, checkAllFinished, getComputerName, \
    registerAsset, addAssetOriginalToTable, checkAndCreatePlutinTable
from core.service import ServiceMixIn
from core.notify import NotifyMixin


class BasePlugin(LoggerMixin, RedisMixin, ServiceMixIn, NotifyMixin, metaclass=abc.ABCMeta):
    pluginName = 'basePlugin'
    pluginNameZh = '插件基类'
    tableName = pluginName + '_table'
    scanTargetType = ['domain', 'ip']
    author = 'maple'
    version = '1.0'
    description = ''
    columnDict = {
    }
    runMode = 1
    # postgreSql创建表格语句.主键为asset character varying(255) NOT NULL，第二个是screen_img 对于text类型的字段,第三个字段是时间，默认当前时间
    postgreSqlTableCreatteSql = f'''
    '''

    def __init__(self):
        # self.consumers: List[str] = self.getService(self.pluginName).getAllService()
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
        res = checkAndCreatePlutinTable(self.postgreSqlTableCreatteSql, self.pluginName)
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

    def fileter(self, traget: str):
        '''
        资产过滤器，将资产转换为想要的格式。
        :param target:
        :return:
        '''
        return traget

    def registerTargetMap(self, target: str, assetId: str):
        '''
        注册资产到资产表格
        :param target:
        :return:
        '''
        self.redis_db_service.hset('asset_target_Map' + self.pluginName, target, assetId)

    def getAssetIdByTarget(self, target: str):
        '''
        通过target获取assetId
        :param target:
        :return:
        '''
        return self.redis_db_service.hget('asset_target_Map' + self.pluginName, target)

    def delAssetIdByTarget(self, target: str):
        '''
        通过target删除assetId
        :param target:
        :return:
        '''
        return self.redis_db_service.hdel('asset_target_Map' + self.pluginName, target)

    def targetPerHandle(self, assets: List[Asset]):
        '''
        资产预处理
        :param asseta:
        :return:
        '''

        tmp = []
        res = []
        for _ in assets:
            if _.getAssetType() in self.scanTargetType:
                tmp.append(_)
        for _ in tmp:
            if 'originalAssets' not in self.scanTargetType:
                res.append({'assetId': _.id, 'assetName': _.getAssetName(), 'target': _.getAssetName()})
            else:
                for i in _.original_assets:
                    res.append({'assetId': _.id, 'assetName': _.getAssetName(), 'target': i})
        for _ in res:
            _['target'] = self.fileter(_.get('target'))
        # 删除res中重复的target
        tmp2 = []
        duplicateCheckTmp = []
        for _ in res:
            if _['target'] not in duplicateCheckTmp:
                if _['target']:
                    tmp2.append(_)
                    duplicateCheckTmp.append(_['target'])
        for _ in tmp2:
            self.init_plugin_table(_.get('assetName'))
            self.registerTargetMap(_['target'], _.get('assetId'))
        tmp3 = []
        for _ in tmp2:
            tmp3.append(_['target'])
        self.notifier.info(f'目标过滤完成,目标数量{len(tmp3)},准备执行！', title=self.pluginNameZh)
        return tmp3

    def run(self, ids: list, config: dict):
        tmpAssets = [Asset().initAsset(id=_) for _ in ids]
        AssetsDictList = self.targetPerHandle(tmpAssets)
        if self.runMode == 0:
            for _ in AssetsDictList:
                msgId = self.getService(self.pluginName).addTask(_, config=config)
        elif self.runMode == 1:
            msgId = self.getService(self.pluginName).addTask(AssetsDictList, config=config)
        else:
            self.logger.error('运行类型匹配失败')
            self.notifier.error(f'运行类型匹配失败', title=self.pluginNameZh)

    def onBeforeResult(self, target: str, data: dict):
        '''
        结果处理前的操作
        :param target:
        :return:
        '''

        tmp = self.getAssetIdByTarget(target)
        if tmp:
            self.delAssetIdByTarget(target)
            asset = Asset().initAsset(id=tmp)
            self.onResult(asset, data)
            self.notifier.info(f'任务完成,target:{target}', title=self.pluginNameZh)
        else:
            self.notifier.error(f'结果回调时未找到资产的原始映射资产,target:{target}。结果丢弃', title=self.pluginNameZh)

    def onResult(self, asset: Asset, result: dict):
        pass
