from utils.sqlHelper import PostgresConnectionContextManager

from typing import List, Type, Union
#写一个数据模型的基类。每个新插件调用此来设置自己表的数据模型，查询，删除，更新等操作都在这里写。
class BaseModel():

    def __init__(self, pluginName: str,tableName:str):
        self.pluginName:str = pluginName.lower()
        self.table_name:str = self.pluginName+'_'+tableName
        self.table_init_script:str = ''
        self.columns:List[str] = []

    def check_table_exists(self):
        with PostgresConnectionContextManager() as db_cursor:
            db_cursor.execute(
                "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema='public' AND table_name=%s)",
                (self.table_name,))
            return db_cursor.fetchone()[0]
    def init_table(self):
        if not self.check_table_exists():
            with PostgresConnectionContextManager() as db_cursor:
                db_cursor.execute(self.table_init_script)


    def getColumns(self):

        with PostgresConnectionContextManager() as db_cursor:
            db_cursor.execute(
                "SELECT column_name FROM information_schema.columns WHERE table_schema='public' AND table_name=%s",
                (self.table_name,))
            a = db_cursor.fetchall()
        for _ in a:
            self.columns.append(_[0])
        return self.columns

    #讲基本的SQL增删查改功能封装到函数之中，方便调用，传参字典规范化where,update,insert等语句，且不允许存在SQL注入







if __name__ == '__main__':
    a = BaseModel('Plugin_Goby','scan')
    print(a.getColumns())

