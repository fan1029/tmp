import sys
sys.path.append('..')
sys.path.append('../..')
import time
from plugins.abstractPlugin import AbstractPlugin
from plugins.Plugin_Goby.gobyTypes import ScanModel, AssetSearchModel, GobyAsset, Options, OptionsAssetSearch, \
    Vulnerability, PluginInfo
from multiprocessing import Process
from plugins.Plugin_Goby.common import runScan, checkProgress, getStatisticsData, assetSearch, stopScan, dataStore
from type.elements import Tag, Text, Popover,Action,TagAttribute,TextAttribute
from type.enums import SIZE, TAG_THEME, TAG_ROUND, TEXT_TYPE, TEXT_TAG
from utils.store import Store
import nb_log
import os
import random
from lib.row import RowManagerProxy



class Plugin_Goby(AbstractPlugin):
    pluginName = 'Plugin_Goby'
    tableName = 'plugin_goby_table'
    author = 'maple'
    version = '1.0'
    description = 'Goby扫描器插件-启动时请不要使用代理,否则会导致启动失败'
    columnDict = {
        'tag': '资产标签',
        'vul': '漏洞',
        'port': '端口',
    }
    runLocal = True

    def __init__(self, assets: list, settings: dict):
        AbstractPlugin.__init__(self, assets, settings)
        self.pluginName = 'Plugin_Goby'
        self.processNum = 1
        self.threadNum = 1
        self.hasMoreInfoPage = True
        self.hasColumn = True
        self.MoreInfoPageContent = None
        self.perUrlTimeOut = None
        self.host = []
        self.taskId = None
        self.hostSelected = ''
        self.runMode = 'check'
        # self.settings =

    def filter(self, target: str) -> str:
        '''
        对资产进行过滤，返回一个字符串
        :param asset:
        :return:
        '''
        # 识别目标asset.asseet_original是ip还是域名。如果是IP，有端口则去除端口保留ip。如果是url则去除http/https协议头。只保留域名。
        if target.startswith('http://'):
            target = target[7:]
        elif target.startswith('https://'):
            target = target[8:]
        if target.find(':') != -1:
            target = target[:target.find(':')]
        if target.endswith('/'):
            target = target[:-1]
        return target

    def registerFreeTimeQueue(self):
        '''
        将本地的空闲进程名注册到空闲队列
        :return:
        '''
        for _ in self.host:
            self.store.lpush('freeTimeQueue_' + self.pluginName + '_' + self.computerName, _)

    def removeFreeTimeQueue(self, host):
        '''
        将本地的空闲进程名注册到空闲队列
        :return:
        '''
        self.store.lrem('freeTimeQueue_' + self.pluginName + '_' + self.computerName, 0, host)

    def addFreeTimeQueue(self, host):
        '''
        将本地的空闲进程名注册到空闲队列
        :return:
        '''
        self.store.lpush('freeTimeQueue_' + self.pluginName + '_' + self.computerName, host)

    @staticmethod
    def runGoBy(GOBY_LIB_PATH, host: str):
        os.system(GOBY_LIB_PATH + ' -mode api -bind ' + host)

    def onLoad(self):
        '''
        Todo:读取配置文件
        :return:
        '''
        act_nums = 1
        self.runLocal = True
        GOBY_LIB_PATH = "D:\TOOLS\goby-win-x64-2.1.2\golib\goby-cmd.exe"
        for _ in range(act_nums):
            self.host.append('127.0.0.1:' + str(random.randint(9000, 9900)))
        for _ in self.host:
            nb_log.info('启动goby进程：' + _)
            p = Process(target=Plugin_Goby.runGoBy, args=(GOBY_LIB_PATH, _))
            p.start()
            time.sleep(15)

        self.registerFreeTimeQueue()

    def onStartLocal(self):
        '''
        启动插件
        :return:
        '''
        # 检测队列是否存在可以使用的进程
        host = self.store.lpop('freeTimeQueue_' + self.pluginName + '_' + self.computerName)
        if not host:
            nb_log.error("没有可用的进程")
        else:
            # 创建scanModel
            self.hostSelected = host
            scanModel = ScanModel(
                taskName='dataCenter' + str(random.randint(1, 999999)),
                asset=GobyAsset(
                    ips=list(set([_.assetFiltered for _ in self.assets])),
                    ports='21,22,80,U:137,443,445,3306,3389,8080'),
                vulnerability=Vulnerability(),
                options=Options(rate=1000),
            )
            res, msg = runScan(host, scanModel)
            if res:
                self.taskId = msg
                self.store.hset('runningTask_' + self.pluginName + '_' + self.computerName, host, msg)
            else:
                self.store.lpush('freeTimeQueue_' + self.pluginName + '_' + self.computerName, host)
                self.notify.error('任务启动失败\n' + msg)
            # 开始扫描

        pass


# @PluginManager.pluginRunFunctionRegister('Plugin_Goby')
def Plugin_Goby_Run(obj: Plugin_Goby):
    '''
    远程/本地 多线程/进程执行的函数。主要用于，扫描逻辑，检测结果等。
    :param obj:
    :return:
    '''
    store = Store()
    nb_log.info('进入check！')
    res, msg = checkProgress(obj.hostSelected, obj.taskId)
    res2, msg2 = assetSearch(obj.hostSelected, obj.taskId)
    nb_log.info((res2, msg2))
    nb_log.info((res, msg))

    if res2:
        for _ in msg2:
            nb_log.info(_)
            if _['hostnames'][0] != "":
                assetFiltered = _['hostnames'][0]
            else:
                assetFiltered = _['ip']
            rowManager = RowManagerProxy(obj.pluginName, assetFiltered)  # 构造表格数据
            #####处理数据########
            # tag
            tagsDict = _['tags']
            if tagsDict is not None:
                if tagsDict:
                    productList = [i.get('product') for i in tagsDict]
                    rowManager.cellClear('tag')
                    # tagList = [Tag(content=i, round=True, theme='dark',click=Popover(content=i,title='test')) for i in productList]
                    tagList = [Tag(content=i, action=Action(click=Popover(content=i,title='test'))) for i in productList]
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
            #########################
            dataStore(_)  # 存储扫描数据

    if res:
        if int(msg) == 100:
            obj.notify.info('任务已完成')
            obj.delCheckQueue()
            store.lpush('freeTimeQueue_' + obj.pluginName + '_' + obj.computerName, obj.hostSelected)
            store.hdel('runningTask_' + obj.pluginName + '_' + obj.computerName, obj.hostSelected)
            obj.hostSelected = ''
            obj.taskId = ''
        else:
            print('任务进度：' + str(msg) + '%')


if __name__ == '__main__':
    # print(a.getList())
    # print(funReg.getFunList())
    # print(funReg.getFunList())
    # 对filter函数进行测试
    # from
    a = Plugin_Goby(["10.1.72.121","10.1.99.100"], {})
    # func = a.getFunctionCheck()
    # a = boost(a.pluginName, broker_kind=BrokerEnum.REDIS_STREAM, concurrent_num=1)(func)
    # a.clear()
    # a = Plugin_Goby(["10.1.99.100"], {})
    a.onLoad()
    a.runAll()
    # a.getSelfQueueName()
    # func = a.getFunctionCheck()
