



class LifeCycle():
    instance=None
    funDict={}

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance=super().__new__(cls)
        return cls.instance


    @staticmethod
    def getFun(key):
        return LifeCycle.funDict[key]

    @staticmethod
    def toolInit(fun):

        def wrapper(*args,**kwargs):
            fun(*args,**kwargs)
        LifeCycle.funDict['toolInit'] = wrapper
        return wrapper


    @staticmethod
    def toolRunning(fun):

        def wrapper(*args,**kwargs):
            fun(*args,**kwargs)
        LifeCycle.funDict['toolRunning'] = wrapper
        return wrapper


