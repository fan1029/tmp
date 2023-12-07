from lib.common import getAllColumnDB, getAllColumnNameDB, initColumnValueDB, initColumnValueDB_id
from type.myTypes import Asset
from lib.column import Column
from typing import Union, List
from lib.cellContainer import Container
from lib.tableBase import TableBase
from copy import deepcopy


class Row(TableBase):

    def __init__(self, asset_original: str,id:int,original_asset:list,columnList: List[Column]):
        self.id = id
        self.asset_name = asset_original
        self.color = ''
        self.columnList = columnList
        self.original_asset = original_asset
        self.value = {}
        self.initContainerValue()

    def initContainerValue(self):
        '''
        根据column初始化container内的数据
        :return:
        '''
        for _ in self.columnList:
            containerObj = _.getContainerClass()
            tmpData = initColumnValueDB(pluginName=_.pluginName, asset_original=self.asset_name, columnName=_.name)
            if tmpData:
                container = containerObj.from_dict(tmpData[0])
            else:
                container = containerObj()
            self.value[_.name] = container

    def to_dict(self):
        tmp = deepcopy(self.__dict__)
        del(tmp['columnList'])
        for k,v in self.value.items():
            tmp["value"][k] = v.to_dict()
            del tmp["value"][k]['className']
        return tmp