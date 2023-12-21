import json
from typing import List
from type.elements import Tag, Text, Image, Row, EL_TableAttribute, TextAttribute, TagAttribute, ImageAttribute
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

    def toJson(self):
        pass

    @staticmethod
    def from_dict(data):
        pass

    # @classmethod
    # def from_dict_by_asset


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

    def to_dict(self):
        tmp = self.__dict__
        c = deepcopy(tmp['values'])
        s = deepcopy(tmp['style'])
        tmp['values'] = [i.toDict() for i in c]
        tmp['style'] = s.toDict()
        return tmp

    def toJson(self):
        # tmp = self.__dict__
        # c = deepcopy(tmp['values'])
        # s = deepcopy(tmp['style'])
        # tmp['values'] = [i.toDict() for i in c]
        # tmp['style'] = s.toDict()
        return json.dumps(self.to_dict())

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

    def to_dict(self):
        tmp = self.__dict__
        c = deepcopy(tmp['values'])
        v = deepcopy(tmp['style'])
        tmp['values'] = [i.toDict() for i in c]
        tmp['style'] = v.toDict()
        return tmp


    def toJson(self):
        # tmp = self.__dict__
        # c = deepcopy(tmp['values'])
        # v = deepcopy(tmp['style'])
        # tmp['values'] = [i.toDict() for i in c]
        # tmp['style'] = v.toDict()
        return json.dumps(self.to_dict())

    @staticmethod
    def from_dict(data):
        if type(data) == str:
            data = json.loads(data)
        tmp = TagContainer(TagAttribute(**data['style']))
        tmp.values = [Tag.from_dict(i) for i in data['values']]
        return tmp


class ImageContainer(Container):
    def __init__(self, ImageStyle: ImageAttribute = ImageAttribute()):
        super().__init__()
        self.values: List[Image] = []
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

    def to_dict(self):
        tmp = self.__dict__
        c = deepcopy(tmp['values'])
        v = deepcopy(tmp['style'])
        tmp['values'] = [i.toDict() for i in c]
        tmp['style'] = v.toDict()
        return tmp

    def toJson(self):
        return json.dumps(self.to_dict())

    @staticmethod
    def from_dict(data):
        if type(data) == str:
            data = json.loads(data)
        tmp = ImageContainer(ImageAttribute(**data['style']))
        tmp.values = [Image.from_dict(i) for i in data['values']]
        return tmp


class TableContainer(Container):
    '''
    表格容器
    '''

    def __init__(self, tableStyle: EL_TableAttribute = TagAttribute()):
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

    def to_dict(self):
        tmp = self.__dict__
        c = deepcopy(tmp['values'])
        t = deepcopy(tmp['style'])
        tmp['values'] = [i.toDict() for i in c]
        tmp['tableStyle'] = t.toDict()
        return tmp


    def toJson(self):
        # tmp = self.__dict__
        # c = deepcopy(tmp['values'])
        # t = deepcopy(tmp['style'])
        # tmp['values'] = [i.toDict() for i in c]
        # tmp['tableStyle'] = t.toDict()
        return json.dumps(self.to_dict())

    @staticmethod
    def from_dict(data):
        if type(data) == str:
            data = json.loads(data)
        tableStyleTmp = EL_TableAttribute(**data['style'])
        tmp = TableContainer(tableStyleTmp)
        tmp.values = [Row.from_dict(i) for i in data['values']]
        return tmp


if __name__ == '__main__':
    tagStyle = TagAttribute()
    a = TagContainer(tagStyle)
    a.add(Tag('123123123123123'))
    c = a.toJson()
    a2 = TagContainer.toDataClass(c)
    print(a2)
