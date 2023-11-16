from dataclasses import dataclass, field, fields
from type.enums import TAG_SIZE, TAG_THEME, TAG_ROUND, TEXT_SIZE, TEXT_TYPE, TEXT_TAG, TOOL_TIP_THEME, POPOVER_THEME, ALERT_TYPE, ALERT_THEME, NOTIFICATION_TYPE, NOTIFICATION_POS
from typing import List, Union


@dataclass
class BaseElement:
    #elementName属性为继承的子类的类名
    content: str
    elementType: str = field(default='')

    def __post_init__(self):
        self.elementName = self.__class__.__name__


    def serialize(self):
        # 遍历每个属性的值
        bak = self.__dict__.copy()
        for f in vars(self):
            if isinstance(self.__dict__[f], BaseElement):
                self.__dict__[f] = self.__dict__[f].serialize()
        tmp = self.__dict__.copy()
        self.__dict__ = bak
        return tmp

    def unserialize(self, data):
        self.__dict__ = data
        return self







@dataclass
class Tag(BaseElement):
    '''
    TODO:添加枚举类
    '''

    size: str = field(default=TAG_SIZE.SMALL.value)  # small default large
    theme: str = field(default=TAG_SIZE.DEFAULT.value)  # dark light plain
    round: bool = field(default=TAG_ROUND.DEFAULT.value)
    hover: Union[None,BaseElement]= field(default=None)
    click: Union[None,BaseElement]= field(default=None)
    elementType: str = field(default='Tag')




@dataclass
class Text(BaseElement):
    size: str = field(default=TEXT_SIZE.SMALL)  # small default large
    type: Union[str, None] = field(default=TEXT_TYPE.DEFAULT.value)  # primary success info warning danger
    tag: Union[str, None] = field(default=TEXT_TAG.NONE.value)  # bold del marked
    hover: Union[None,BaseElement]= field(default=None)
    click: Union[None,BaseElement]= field(default=None)
    elementType: str = field(default='Text')


@dataclass
class Image(BaseElement):
    width: Union[str, None] = field(default=None)
    height: Union[str, None] = field(default=None)
    elementType: str = field(default='Image')







@dataclass
class ToolTip(BaseElement):
    '''
    悬浮消息
    '''
    multipleLines: bool = field(default=False)
    theme: str = field(default=TOOL_TIP_THEME.LIGHT.value)
    placement: str = field(default=TOOL_TIP_THEME.DEFAULT.value)
    elementType: str = field(default='ToolTip')



@dataclass
class Popover(BaseElement):
    '''
    弹出气泡
    '''
    title: str = field(default='')
    theme: str = field(default=POPOVER_THEME.LIGHT.value)
    placement: str = field(default=POPOVER_THEME.DEFAULT.value)
    elementType: str = field(default='Popover')




@dataclass
class Alert(BaseElement):
    '''
    弹出提示
    '''
    type: str = field(default=ALERT_TYPE.INFO.value)
    theme: str = field(default=ALERT_THEME.DEFAULT.value)
    showIcon: bool = field(default=False)
    center: bool = field(default=False)
    elementType: str = field(default='Alert')



@dataclass
class Notification(BaseElement):
    '''
    通知
    '''
    title: str = field(default='')
    autoClose: bool = field(default=True)
    type: str = field(default=NOTIFICATION_TYPE.INFO.value)
    pos: str = field(default=NOTIFICATION_POS.DEFAULT.value)
    elementType: str = field(default='Notification')


if __name__ == '__main__':
    #测试element的序列化和反序列化
    a = Tag(content='test')
    print(a)
