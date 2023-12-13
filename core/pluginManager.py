# 插件管理器，负责插件加载,重启,卸载,更新等
import json
import os
import pickle
from utils.redis_manager import RedisMixin
# from plugins.abstractPlugin import AbstractPlugin


class PluginManager(RedisMixin):
    __instance = None
    __pluginList = {}

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(PluginManager, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        pass



    @staticmethod
    def regInRedis(cls):
        info = {'pluginName': cls.pluginName, 'author': cls.author, 'version': cls.version, 'description': cls.description,'tableName':cls.tableName,'columnDict':cls.columnDict,'runMode':cls.runMode}
        RedisMixin().redis_db_service.hset('plugin', cls.pluginName,json.dumps(info))


    @staticmethod
    def pluginClassRegister(pluginName: str):
        '''
        注册插件类
        :param pluginName:
        :return:
        '''

        # 类装饰器，将获取的类添加到__pluginList中
        def wrapper(cls):
            PluginManager.__pluginList[pluginName.lower()] = {
                "class": cls, "fun": None, "obj": []}
            PluginManager.regInRedis(cls)
            return cls

        return wrapper

    @staticmethod
    def pluginRunFunctionRegister(pluginName: str):
        '''
        注册远程调用函数
        :param pluginName:
        :return:
        '''

        # 注册远程调用函数
        def wrapper(func):
            # def inner(obj):  # 序列化对象数据处理
            #     if obj:
            #         obj = pickle.loads(bytes.fromhex(obj))
            #         obj.onRemoteNew()
            #     return func(obj)

            PluginManager.__pluginList[pluginName.lower()]['fun'] = func
            return func

        return wrapper

    # def resultHandler(self, pluginName: str, result: dict):
    #     while True:
    #         self.redis_db_service.rpop('plugin-result')
    #     pass



    def getPluginNameList(self) -> list:
        '''
        获取插件名称列表
        :return:
        '''
        nameList = []
        for k in self.__pluginList.keys():
            nameList.append(k)
        return nameList

    def pluginOnLoad(self) -> None:
        '''
        加载插件
        :param pluginName:
        :return:
        '''
        # 依次调用注册了插件的类的onLoad静态方法
        for _ in self.__pluginList.values():
            _['class'].onLoad()

    def reloadPlugin(self, pluginName):
        '''
        重载插件
        :param pluginName:
        :return:
        '''
        # 从插件列表中删除插件,重新读取插件文件,重新加载插件
        pass

    def unloadPlugin(self, pluginName):
        '''
        卸载插件
        :param pluginName:
        :return:
        '''
        # 从插件列表中删除插件,删除插件文件,调用插件的onUnload方法
        pass

    def getPlugin(self, pluginName):
        '''
        获取插件类
        :param pluginName:
        :return:
        '''
        return self.__pluginList[pluginName.lower()]['class']

    def getPluginRunFunction(self, pluginName):
        '''
        获取插件远程调用函数
        :param pluginName:
        :return:
        '''
        return self.__pluginList[pluginName.lower()]['fun']

    def newPluginObj(self, pluginName: str, asset: str) -> object:
        '''
        实例化插件对象
        :param pluginName:
        :param asset:
        :return:
        '''
        obj = self.__pluginList[pluginName.lower()]['class'](asset)
        self.__pluginList[pluginName.lower()]['obj'].append(obj)
        return obj

    def getPluginTable(self, pluginName: str):
        '''
        获取插件表名
        :param pluginName:
        :return:
        '''
        tableName = self.__pluginList[pluginName.lower()]['class'].tableName
        columnDict = self.__pluginList[pluginName.lower()]['class'].columnDict
        return {tableName: columnDict}

    def getPluginTableList(self):
        '''
        获取所有插件表名列表
        :return:
        '''
        tableList = []
        pluginNameList = self.getPluginNameList()
        for pluginName in pluginNameList:
            tableList.append(self.getPluginTable(pluginName))
        return tableList


    def getList(self):
        return self.__pluginList
