from utils.sqlHelper import PostgresConnectionContextManager
from utils.redis_manager import RedisMixin
from type.elements import BaseElement
from type.myTypes import Column
from core.common import initColumnValueDB, submitOneRowDB, getAllColumnDB
from typing import List, Union
from core.cellContainer import TextContainer, TagContainer, ImageContainer
from functools import lru_cache
import json


class RowManager():
    def __init__(self, pluginName: str, asset_id: int):
        self.pluginName = pluginName.lower()
        self.asset_id: int = asset_id
        self.column: List[Column] = []
        self.getAllColumn()

    def getAllColumn(self):
        for _ in getAllColumnDB(self.pluginName):
            _ = _[0]
            _.pop('plugin_name')
            self.column.append(Column(**_))
        print(self.column)
        for i in self.column:
            self.initColumnValue(i)
        return self.column

    @staticmethod
    def getCellType(column: Column):
        return column.type

    def setAsset(self, asset_id):
        self.asset_id = asset_id

    def setAssetId(self, asset_id):
        self.asset_id = asset_id

    def getColumn(self, columnName: str):
        for _ in self.column:
            if _.name == columnName:
                return _

    def initColumnValue(self, column: Column):
        # 从pluginName_table表中获取对应的cell对象
        a = initColumnValueDB(self.pluginName, self.asset_id, column.name)  # 查插件表中对应列的数据
        if a is None:
            # raise Exception('数据库中没有对应的记录')
            cellClass = globals()[column.type + 'Container']
            column.container = cellClass()
            return column.container
        if a[0]:
            # 反序列化出Container对象
            cellClass = globals()[a[0]['className']]
            column.container = cellClass.from_dict(a[0])
            return column.container
        else:
            # 如果没有对应的记录，则初始化一个Container对象
            cellClass = globals()[column.type + 'Container']
            column.container = cellClass()
            return column.container

    def cellSet(self, columnName: str, cell: BaseElement):
        column = self.getColumn(columnName)
        column.container.set(cell)

    def cellListSet(self, columnName: str, cellList: List[BaseElement]):
        column = self.getColumn(columnName)
        column.container.clear()
        for _ in cellList:
            column.container.add(_)

    def cellListAdd(self, columnName: str, cellList: List[BaseElement]):
        column = self.getColumn(columnName)
        for _ in cellList:
            column.container.add(_)

    def cellGet(self, columnName: str):
        column = self.getColumn(columnName)
        return column.container.get()

    def cellClear(self, columnName: str):
        column = self.getColumn(columnName)
        column.container.clear()

    def cellAdd(self, columnName: str, cell: BaseElement):
        column = self.getColumn(columnName)
        column.container.add(cell)

    def submitOneRow(self, column: Column):
        cellJson = column.container.toJson()
        submitOneRowDB(self.pluginName, self.asset_id, column.name, cellJson)

    def submitRow(self, columnName: str = ''):

        if columnName:
            column = self.getColumn(columnName)
            self.submitOneRow(column)
        else:
            for _ in self.column:
                self.submitOneRow(_)


