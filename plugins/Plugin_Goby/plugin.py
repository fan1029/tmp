from plugins.BasePlugin import BasePlugin
import multiprocessing
from plugins.Plugin_Goby.common import runScan, checkProgress, getStatisticsData, assetSearch, stopScan, dataStore
# from services.screenshot.main import runFromPythonImport
from core.rowManager import RowManagerProxy
from type.elements import Tag, Text, Popover, Action, TagAttribute, TextAttribute
from type.enums import SIZE, TAG_THEME, TAG_ROUND, TEXT_TYPE, TEXT_TAG
from core.asset import Asset
import nb_log



class Plugin_Goby(BasePlugin):
    pluginName = 'plugin_goby'
    pluginNameZh = 'Goby扫描插件'
    tableName = pluginName + '_table'
    scanTargetType = ['domain', 'ip']
    author = 'maple'
    version = '1.0'
    description = 'GOBY扫描插件。使用时请关闭代理软件'
    columnDict = {
        'tag': '资产标签',
        'vul': '漏洞',
        'port': '端口',
    }
    runMode = 1
    postgreSqlTableCreatteSql = f'''
    CREATE TABLE IF NOT EXISTS {tableName} (
        asset character varying(255) NOT NULL,
        screen_img text,
        time timestamp without time zone DEFAULT now()
    );
    '''

    def onLoad(self):
        pass

    def filter(self, target):
        return target

    # def startService(self):
    #     from services.plugin_goby.main import runFromPythonImport
    #     p = multiprocessing.Process(target=runFromPythonImport)
    #     p.start()

    @classmethod
    def onResult(cls, asset: Asset, result: dict):
        _ = result.get('data')
        nb_log.info(_)
        # tag
        tagsDict = _['tags']
        if tagsDict is not None:
            if tagsDict:
                productList = [i.get('product') for i in tagsDict]
                tagList = [Tag(content=i, action=Action(click=Popover(content=i, title='test'))) for i in productList]
                asset.setCell('tag', tagList)
        # vul
        vulDict = _['vulnerabilities']
        if vulDict is not None:
            if vulDict:
                vulList = [i.get('name') for i in vulDict]
                vulTextList = [Text(content=i) for i in vulList]
                asset.setCell('vul', vulTextList)
        # port
        portDict: dict = _['protocols']
        if portDict is not None:
            if portDict:
                portList = [(v.get('port') + ':' + v.get('protocol')) for v in portDict.values()]
                portTagList = [Tag(content=i) for i in portList]
                asset.setCell('port', portTagList)
        dataStore(result.get('data'))


