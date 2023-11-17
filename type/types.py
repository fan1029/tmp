from dataclasses import dataclass, field
from typing import  Union
from enum import Enum
from lib.cellContainer import Container


@dataclass
class Asset:
    assetOriginal: str
    assetFiltered: str
    ip: Union[str, None] = field(default=None)
    port: Union[str, None] = field(default=None)

    def serialize(self):
        return self.__dict__


@dataclass
class PluginInfo:
    plugin_name: str
    process_num: int
    thread_num: int
    columnPage: bool
    singlePage: bool
    infoPage: bool
    author: str
    introduction: str




# 单元格数据属性


class Text_Size(Enum):
    small = 'small'
    default = 'default'
    large = 'large'


class Text_Type(Enum):
    primary = 'primary'
    success = 'success'
    info = 'info'
    warning = 'warning'
    danger = 'danger'


class Text_Tag(Enum):
    bold = 'bold'
    del_ = 'del'
    marked = 'marked'


@dataclass
class Text:
    content: str
    size: Text_Size  # small default large
    type: Text_Type  # primary success info warning danger
    tag: Text_Tag  # bold del marked




#############


@dataclass
class Column:
    name: str
    type: str
    edit: bool
    sort: bool
    hide: bool
    label: str
    max_width: int
    value: Union[Container, None] = field(default=None)


@dataclass
class Color:
    # 列出红黄绿蓝白这几种颜色的hex值设置为常量
    red: str = '#FF0000'
    yellow: str = '#FFFF00'
    green: str = '#00FF00'
    blue: str = '#0000FF'
    white: str = '#FFFFFF'
    black: str = '#000000'
    gray: str = '#808080'
    purple: str = '#800080'
    pink: str = '#FFC0CB'
    orange: str = '#FFA500'
    brown: str = '#A52A2A'
    cyan: str = '#00FFFF'
    darkblue: str = '#00008B'
    darkcyan: str = '#008B8B'
    darkgray: str = '#A9A9A9'
    darkgreen: str = '#006400'
    darkorange: str = '#FF8C00'
    darkred: str = '#8B0000'
    darkviolet: str = '#9400D3'
    gold: str = '#FFD700'
    lightblue: str = '#ADD8E6'
    lightcyan: str = '#E0FFFF'
