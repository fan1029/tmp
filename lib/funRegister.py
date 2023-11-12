import pickle


# 使用funRegister.getFunList()获取注册器中的函数列表
# 使用funRegister.getFun(funName)获取指定函数
# 使用funRegister.clear()清空注册器
class FunRegister():
    __instance = None
    __funList = {}

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(FunRegister, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        pass

    def getFunList(self):
        return self.__funList

    def getFun(self, funName):
        return self.__funList[funName]

    def clear(self):
        self.__funList.clear()

    def __call__(self, funName):
        def wrapper(func):
            # self.__funList[funName] = func

            def inner(obj):  # 序列化对象数据处理
                # obj = kwargs.get('obj')
                if obj:
                    obj = pickle.loads(bytes.fromhex(obj))
                    obj.onRemoteNew()
                return func(obj)

            self.__funList[funName] = inner
            return inner

        return wrapper
