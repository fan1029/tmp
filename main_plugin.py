from plugins import importPlugins
from funboost import boost, BrokerEnum
import socket
from lib.pluginManager import PluginManager
importPlugins()
pluginReg = PluginManager()


if __name__ == '__main__':
    a = PluginManager()
    NameList = a.getPluginNameList()
    for _ in NameList:
        print(_)
        fun = a.getPluginRunFunction(_)
        clazz = a.getPlugin(_)
        if clazz.runLocal:
            boostFun = boost(_ + socket.gethostname(), broker_kind=BrokerEnum.REDIS_STREAM)(fun)
        else:
            boostFun = boost(_ , broker_kind=BrokerEnum.REDIS_STREAM)(fun)
        boostFun.consume()