from functools import wraps


def cached_method_result(fun):
    """方法的结果装饰器,不接受self以外的多余参数，主要用于那些属性类的property方法属性上，配合property装饰器，主要是在pycahrm自动补全上比上面的装饰器好"""

    @wraps(fun)
    def inner(self):
        if not hasattr(fun, 'result'):
            result = fun(self)
            fun.result = result
            fun_name = fun.__name__
            setattr(self.__class__, fun_name, result)
            setattr(self, fun_name, result)
            return result
        else:
            return fun.result

    return inner