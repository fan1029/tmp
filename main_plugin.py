from plugins import importPlugins
from utils.redis_manager import RedisMixin
from core.pluginManager import PluginManager
from plugins.BasePlugin import BasePlugin
from core.notify import Notify
import json

if __name__ == '__main__':
    importPlugins()
    pluginManager = PluginManager()
    NameList = pluginManager.getPluginNameList()
    while True:   #处理插件结果的
        ResultList = RedisMixin().redis_db_service.lpop('plugin-result',10)
        # ResultList = RedisMixin().redis_db_service.lrange('plugin-result', 0,-1)
        if ResultList:
            for _ in ResultList:
                _ = json.loads(_)
                pluginObj: BasePlugin = pluginManager.getPlugin(_.get('pluginName'))
                if _.get('error'):
                    pluginObj().onError(_.get('msgId'),_.get('msg'),_.get('targets'))
                else:

                    pluginObj().onBeforeResult(_.get('url'), _)
