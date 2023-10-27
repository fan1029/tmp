from utils import store
from utils.sqlHelper import PostgresConnectionContextManager


class Notify():

    def __init__(self,notifier:str,project_id:str):
        self.notifier = None
        self.project_id = project_id


    def info(self,info):
        message ={"info": info,"type":"info"}
        with PostgresConnectionContextManager() as cur:
            cur.execute('INSERT INTO notify (notifier, type, message,project_id) VALUES (%s,%s,%s,%s)', (self.notifier, 'info', message,self.project_id))


    def waring(self,waring):
        message ={"info": waring,"type":"waring"}
        with PostgresConnectionContextManager() as cur:
            cur.execute('INSERT INTO notify (notifier, type, message,project_id) VALUES (%s,%s,%s,%s)', (self.notifier, 'waring', message,self.project_id))


    def error(self,error):
        message ={"info": error,"type":"error"}
        with PostgresConnectionContextManager() as cur:
            cur.execute('INSERT INTO notify (notifier, type, message,project_id) VALUES (%s,%s,%s,%s)', (self.notifier, 'error', message,self.project_id))

    def highLightRow(self,asset_original,color,project_id,tag_id):
        message={"asset_original":asset_original,
                 "color":color,
                 "project_id":project_id,
                 "tag_id":tag_id,
                 "type":"highLightRow"
                 }
        with PostgresConnectionContextManager() as cur:
            cur.execute('INSERT INTO notify (notifier, type, message,project_id) VALUES (%s,%s,%s,%s)', (self.notifier, 'highLightRow', message,self.project_id))

    def addTag(self,project_id,tag_name,urls:list):
        # todo: addTag
        message={"project_id":project_id,
                 "tag_name":tag_name,
                 "type":"addTag",
                 "urls":urls
                 }
        with PostgresConnectionContextManager() as cur:
            cur.execute('INSERT INTO notify (notifier, type, message,project_id) VALUES (%s,%s,%s,%s)', (self.notifier, 'addTag', message,self.project_id))
