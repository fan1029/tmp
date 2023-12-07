from plugins.BasePlugin import BasePlugin
import multiprocessing
from plugins.Plugin_Goby.common import runScan, checkProgress, getStatisticsData, assetSearch, stopScan, dataStore
# from services.screenshot.main import runFromPythonImport
from lib.rowManager import RowManagerProxy
from type.elements import Tag, Text, Popover, Action, TagAttribute, TextAttribute
from type.enums import SIZE, TAG_THEME, TAG_ROUND, TEXT_TYPE, TEXT_TAG
import nb_log



class Plugin_Goby(BasePlugin):
    pluginName = 'plugin_goby'
    tableName = pluginName + '_table'
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
    #     from services.goby.main import runFromPythonImport
    #     p = multiprocessing.Process(target=runFromPythonImport)
    #     p.start()

    @classmethod
    def onResult(cls, url: str, result: dict):
        '''
        每个插件必须实现。处理结果
        :param msg:
        :return:
        '''
        _ = result.get('data')
        nb_log.info(_)
        if _['hostnames'][0] != "":
            assetFiltered = _['hostnames'][0]
        else:
            assetFiltered = _['ip']
        rowManager = RowManagerProxy(cls.pluginName, assetFiltered)  # 构造表格数据
        #####处理数据########
        # tag
        tagsDict = _['tags']
        if tagsDict is not None:
            if tagsDict:
                productList = [i.get('product') for i in tagsDict]
                rowManager.cellClear('tag')
                # tagList = [Tag(content=i, round=True, theme='dark',click=Popover(content=i,title='test')) for i in productList]
                tagList = [Tag(content=i, action=Action(click=Popover(content=i, title='test'))) for i in productList]
                rowManager.cellListSet('tag', tagList)
        # rowManager.submitRow(columnName='tag')
        # vul
        vulDict = _['vulnerabilities']
        if vulDict is not None:
            if vulDict:
                vulList = [i.get('name') for i in vulDict]
                vulTextList = [Text(content=i) for i in vulList]
                rowManager.cellListSet('vul', vulTextList)
        # port
        portDict: dict = _['protocols']
        if portDict is not None:
            if portDict:
                portList = [(v.get('port') + ':' + v.get('protocol')) for v in portDict.values()]
                portTagList = [Tag(content=i) for i in portList]
                rowManager.cellListSet('port', portTagList)
        rowManager.submitRow()
        dataStore(result.get('data'))


