import datetime
from utils.sqlHelper import PostgresConnectionContextManager
import json
from typing import List, Union


class OperateLog():
    '''
    操作日志记录类
    '''
    def __init__(self, userName,projectId):
        self.operateUserName = userName
        self.projectId = projectId


    def _setDB(self, message,targets:list):
        '''
        设置数据库
        :param msgType:
        :param message:
        :return:
        '''
        with PostgresConnectionContextManager() as cur:
            cur.execute('INSERT INTO log (user_name,target, content,project_id) VALUES (%s,%s,%s,%s)',
                        (self.operateUserName, targets, message,self.projectId))


    def addAsset(self, target:Union[List,str]):
        message = f'添加了新资产'
        if isinstance(target,str):
            target = [target]
        self._setDB(message,target)


    def delAsser(self, target:str):
        message = f'删除了资产{target}'
        if isinstance(target,str):
            target = [target]
        self._setDB(message,target)

    def runPlugin(self, pluginName, target:Union[List,str]):
        message = f'运行了插件{pluginName}'
        if isinstance(target,str):
            target = [target]
        self._setDB(message,target)

    def pausePlugin(self, consumerName, target:Union[List,str]):
        message = f'暂停了插件消费者{consumerName}'
        if isinstance(target,str):
            target = [target]
        self._setDB(message,target)

    def enterProject(self):
        message = f'进入了项目'
        self._setDB(message,[])

    def addNote(self, target:str):
        message = f'为{target}添加了笔记'
        self._setDB(message,[target])

    def downloadAsset(self,tagName,projectName):
        message = f'下载了资产{tagName},项目{projectName}'
        self._setDB(message,[])


    def markAsset(self,target,color):
        message = f'标记了资产{target},颜色{color}'
        self._setDB(message,[])