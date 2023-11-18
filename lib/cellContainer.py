import json
from typing import List
from type.elements import Tag, Text, Image, Row, TableAttribute, TextAttribute, TagAttribute, ImageAttribute
from copy import deepcopy
from abc import ABC, abstractmethod
from dataclasses import asdict, is_dataclass


class Container(ABC):
    def __init__(self):
        self.className = self.__class__.__name__
        self.elementType = ''
        pass

    @abstractmethod
    def set(self, data):
        pass

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def add(self, data):
        pass

    # def serialize(self):
    #     return json.dumps(self.__dict__)
    # def toDict(self):
    #     # 遍历每个属性的值
    #     return asdict(self)
    #     # bak = self.__dict__.copy()
    #     # for f in vars(self):
    #     #     if isinstance(self.__dict__[f], Container):
    #     #         self.__dict__[f] = self.__dict__[f].toDict()
    #     # tmp = self.__dict__.copy()
    #     # self.__dict__ = bak
    #     # return tmp
    def toJson(self):
        pass

    @staticmethod
    def from_dict(data):
        pass


class TextContainer(Container):
    def __init__(self, TextStyle: TextAttribute = TextAttribute()):
        super().__init__()
        self.elementType = 'Text'
        self.style = TextStyle
        self.values = []

    def get(self):
        return self.values

    def set(self, text: Text):
        self.clear()
        self.add(text)
        pass

    def clear(self):
        self.values = []

    def add(self, text: Text):
        self.values.append(text)

    def toJson(self):
        tmp = self.__dict__
        c = deepcopy(tmp['values'])
        s = deepcopy(tmp['style'])
        tmp['values'] = [i.toDict() for i in c]
        tmp['style'] = s.toDict()
        print(tmp)
        return json.dumps(tmp)

    @staticmethod
    def from_dict(data):
        if type(data) == str:
            data = json.loads(data)
        # textStyle =
        values = [Text.from_dict(i) for i in data['values']]
        tmp = TextContainer(TextAttribute(**data['style']))
        tmp.values = values
        return tmp


class TagContainer(Container):
    def __init__(self, TagStyle: TagAttribute = TagAttribute()):
        super().__init__()
        self.values: List[Tag] = []
        self.style = TagStyle
        self.elementType = 'Tag'

    def get(self):
        return self.values

    def set(self, tag: Tag):
        self.clear()
        self.add(tag)

    def clear(self):
        self.values = []

    def add(self, tag: Tag):
        self.values.append(tag)

    def toJson(self):
        tmp = self.__dict__
        c = deepcopy(tmp['values'])
        v = deepcopy(tmp['style'])
        tmp['values'] = [i.toDict() for i in c]
        tmp['style'] = v.toDict()
        return json.dumps(tmp)

    @staticmethod
    def from_dict(data):
        if type(data) == str:
            data = json.loads(data)
        tmp = TagContainer(TagAttribute(**data['style']))
        tmp.values = [Tag.from_dict(i) for i in tmp.values]
        return tmp


class ImageContainer(Container):
    def __init__(self, ImageStyle: ImageAttribute = ImageAttribute()):
        super().__init__()
        self.values = []
        self.style = ImageStyle
        self.elementType = 'Image'

    def get(self):
        return self.values

    def set(self, image: Image):
        self.clear()
        self.add(image)

    def clear(self):
        self.values = []

    def add(self, image: Image):
        self.values.append(image)

    def toJson(self):
        tmp = self.__dict__
        c = deepcopy(tmp['values'])
        v = deepcopy(tmp['style'])
        tmp['values'] = [i.toDict() for i in c]
        tmp['style'] = v.toDict()
        return json.dumps(tmp)

    @staticmethod
    def from_dict(data):
        if type(data) == str:
            data = json.loads(data)
        tmp = ImageContainer(ImageAttribute(**data['style']))
        tmp.values = [Image.from_dict(i) for i in tmp.values]
        return tmp


class TableContainer(Container):
    '''
    表格容器
    '''

    def __init__(self, tableStyle: TableAttribute = TagAttribute()):
        super().__init__()
        self.values = []
        self.elementType = 'Table'
        self.style = tableStyle

    def get(self):
        return self.values

    def set(self, row: Row):
        self.clear()
        self.add(row)

    def clear(self):
        self.values = []

    def add(self, row: Row):
        self.values.append(row)

    def toJson(self):
        tmp = self.__dict__
        c = deepcopy(tmp['values'])
        t = deepcopy(tmp['style'])
        tmp['values'] = [i.toDict() for i in c]
        tmp['tableStyle'] = t.toDict()
        return json.dumps(tmp)

    @staticmethod
    def from_dict(data):
        if type(data) == str:
            data = json.loads(data)
        tableStyleTmp = TableAttribute(**data['style'])
        tmp = TableContainer(tableStyleTmp)
        tmp.values = [Row.from_dict(i) for i in tmp.values]
        return tmp


if __name__ == '__main__':
    tagStyle = TagAttribute()
    a = TagContainer(tagStyle)
    a.add(Tag('123123123123123'))
    c = a.toJson()
    a2 = TagContainer.toDataClass(c)
    print(a2)
    # textStyle = TextAttribute()
    # a = TextContainer(textStyle)
    # c = textStyle.toDict()
    #
    # a.add(Text('123123123123123'))
    # c1 = a.toJson()
    # a2 = TextContainer.toDataClass(c1)
    # print(a2)
    # tableStyle = TableAttribute(showHeader=False,header=["test1", "test2"])
    # print(tableStyle.toDict())
    # a = TableContainer(tableStyle)
    # a.set(Row(['1', '2']))
    # print(a.values)
    # c = a.toJson()
    # a2 = a.toDataClass(c)
    # print(a2)
    # c = a.serialize()
    # print(c)
    # a2 = TextElementCell.unserialize(c)
    # print(a2.get())
    # c = Tag('aaaa',theme='dark',round=True)
    # # print(c.__dict__)
    # a = TagElementCell()
    # a.set(c)
    # c = a.serialize()
    # print(c)
    # c = TagElementCell.unserialize(c)
    # print(c.__dict__)
    # aaa = globals()
    # print(aaa)
    # a = TextElementCell()
    # a.set('123123123123123','marked',size='small')
    # a.clear()
    # print(a.serialize())
