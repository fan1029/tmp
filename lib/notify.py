import time

from utils.sqlHelper import PostgresConnectionContextManager
import json
import datetime





class Notify():
    '''
    notifier: 通知者名称
    project_id: 项目id
    info: 通知信息
    msgType: 通知类型 tmp:临时通知（下次启动时不会看到）.permanent:永久通知
    displayType: 通知显示类型 ToolTip:悬浮提示框,Popover:弹出框,Alert:弹出提示,Notification:通知 对应element-ui中的样式
    '''

    def __init__(self, notifier: str, project_id: int):
        self.notifier = notifier
        self.project_id = project_id

    def info(self, info, msgType="tmp", displayType="ToolTip"):
        message = {"info": info, "type": "info", "displayType": displayType}
        with PostgresConnectionContextManager() as cur:
            cur.execute('INSERT INTO notify (notifier, type, message,project_id) VALUES (%s,%s,%s,%s)',
                        (self.notifier, msgType, json.dumps(message), self.project_id))

    def waring(self, waring, msgType="tmp", displayType="ToolTip"):
        message = {"info": waring, "type": "waring", "displayType": displayType}
        with PostgresConnectionContextManager() as cur:
            cur.execute('INSERT INTO notify (notifier, type, message,project_id) VALUES (%s,%s,%s,%s)',
                        (self.notifier, msgType, json.dumps(message), self.project_id))

    def error(self, error, msgType="tmp", displayType="ToolTip"):
        message = {"info": error, "type": "error", "displayType": displayType}
        with PostgresConnectionContextManager() as cur:
            cur.execute('INSERT INTO notify (notifier, type, message,project_id) VALUES (%s,%s,%s,%s)',
                        (self.notifier, msgType, json.dumps(message), self.project_id))

    @staticmethod
    def getNotify(msgType=''):
        if not msgType:
            with PostgresConnectionContextManager() as cur:
                # 筛选出时间大于当前时间的type为tmp的通知，和所有的type为permanent的通知
                cur.execute('SELECT * FROM notify WHERE (type=%s and time>=%s) or type=%s',
                            ('tmp', datetime.datetime.now() - datetime.timedelta(seconds=30), 'permanent'))
                return cur.fetchall()
        else:
            if msgType == 'tmp':
                with PostgresConnectionContextManager() as cur:
                    # 筛选出时间大于当前时间-30s 的type为tmp的通知
                    cur.execute('SELECT * FROM notify WHERE type=%s and time>=%s',
                                ('tmp', (datetime.datetime.now() - datetime.timedelta(seconds=30))))
                    return cur.fetchall()
            elif msgType == 'permanent':
                with PostgresConnectionContextManager() as cur:
                    # 筛选出所有的type为permanent的通知
                    cur.execute('SELECT * FROM notify WHERE type=%s',
                                ('permanent',))
                    return cur.fetchall()


if __name__ == '__main__':
    notify = Notify('test', 1)
    notify.info('test')
    # notify.waring('test',msgType='permanent')
    time.sleep(1)
    notify.error('test')
    # print(notify.getNotify())
    time.sleep(1)
    # print(notify.getNotify('permanent'))
