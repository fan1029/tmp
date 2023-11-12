from dataclasses import dataclass, field, fields
from enum import Enum
from typing import List, Union


@dataclass
class BaseElement:
    content: str

    def serialize(self):
        return self.__dict__

    def unserialize(self, data):
        self.__dict__ = data
        return self


class TAG_SIZE(Enum):
    SMALL = 'small'
    DEFAULT = 'default'
    LARGE = 'large'

class TAG_THEME(Enum):
    DARK = 'dark'
    LIGHT = 'light'
    PLAIN = 'plain'
    DEFAULT = ''

class TAG_ROUND(Enum):
    TRUE = True
    FALSE = False
    DEFAULT = False


@dataclass
class Tag(BaseElement):
    '''
    TODO:添加枚举类
    '''
    size: str = field(default=TAG_SIZE.SMALL)  # small default large
    theme: str = field(default=TAG_SIZE.DEFAULT)  # dark light plain
    round: bool = field(default=TAG_ROUND.DEFAULT)
    # hover: bool= field(default=False)

class TEXT_SIZE(Enum):
    SMALL = 'small'
    DEFAULT = 'default'
    LARGE = 'large'

class TEXT_TYPE(Enum):
    PRIMARY = 'primary'
    SUCCESS = 'success'
    INFO = 'info'
    WARNING = 'warning'
    DANGER = 'danger'
    DEFAULT = ''

class TEXT_TAG(Enum):
    BOLD = 'bold'
    DEL = 'del'
    MARKED = 'marked'
    NONE = ''

@dataclass
class Text(BaseElement):
    size: str = field(default=TEXT_SIZE.SMALL)  # small default large
    type: Union[str, None] = field(default=TEXT_TYPE.DEFAULT)  # primary success info warning danger
    tag: Union[str, None] = field(default=TEXT_TAG.NONE)  # bold del marked


@dataclass
class Image(BaseElement):
    width: Union[str, None] = field(default=None)
    height: Union[str, None] = field(default=None)
