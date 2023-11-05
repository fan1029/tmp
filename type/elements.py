from dataclasses import dataclass, field, fields
from typing import List, Union

@dataclass
class BaseElement:
    content: str
    def serialize(self):
        return self.__dict__

    def unserialize(self, data):
        self.__dict__ = data
        return self

@dataclass
class Tag(BaseElement):
    theme: str = field(default='small')# dark light plain
    round: bool= field(default=False)

@dataclass
class Text(BaseElement):
    size: str = field(default='small')  # small default large
    type: Union[str, None] = field(default='')  # primary success info warning danger
    tag: Union[str, None] = field(default='')  # bold del marked


@dataclass
class Image(BaseElement):
    width: Union[str, None] = field(default=None)
    height: Union[str, None] = field(default=None)