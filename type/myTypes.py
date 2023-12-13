from dataclasses import dataclass, field,asdict,is_dataclass
from typing import  Union
from enum import Enum
from core.cellContainer import Container


@dataclass
class Asset:
    asset_name: str
    asset_type: str
    assetFiltered: str
    original_assets:list
    rowColor: str = 'DEFAULT'
    label: str = ''

    def toDict(self):
        return asdict(self)


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
    container: Union[Container, None] = field(default=None)

