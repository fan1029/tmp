from lib.common import is_basic_type


class TableBase:

    def passs(self):
        pass

    # def to_dict(self):
    #     result = {}
    #     for key, value in self.__dict__.items():
    #         #如果type(value)为list
    #         if type(value) == list:
    #             if not value:
    #                 result[key] = value
    #             else:
    #
    #
    #
    #
    #         # if is_basic_type(value):
    #         #     result[key] = value
    #         # elif isinstance(value, list):
    #         #     result[key] = [v.to_dict() if hasattr(v, 'to_dict') else v for v in value]
    #         # else:
    #         #     result[key] = value.to_dict()
    #     return result