from type.types import Asset, Column, Color
from utils.sqlHelper import PostgresConnectionContextManager
from typing import List, Union
from cell import TextElementCell,TagElementCell,ImageElementCell
# from models.cell import ElementCell


class RowManager():

    def __init__(self, pluginName: str, asset: Asset):
        self.pluginName = pluginName.lower()
        self.asset: Asset = asset
        self.color: Union[Color, None] = None
        self.column: List[Column] = []
        self.getAllColumn()

    def getAllColumn(self):
        # 获取所有column_attribute表下plugin_name为self.pluginName的记录,使用row_to_json
        # 将查询到的数据转换为json格式
        with PostgresConnectionContextManager() as db_cursor:
            db_cursor.execute(
                "SELECT row_to_json(t) FROM (SELECT * FROM column_attribute WHERE plugin_name=%s) as t",
                (self.pluginName,))
            a = db_cursor.fetchall()
        # 遍历a中的数据赋值给Column类,将每个新的对象添加到self.column中
        for _ in a:
            _ = _[0]
            _.pop('plugin_name')
            self.column.append(Column(**_))
        print(self.column)
        for i in self.column:
            self.initColumnValue(i)
        return self.column

    @staticmethod
    def getCellType(column: Column):
        return column.type

    def setAsset(self,asset: Asset):
        self.asset = asset

    def getColumn(self,columnName: str):
        for _ in self.column:
            if _.name == columnName:
                return _

    def initColumnValue(self,column: Column):
        with PostgresConnectionContextManager() as db_cursor:
            #inject vul
            db_cursor.execute("SELECT "+column.name+" FROM "+self.pluginName+'_table'+" WHERE asset_original = %s",(self.asset.assetOriginal,))
            a = db_cursor.fetchone()
            if a:
                #反序列化出cell对象
                cellClass = globals()[a[0]['className']]
                column.value = cellClass.unserialize(a[0])
                return column.value
            else:
                #如果没有对应的记录，则初始化一个cell对象
                cellClass = globals()[column.type+'ElementCell']
                column.value = cellClass()
                return column.value

    def cellSet(self,columnName: str,cell):
        column = self.getColumn(columnName)
        column.value.set(cell)

    def cellGet(self,columnName: str):
        column = self.getColumn(columnName)
        return column.value.get()

    def cellClear(self,columnName: str):
        column = self.getColumn(columnName)
        column.value.clear()

    def cellAdd(self,columnName: str,cell):
        column = self.getColumn(columnName)
        column.value.add(cell)

    def submitRow(self,column: Column):
        #将cell对象序列化后提交到数据库
        cellJson = column.value.serialize()
        with PostgresConnectionContextManager() as db_cursor:
            #检查存不存在对应的行，有则更新，没有则添加
            #inject vul
            db_cursor.execute("SELECT * FROM "+self.pluginName+'_table'+" WHERE asset_original = %s",(self.asset.assetOriginal,))
            a = db_cursor.fetchone()
            if a:
                db_cursor.execute("UPDATE "+self.pluginName+'_table'+" SET "+column.name+" = %s WHERE asset_original = %s",(cellJson,self.asset.assetOriginal))
            else:
                db_cursor.execute("INSERT INTO "+self.pluginName+'_table'+" (asset_original,"+column.name+") VALUES (%s,%s)",(self.asset.assetOriginal,cellJson))



if __name__ == '__main__':
    a = RowManager('Plugin_Goby', Asset('http://www.baidu.com', 'http://www.baidu.com'))
    column = a.getColumn('tag')
    c = a.initColumnValue(column)
    print(c.get())
    # from cell import Tag
    # c.add(Tag('aaaa', theme='dark', round=True))
    # a.submitRow(column)


