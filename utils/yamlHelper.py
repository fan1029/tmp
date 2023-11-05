#写一个读取yaml配置文件的类
import yaml
import os



class YamlHelper:
    def __init__(self, yamlf):
        if os.path.exists(yamlf):
            self.yamlf = yamlf
        else:
            raise FileNotFoundError('文件不存在！')
        self._data = None

    @property
    def data(self):
        if not self._data:
            with open(self.yamlf, 'rb') as f:
                self._data = list(yaml.safe_load_all(f))
        return self._data

    def get(self, element, index=0):
        return self.data[index].get(element)

    def get_all(self, element, index=0):
        return self.data[index].get(element)

    def get_all_elements(self, index=0):
        return self.data[index].keys()

    def get_all_elements_by_list(self, index=0):
        return list(self.data[index].keys())

    def get_all_values(self, index=0):
        return self.data[index].values()

    def get_all_values_by_list(self, index=0):
        return list(self.data[index].values())

    def get_all_items(self, index=0):
        return self.data[index].items()

    def get_all_items_by_list(self, index=0):
        return list(self.data[index].items())

    def get_all_elements_and_values(self, index=0):
        return self.data[index]

    def get_all_elements_and_values_by_list(self, index=0):
        return list(self.data[index])

    def get_all_elements_and_values_by_dict(self, index=0):
        return dict(self.data[index])

    def get_all_elements_and_values_by_tuple(self, index=0):
        return tuple(self.data[index])

    def get_all_elements_and_values_by_set(self, index=0):
        return set(self.data[index])

    def get_all_elements_and_values_by_frozenset(self, index=0):
        return frozenset(self.data[index])

    def get_all_elements_and_values_by_zip(self, index=0):
        return zip(self.data[index])

    def get_all_elements_and_values_by_enumerate(self, index=0):
        return enumerate(self.data[index])

