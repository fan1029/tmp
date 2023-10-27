import time

from funboost import boost, BrokerEnum, get_consumer, ConcurrentModeEnum


class T2():

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def say(self):
        print('哈哈12哈哈' + str(self.x) + str(self.y))


ccc = T2(1, 2)


class T():

    def __init__(self, x, y, c):
        self.x = x
        self.y = y
        self.c = c
        # self.c = f2


    def tmprun(self):
        obj = type(self)
        var = vars(self)
        def tmp():
            obj(**var).say()
        return tmp

    def say(self):
        print('say' + str(self.x) + str(self.y))

    def getVar(self):
        return vars(self)

    @staticmethod
    def a2(var):
        T(**var).say()




# def f2(t):
#     type(t)(**ttt.getVar()).say()

# cls = getattr(module,class_name)
def f3(ttt,name):
    module = importlib.import_module(name)
    class_name = 'T'
    cls = getattr(module,class_name)
    cls(**ttt).say()
# ttt = T(1, 2,3)
# ttt.go()
if __name__ == '__main__':
    # import importlib
    ttt = T(1, 2,3)
    aaa = ttt.tmprun()
    c = boost('test2223131313',broker_kind=BrokerEnum.REDIS_STREAM, concurrent_num=1)(aaa)
    c.push()
    c.consume()
