import json
from typing import List
from type.elements import Tag, Text,Image
from copy import deepcopy
from abc import ABC, abstractmethod


class Container(ABC):
    def __init__(self):
        self.className = self.__class__.__name__
        self.elementType=''
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
    def serialize(self):
        # 遍历每个属性的值
        bak = self.__dict__.copy()
        for f in vars(self):
            if isinstance(self.__dict__[f], Container):
                self.__dict__[f] = self.__dict__[f].serialize()
        tmp = self.__dict__.copy()
        self.__dict__ = bak
        return tmp

    @staticmethod
    def unserialize(data):
        data = json.loads(data)
        unserializeClass = globals()[data['className']]
        tmp = unserializeClass()
        tmp.__dict__ = data
        return tmp


class TextContainer(Container):
    def __init__(self):
        super().__init__()
        self.elementType='Text'
        self.values = []
        pass

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

    def serialize(self):
        tmp = self.__dict__
        c = deepcopy(tmp['values'])
        tmp['values'] = [i.serialize() for i in c]
        return json.dumps(tmp)

    @staticmethod
    def unserialize(data):
        if type(data) == str:
            data = json.loads(data)
        tmp = TextContainer()
        tmp.__dict__ = data
        tmp.values = [Text('', '', '', '').unserialize(i) for i in tmp.values]
        return tmp


class TagContainer(Container):
    def __init__(self):
        super().__init__()
        self.values: List[Tag] = []
        self.elementType='Tag'

    def get(self):
        return self.values

    def set(self, tag: Tag):
        self.clear()
        self.add(tag)

    def clear(self):
        self.values = []

    def add(self, tag: Tag):
        self.values.append(tag)

    def serialize(self):
        tmp = self.__dict__
        c = deepcopy(tmp['values'])
        tmp['values'] = [i.serialize() for i in c]
        return json.dumps(tmp)

    @staticmethod
    def unserialize(data):
        if type(data) == str:
            data = json.loads(data)
        tmp = TagContainer()
        tmp.__dict__ = data
        tmp.values = [Tag(content='').unserialize(i) for i in tmp.values]
        return tmp


class ImageContainer(Container):
    def __init__(self):
        super().__init__()
        self.values=[]
        self.elementType='Image'

    def get(self):
        return self.values

    def set(self,image:Image):
        self.clear()
        self.add(image)

    def clear(self):
        self.values=[]

    def add(self,image:Image):
        self.values.append(image)




# class LinkElementCell(ElementCell):
#     def __init__(self):
#         super().__init__()
#         pass
#
#
# class TableElementCell(ElementCell):
#     def __init__(self):
#         super().__init__()
#         pass


if __name__ == '__main__':
    pass
    a = TextContainer()
    a.set('123123123123123')
    print(a)
    print(a.type)
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
