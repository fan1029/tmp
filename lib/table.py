from lib.common import getAllColumnNameDB
from lib.column import Column
from lib.row import Row
from typing import List, Union
from lib.tableBase import TableBase

class Table(TableBase):

    def __init__(self, pluginNameList: List[str]):
        self.column: List[Column] = []
        self.asset_original: List[str] = []
        self.row = []
        self.initColumn(pluginNameList)

    def initColumn(self, pluginNameList: List[str]):
        '''
        获取一个plugin的所有column，根据前端传来的插件名初始化所有哟用到插件的column
        :param pluginName:
        :return:
        '''
        for pluginName in pluginNameList:
            self.initColumnByColumnName(pluginName)

    def initColumnByColumnName(self, pluginName: str):
        '''
        单个插件返回列信息
        :param pluginName:
        :return:
        '''
        columnNameList = getAllColumnNameDB(pluginName)
        for _ in columnNameList:
            _ = _[0]
            self.column.append(Column.initColumnFromDB(pluginName, _['name']))

    def initContainerColumnDict(self):
        containers = {}
        for _ in self.column:
            containers[_.name] = _.getContainerClass()

    def getColumnList(self):
        return self.column

    def addRow(self, row: Row):
        self.asset_original.append(row.asset_original)
        self.row.append(row)


    def generateTable(self):
        returnDict = {"column": [_.to_dict() for _ in self.column],
                      "asset_original": self.asset_original,
                      "rows": [_.to_dict() for _ in self.row]}
        # returnDict = {"column": [_.to_dict() for _ in self.column],
        #               "asset_original": self.asset_original,
        #               "rows": {}}
        # for _ in  self.row:
        #     tmp =_.to_dict()
        #     returnDict['row'][tmp['id']] = tmp
        return returnDict




if __name__ == '__main__':
    pluginNameList = ['plugin_goby']
    table = Table(pluginNameList)
    row = Row("10.1.99.100", table.getColumnList())
    row2 = Row("10.1.72.121", table.getColumnList())
    table.addRow(row)
    table.addRow(row2)
    returnDict = {"column":[_.to_dict() for _ in table.column],
                  "asset_original":table.asset_original,
                  "rows":[_.to_dict() for _ in table.row]}
    print(returnDict)
