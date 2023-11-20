from dataclasses import dataclass, field, fields, is_dataclass, asdict
from type.enums import SIZE, TAG_THEME, TAG_ROUND, SIZE, TEXT_TYPE, TEXT_TAG, TOOL_TIP_THEME, POPOVER_THEME, ALERT_TYPE, \
    ALERT_THEME, NOTIFICATION_TYPE, NOTIFICATION_POS
from typing import List, Union
import json


@dataclass
class Base:

    def serializeJson(obj):
        if is_dataclass(obj):
            return asdict(obj)
        return obj

    def toDict(self):
        # 遍历每个属性的值
        return asdict(self)

    @staticmethod
    def from_dict(self, data):
        self.__dict__ = data
        return self


@dataclass
class BaseElement(Base):
    # elementName属性为继承的子类的类名
    content: str
    elementType: str = field(init=False)

    def __post_init__(self):
        self.elementType = self.__class__.__name__

    @classmethod
    def from_dict(cls, data):
        data.pop('elementType', None)
        return cls(**data)


@dataclass
class TagAttribute(Base):
    size: str = field(default=SIZE.SMALL.value)  # small default large
    theme: str = field(default=TAG_THEME.DEFAULT.value)  # dark light plain
    round: bool = field(default=TAG_ROUND.DEFAULT.value)


@dataclass
class Action(Base):
    hover: Union[None, BaseElement] = field(default=None)
    click: Union[None, BaseElement] = field(default=None)


@dataclass
class Tag(BaseElement):
    '''
    TODO:添加枚举类
    '''

    # size: str = field(default=SIZE.SMALL.value)  # small default large
    # theme: str = field(default=SIZE.DEFAULT.value)  # dark light plain
    # round: bool = field(default=TAG_ROUND.DEFAULT.value)
    attribute: TagAttribute = field(default=TagAttribute())
    action: Action = field(default=Action())
    # hover: Union[None,BaseElement]= field(default=None)
    # click: Union[None,BaseElement]= field(default=None)
    # elementType: str = field(default='Tag')


@dataclass
class TextAttribute(Base):
    size: str = field(default=SIZE.SMALL.value)  # small default large
    type: Union[str, None] = field(default=TEXT_TYPE.DEFAULT.value)  # primary success info warning danger
    tag: Union[str, None] = field(default=TEXT_TAG.NONE.value)  # bold del marked


@dataclass
class Text(BaseElement):
    # size: str = field(default=SIZE.SMALL)  # small default large
    # 1.type: Union[str, None] = field(default=TEXT_TYPE.DEFAULT.value)  # primary success info warning danger
    # tag: Union[str, None] = field(default=TEXT_TAG.NONE.value)  # bold del marked
    attribute: TextAttribute = field(default=TextAttribute())
    action: Action = field(default=Action())
    # hover: Union[None,BaseElement]= field(default=None)
    # click: Union[None,BaseElement]= field(default=None)
    # elementType: str = field(default='Text')

@dataclass
class ImageAttribute(Base):
    width: Union[str, None] = field(default=None)
    height: Union[str, None] = field(default=None)
@dataclass
class Image(BaseElement):
    action: Action = field(default=Action())
    # elementType: str = field(default='Image')


@dataclass
class EL_TableAttribute(Base):
    header: list
    stripe: bool = field(default=False)
    border: bool = field(default=False)
    size: str = field(default=SIZE.SMALL.value)
    fit: bool = field(default=True)
    showHeader: bool = field(default=True)
    max_height: str = field(default='150 px')


# @dataclass
# class Table(BaseElement):
#     '''
#     表格
#     '''
#
#     # header: list
#     content: str = field(init=False)
#     attribute: TableAttribute = field(default=TableAttribute())
#
#     def __post_init__(self):
#         super().__post_init__()
#         self.content = ''



@dataclass
class Row(BaseElement):
    '''
    表格行
    '''
    # elementType: str = field(default='Row')
    content: list
    action: Action = field(default=Action())


############ACTION############
@dataclass
class ToolTipAttribute(Base):
    multipleLines: bool = field(default=False)
    theme: str = field(default=TOOL_TIP_THEME.LIGHT.value)
    placement: str = field(default=TOOL_TIP_THEME.DEFAULT.value)


@dataclass
class ToolTip(BaseElement):
    '''
    悬浮消息
    '''
    attribute: ToolTipAttribute = field(default=ToolTipAttribute())
    # multipleLines: bool = field(default=False)
    # theme: str = field(default=TOOL_TIP_THEME.LIGHT.value)
    # placement: str = field(default=TOOL_TIP_THEME.DEFAULT.value)
    # elementType: str = field(default='ToolTip')


@dataclass
class PopoverAttribute(Base):
    theme: str = field(default=POPOVER_THEME.LIGHT.value)
    placement: str = field(default=POPOVER_THEME.DEFAULT.value)


@dataclass
class Popover(BaseElement):
    '''
    弹出气泡
    '''
    title: str = field(default='')
    attribute: PopoverAttribute = field(default=PopoverAttribute())
    # theme: str = field(default=POPOVER_THEME.LIGHT.value)
    # placement: str = field(default=POPOVER_THEME.DEFAULT.value)
    # elementType: str = field(default='Popover')


@dataclass
class AlertAttribute(Base):
    type: str = field(default=ALERT_TYPE.INFO.value)
    theme: str = field(default=ALERT_THEME.DEFAULT.value)
    showIcon: bool = field(default=False)
    center: bool = field(default=False)


@dataclass
class Alert(BaseElement):
    '''
    弹出提示
    '''
    attribute: AlertAttribute = field(default=AlertAttribute())
    # type: # str = field(default=ALERT_TYPE.INFO.value)
    # theme: str = field(default=ALERT_THEME.DEFAULT.value)
    # showIcon: bool = field(default=False)
    # center: bool = field(default=False)
    # elementType: str = field(default='Alert')


@dataclass
class NotificationAttribute(Base):
    autoClose: bool = field(default=True)
    type: str = field(default=NOTIFICATION_TYPE.INFO.value)
    pos: str = field(default=NOTIFICATION_POS.DEFAULT.value)


@dataclass
class Notification(BaseElement):
    '''
    通知
    '''
    title: str = field(default='')
    attribute: NotificationAttribute = field(default=NotificationAttribute())
    # autoClose: bool = field(default=True)
    # type: # str = field(default=NOTIFICATION_TYPE.INFO.value)
    # pos: str = field(default=NOTIFICATION_POS.DEFAULT.value)
    # elementType: str = field(default='Notification')


if __name__ == '__main__':
    # 测试element的序列化和反序列化
    # c = Tag(content='i', action=Action(click=Popover(content='i', title='test')))
    # c = BaseElement('2')
    # c = Text('123123123123123')
    a = BaseElement('123123123123123')
    c = asdict(a)
    a2 = BaseElement.from_dict(c)