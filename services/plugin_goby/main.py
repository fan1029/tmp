from services.plugin_goby.lifeCycleFuntion_manager import LifeCycle
from services.plugin_goby.plugin_service import PlguinService
from multiprocessing import Process
from services.plugin_goby.gobyTypes import ScanModel, AssetSearchModel, GobyAsset, Options, OptionsAssetSearch, \
    Vulnerability, PluginInfo
from services.plugin_goby.common import runScan, checkProgress, assetSearch, dataStore
from core.rowManager import RowManagerProxy
from type.elements import Tag, Text, Popover, Action, TagAttribute, TextAttribute
from type.enums import SIZE, TAG_THEME, TAG_ROUND, TEXT_TYPE, TEXT_TAG
import nb_log
import time
import json
import os
import random
import queue

pluginConfig = {
    'pluginName': 'plugin_goby',
    'author': 'maple',
    'maxThread': 1,
    'pluginType': 2,
    'gobyPath': 'D:\TOOLS\goby-win-x64-2.1.2\golib\goby-cmd.exe'
}

GobyFreeProcessQueue = queue.Queue()
service = PlguinService(pluginConfig)


def runGoBy(GOBY_LIB_PATH: str, host: str):
    os.system(GOBY_LIB_PATH + ' -mode api -bind ' + host)


@LifeCycle.toolInit
def initGobyService():
    global GobyFreeProcessQueue
    host = []
    act_nums = pluginConfig.get('maxThread')
    GOBY_LIB_PATH = pluginConfig.get('gobyPath')
    for _ in range(act_nums):
        host.append('127.0.0.1:' + str(random.randint(9000, 9900)))
    for _ in host:
        nb_log.info('启动goby进程API，API端口->' + _)
        p = Process(target=runGoBy, args=(GOBY_LIB_PATH, _))
        p.start()
        GobyFreeProcessQueue.put(_)
    time.sleep(15)


@LifeCycle.toolRunning
def gobyScan(msgId: str,targets:list,config:dict):
    urls = targets
    # if type(urls) == str:
    #     urls = json.loads(urls)
    host = GobyFreeProcessQueue.get()
    nb_log.debug('gobyScan: 获取使用进程API' + host)
    scanModel = ScanModel(
        taskName='dataCenter' + str(random.randint(1, 999999)),
        asset=GobyAsset(
            ips=list(set([_ for _ in urls])),
            ports=config.get('ports')),
        vulnerability=Vulnerability(),
        options=Options(rate=1000),
    )
    res, msg = runScan(host, scanModel)
    if res:
        taskId = msg
    else:
        nb_log.error('gobyScan: 任务启动失败' + msg)
        return

    while True:
        time.sleep(5)
        nb_log.info('进入check！')
        res, msg = checkProgress(host, taskId)
        res2, msg2 = assetSearch(host, taskId)
        nb_log.info((res2, msg2))
        nb_log.info((res, msg))
        if res2:
            for _ in msg2:
                if _['hostnames'][0] != "":
                    assetFiltered = _['hostnames'][0]
                else:
                    assetFiltered = _['ip']
                service.setResult(assetFiltered, _)  # 存储扫描数据

        if res:
            if int(msg) == 100:
                service.ackMsg(msgId)
                nb_log.info('gobyScan: 任务已完成')
                GobyFreeProcessQueue.put(host)
                break
            else:
                print('任务进度：' + str(msg) + '%')


def reg():
    service.regPluginCenter()


def runFromPythonImport():
    service.runService()


if __name__ == '__main__':
    service.runService()
