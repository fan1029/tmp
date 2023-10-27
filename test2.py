class T():

    def __init__(self, x, y, c):
        self.x = x
        self.y = y
        self.c = c
        # self.c = f2

    def say(self):
        print('say' + str(self.x) + str(self.y))

    def getVar(self):
        return vars(self)


def hello():
    print('hello')