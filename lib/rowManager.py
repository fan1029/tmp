from lib.common import submitOneRowDB, submitRowColorDB, getAllColumnDB, initColumnValueDB
from type.myTypes import Asset, Column
from utils.sqlHelper import PostgresConnectionContextManager
from typing import List, Union
from type.elements import BaseElement
from plugins.common import getAssetOriginal
from type.enums import COLOR
from lib.cellContainer import TextContainer, TagContainer, ImageContainer


class RowManagerProxy():
    # 对于同一个pluginName实例化RowManagerProxy时使用单例模式
    _instance = {}

    def __new__(cls, *args, **kwargs):
        # 单例模式
        if args[0] not in cls._instance:
            cls._instance[args[0]] = object.__new__(cls)
        return cls._instance[args[0]]

    def __init__(self, pluginName: str, assetFiltered: str):
        self.assets = []
        self.pluginName = pluginName.lower()
        self.__initAsset(assetFiltered)
        self.rowManagers: List[RowManager] = []
        self.__initRowManager()
        self.tmpRowManager = self.rowManagers[0]

    def __initRowManager(self):
        for _ in self.assets:
            self.rowManagers.append(RowManager(self.pluginName, _))

    def __initAsset(self, asset_filtered):
        res = getAssetOriginal(self.pluginName, asset_filtered)
        if res:
            for _ in res:
                self.assets.append(Asset(_, asset_filtered))

    # 复制RowManager中的所有方法。每次调用时，遍历self.rowManagers，调用对应的方法

    def getColumn(self, columnName: str):

        return self.tmpRowManager.getColumn(columnName)

    def getAllColumn(self):
        return self.tmpRowManager.getAllColumn()

    def getCellType(self, column: Column):
        return self.tmpRowManager.getCellType(column)

    def cellSet(self, columnName: str, cell: BaseElement):
        for _ in self.rowManagers:
            _.cellSet(columnName, cell)

    def cellListSet(self, columnName: str, cellList: List[BaseElement]):
        for _ in self.rowManagers:
            _.cellListSet(columnName, cellList)

    def cellListAdd(self, columnName: str, cellList: List[BaseElement]):
        for _ in self.rowManagers:
            _.cellListAdd(columnName, cellList)

    def cellGet(self, columnName: str):
        return self.tmpRowManager.cellGet(columnName)

    def cellClear(self, columnName: str):
        for _ in self.rowManagers:
            _.cellClear(columnName)

    def rowColorSet(self, color: str):
        for _ in self.rowManagers:
            _.rowColorSet(color)

    def cellAdd(self, columnName: str, cell: BaseElement):
        for _ in self.rowManagers:
            _.cellAdd(columnName, cell)

    def submitRow(self, columnName: str = ''):
        for _ in self.rowManagers:
            _.submitRow(columnName)


class RowManager():
    def __init__(self, pluginName: str, asset: Asset):
        self.pluginName = pluginName.lower()
        self.asset: Asset = asset
        self.color: COLOR = COLOR.DEFAULT
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

    def setAsset(self, asset: Asset):
        self.asset = asset

    def getColumn(self, columnName: str):
        for _ in self.column:
            if _.name == columnName:
                return _

    def initColumnValue(self, column: Column):
            #从pluginName_table表中获取对应的cell对象
            a = initColumnValueDB(self.pluginName, self.asset.assetOriginal,column.name)   #查插件表中对应列的数据
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

    def rowColorSet(self, color: str):
        for i in COLOR:
            if i.name == color:
                if i.value > self.color.value:
                    self.color = i
                    break
                else:
                    break

    def submitRowColor(self):
        asset_original = self.asset.assetOriginal
        color = self.color.name
        submitRowColorDB(asset_original, color)
    def submitOneRow(self, column: Column):
        cellJson = column.container.toJson()
        submitOneRowDB(self.pluginName, self.asset.assetOriginal, column.name, cellJson)
        self.submitRowColor()

    def submitRow(self, columnName: str = ''):

        if columnName:
            column = self.getColumn(columnName)
            self.submitOneRow(column)
        else:
            for _ in self.column:
                self.submitOneRow(_)


if __name__ == '__main__':
    a = RowManager('Plugin_Goby', Asset('10.1.99.100', '10.1.99.100'))
    a.getAllColumn()
    print(a.getColumn('vul'))
    # a = RowManagerProxy('Plugin_Goby', 'www.baidu.com')
