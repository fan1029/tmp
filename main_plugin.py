from plugins import importPlugins
from utils.redis_manager import RedisMixin
from core.pluginManager import PluginManager
from plugins.BasePlugin import BasePlugin
from core.notify import Notify
import json

if __name__ == '__main__':
    importPlugins()
    pluginManager = PluginManager()
    # print(pluginManager.getPluginTableList())
    NameList = pluginManager.getPluginNameList()
    while True:   #处理插件结果的
        ResultList = RedisMixin().redis_db_service.lpop('plugin-result', 10)
        if ResultList:
            for _ in ResultList:
                _ = json.loads(_)
                if _.get('error'):
                    Notify('System').error(_.get('msg'))
                else:
                    pluginObj: BasePlugin = pluginManager.getPlugin(_.get('pluginName'))
                    pluginObj().onBeforeResult(_.get('url'), _)
