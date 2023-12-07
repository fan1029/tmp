from plugins import importPlugins
from utils.redis_manager import RedisMixin
from lib.pluginManager import PluginManager
from plugins.BasePlugin import BasePlugin
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
                pluginObj: BasePlugin = pluginManager.getPlugin(_.get('pluginName'))
                pluginObj.onResult(_.get('url'), _)
