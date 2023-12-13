import time
import queue
from utils.sqlHelper import PostgresConnectionContextManager
import json
from utils.redis_manager import RedisMixin
import datetime


class Notify(RedisMixin):

    def addToMsgQueue(self, msg):
        '''
        跨进程，无法共享空间 改为redis队列
        :param msg:
        :return:
        '''
        self.redis_db_service.lpush('notify', json.dumps(msg))

    def __init__(self, notifier):
        self.notifier = notifier

    def setToDB(self, msgType, message):
        with PostgresConnectionContextManager() as cur:
            cur.execute('INSERT INTO notify (notifier, type, message) VALUES (%s,%s,%s)',
                        (self.notifier, msgType, json.dumps(message)))

    def info(self, info, msgType="tmp", title='', displayType="ToolTip"):
        message = {"title": title, "content": info, "type": "info", "displayType": displayType,
                   "notifier": self.notifier,
                   "time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        self.addToMsgQueue(message)
        self.setToDB(msgType, message)

    def waring(self, waring, msgType="tmp", title='', displayType="ToolTip"):
        message = {"title": title, "content": waring, "type": "waring", "displayType": displayType,
                   "notifier": self.notifier,
                   "time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        self.addToMsgQueue(message)
        self.setToDB(msgType, message)

    def error(self, error, msgType="tmp", title='', displayType="ToolTip"):
        message = {"title": title, "content": error, "type": "error", "displayType": displayType,
                   "notifier": self.notifier,
                   "time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        self.addToMsgQueue(message)
        self.setToDB(msgType, message)

    def high(self, high, msgType="tmp", title='', displayType="ToolTip"):
        message = {"title": title, "content": high, "type": "high", "displayType": displayType,
                   "notifier": self.notifier,
                   "time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        self.addToMsgQueue(message)
        self.setToDB(msgType, message)

    def medium(self, medium, msgType="tmp", title='', displayType="ToolTip"):
        message = {"title": title, "content": medium, "type": "medium", "displayType": displayType,
                   "notifier": self.notifier,
                   "time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        self.addToMsgQueue(message)
        self.setToDB(msgType, message)

    def low(self, low, msgType="tmp", title='', displayType="ToolTip"):
        message = {"title": title, "content": low, "type": "low", "displayType": displayType, "notifier": self.notifier,
                   "time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        self.addToMsgQueue(message)
        self.setToDB(msgType, message)


class NotifyMixin():
    pluginNameZh = ''

    @property
    def notifier(self):
        return Notify(self.pluginNameZh)


if __name__ == '__main__':
    notify = Notify('test', 1)
    notify.info('test')
    # notify.waring('test',msgType='permanent')
    time.sleep(1)
    notify.error('test')
    # print(notify.getNotify())
    time.sleep(1)
    # print(notify.getNotify('permanent'))