class Asset(RedisMixin):

    def __init__(self):
        self.id = None
        self.asset_name = None
        self.asset_type = None
        self.original_assets = []
        self.label = []
        self.row_color = 'DEFAULT'
        self.allPluginInfo = None
        self.initAllPluginInfo()

    def initAsset(self, **kwargs):
        '''
        通过asset_name或者id初始化资产
        :param kwargs:
        :return:
        '''
        if kwargs.get('asset_name'):
            with PostgresConnectionContextManager() as cur:
                cur.execute(
                    'SELECT row_to_json(t) FROM (SELECT id,asset_name,asset_type,original_assets,label,row_color FROM asset WHERE asset_name=%s)t',
                    (kwargs.get('asset_name'),))
                AssetTmp = cur.fetchone()
        elif kwargs.get('id'):
            with PostgresConnectionContextManager() as cur:
                cur.execute(
                    'SELECT row_to_json(t) FROM (SELECT id,asset_name,asset_type,original_assets,label,row_color FROM asset WHERE id=%s)t',
                    (kwargs.get('id'),))
                AssetTmp = cur.fetchone()
            pass
        else:
            raise Exception('init asset failed')
        if AssetTmp:
            AssetTmp = AssetTmp[0]
            self.id = AssetTmp['id']
            self.asset_name = AssetTmp['asset_name']
            self.asset_type = AssetTmp['asset_type']
            self.original_assets = AssetTmp['original_assets']
            self.label = AssetTmp['label']
            self.row_color = AssetTmp['row_color']
        else:
            raise Exception('init asset failed')
        return self

    @lru_cache(maxsize=5)
    def initAllPluginInfo(self):
        self.allPluginInfo = {}
        tmp = self.redis_db_service.hgetall('plugin')
        for k, v in tmp.items():
            self.allPluginInfo[k] = json.loads(v)

    def getAssetType(self):
        return self.asset_type

    def addLabel(self, label):
        # label在数据库中是数组
        self.label.append(label)

        with PostgresConnectionContextManager() as cur:
            cur.execute('UPDATE asset SET label=ARRAY(SELECT DISTINCT UNNEST(array_append(label,%s))) WHERE id=%s', (label, self.id,))

    def delLabel(self, label):
        self.label.remove(label)
        with PostgresConnectionContextManager() as cur:
            cur.execute('UPDATE asset SET label=array_remove(label,%s) WHERE id=%s', (label, self.id,))

    def addOriginalAsset(self, original_asset):
        self.original_assets.append(original_asset)
        with PostgresConnectionContextManager() as cur:
            cur.execute('''
                UPDATE asset 
                SET original_assets = ARRAY(
                    SELECT DISTINCT UNNEST(
                        ARRAY_APPEND(original_assets, %s)
                    )
                ) 
                WHERE id = %s
            ''', (original_asset, self.id,))

    def delOriginalAsset(self, original_asset):
        self.original_assets.remove(original_asset)
        with PostgresConnectionContextManager() as cur:
            cur.execute('UPDATE asset SET original_assets=array_remove(original_assets,%s) WHERE id=%s',
                        (original_asset, self.id,))

    def setColor(self, color):
        self.row_color = color
        with PostgresConnectionContextManager() as cur:
            cur.execute('UPDATE asset SET row_color = %s WHERE id=%s', (color, self.id,))

    def getAssetName(self):
        return self.asset_name



    def getOriginalAssets(self):
        return self.original_assets

    def getColumn(self, columnName) -> dict:
        '''
        获取资产的某个字段下的内容
        :param columnName:
        :return:
        '''
        for k, v in self.allPluginInfo:
            columnDict = v['columnDict']
            if columnName in columnDict.values():
                tableName = v['tableName']
                with PostgresConnectionContextManager() as cur:
                    # 需要修改
                    cur.execute('SELECT ' + columnName + ' FROM ' + tableName + ' WHERE id=%s', (self.id,))
                    a = cur.fetchone()
                    return a[0]

    def getPluginNameByColumnName(self, columnName) -> str:
        '''
        通过字段名获取插件名
        :param columnName:
        :return:
        '''
        for k, v in self.allPluginInfo.items():
            columnDict = v['columnDict']
            if columnName in columnDict.keys():
                return k

    def setCell(self, cloName, cell: Union[BaseElement, List[BaseElement]]):
        '''
        设置资产的某个字段下的内容
        :param cloName:
        :param cell:
        :return:
        '''
        pluginName = self.getPluginNameByColumnName(cloName)
        rowManager = RowManager(pluginName, self.id)
        if isinstance(cell, list):
            rowManager.cellListSet(cloName, cell)
        else:
            rowManager.cellSet(cloName, cell)
        rowManager.submitRow(cloName)

    def getCell(self, cloName):
        '''
        获取资产的某个字段下的内容
        :param cloName:
        :return:
        '''
        pluginName = self.getPluginNameByColumnName(cloName)
        rowManager = RowManager(pluginName, self.id)
        return rowManager.cellGet(cloName)

    def addCell(self, cloName, cell: BaseElement):
        '''
        添加资产的某个字段下的内容
        :param cloName:
        :param cell:
        :return:
        '''
        pluginName = self.getPluginNameByColumnName(cloName)
        rowManager = RowManager(pluginName, self.id)
        rowManager.cellAdd(cloName, cell)
        rowManager.submitRow(cloName)

    def clearCell(self, cloName):
        '''
        清空资产的某个字段下的内容
        :param cloName:
        :return:
        '''
        pluginName = self.getPluginNameByColumnName(cloName)
        rowManager = RowManager(pluginName, self.id)
        rowManager.cellClear(cloName)
        rowManager.submitRow(cloName)


if __name__ == '__main__':
    a = RedisMixin().redis_db_service.hgetall('plugin')
    for k, v in a.items():
        print(k, json.loads(v))
