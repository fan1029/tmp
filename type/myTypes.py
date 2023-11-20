from dataclasses import dataclass, field,asdict,is_dataclass
from typing import  Union
from enum import Enum
from lib.cellContainer import Container


@dataclass
class Asset:
    assetOriginal: str
    assetFiltered: str
    ip: Union[str, None] = field(default=None)
    port: Union[str, None] = field(default=None)

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

