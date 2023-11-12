import json
from typing import List
from type.elements import Tag, Text,Image
from copy import deepcopy
from abc import ABC, abstractmethod


class ElementCell(ABC):
    def __init__(self):
        self.className = self.__class__.__name__
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

    def serialize(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def unserialize(data):
        data = json.loads(data)
        unserializeClass = globals()[data['className']]
        tmp = unserializeClass()
        tmp.__dict__ = data
        return tmp


class TextElementCell(ElementCell):
    def __init__(self):
        super().__init__()
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
        tmp = TextElementCell()
        tmp.__dict__ = data
        tmp.values = [Text('', '', '', '').unserialize(i) for i in tmp.values]
        return tmp


class TagElementCell(ElementCell):
    def __init__(self):
        super().__init__()
        self.values: List[Tag] = []

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
        tmp = TagElementCell()
        tmp.__dict__ = data
        tmp.values = [Tag(content='').unserialize(i) for i in tmp.values]
        return tmp


class ImageElementCell(ElementCell):
    def __init__(self):
        super().__init__()
        self.values=[]

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
    a = TextElementCell()
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
