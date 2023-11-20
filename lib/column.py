# This file contains the Column class, which is used to store information about a column in a table.
from typing import Union
from lib.cellContainer import Container
from lib.common import getAllColumnDB, getColumnDB
from lib.cellContainer import TagContainer, TextContainer, ImageContainer, TableContainer
from lib.tableBase import TableBase
from copy import deepcopy


class Column(TableBase):

    def __init__(self, name: str, type: str, edit: bool, sort: bool, hide: bool, label: str, max_width: int,pluginName: str,
                 containerClass: Union[Container, None] = None):
        self.name = name
        self.type = type
        self.edit = edit
        self.sort = sort
        self.hide = hide
        self.label = label
        self.max_width = max_width
        self.pluginName = pluginName
        self._containerClass = containerClass

    def toDict(self):
        #返回不是以__开头的属性
        return {k:v for k,v in self.__dict__.items() if not k.startswith('_')}

    def setContainer(self, container: Container):
        self._containerClass = container

    def __initColumnContainer(self, container: Container):
        self.container = container

    def getContainerClass(self):
        return self._containerClass

    @classmethod
    def initColumnFromDB(cls, pluginName, columnName):
        _ = getColumnDB(pluginName, columnName)
        _ = _[0]
        _.pop('plugin_name')
        containerType = _['type']
        _['containerClass'] = globals()[containerType + 'Container']
        _['pluginName'] = pluginName
        return Column(**_)

    def to_dict(self):
        tmp = deepcopy(self.__dict__)
        del (tmp['_containerClass'])
        return tmp



if __name__ == '__main__':
    a = Column.initColumnFromDB('plugin_goby', 'tag')
    print(a.toDict())
