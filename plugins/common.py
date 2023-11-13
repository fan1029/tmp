from typing import List, Type, Union
from utils.store import Store
from utils.utils import md5Encode
from type.types import Asset
from utils.sqlHelper import PostgresConnectionContextManager
import json
import socket


def pluginLock(asset: Asset, pluginName):
    store = Store()
    store.lpush('lock' + md5Encode(asset.assetFiltered), pluginName)


def pluginUnlock(asset: Asset, pluginName):
    store = Store()
    store.lrem('lock' + md5Encode(asset.assetFiltered), 0, pluginName)


def pushUndoQueue(pluginName, asset: Asset):
    store = Store()
    store.lpush('undo' + pluginName, asset.assetFiltered)


def removeUndoQueue(pluginName, asset: Asset):
    store = Store()
    store.lrem('undo' + pluginName, 0, asset.assetFiltered)


def checkAllFinished(pluginName):
    store = Store()
    queueLen = store.llen('undo' + pluginName)
    if queueLen == 0:
        return True
    else:
        return False


def getComputerName():
    '''
    获取本地计算机名称
    :return:
    '''
    return socket.gethostname()


def getAssetOriginal(pluginName: str, assetFiltered: str) -> List[str]:
    '''
    根据组件名获取资产过滤前的原资产名
    :param pluginName:
    :param assetFiltered:
    :return:
    '''
    # 先从redis中读取
    pluginName = pluginName.lower()
    store = Store()
    assetOriginal = store.hget('asset_map' + pluginName, assetFiltered)
    if assetOriginal:
        return json.loads(assetOriginal)
    print('database')
    # 从asset_map表中筛选出asset_filtered=assetFiltered的结果。并取其asset_original数组返回
    with PostgresConnectionContextManager() as cur:
        cur.execute(
            "SELECT asset_original FROM asset_map WHERE asset_filtered=%s AND plugin_name=%s",
            (assetFiltered,
             pluginName))
        rows = cur.fetchone()
        if rows:
            return rows[0]
        else:
            return []

    pass


def registerAsset(pluginName, asset: Asset) -> bool:
    '''
    将资产过滤前后的映射关系保存
    :param pluginName:
    :param asset:
    :return:
    '''
    pluginName = pluginName.lower()
    store = Store()
    with PostgresConnectionContextManager() as cur:
        cur.execute(
            "SELECT asset_filtered FROM asset_map WHERE asset_filtered=%s AND plugin_name=%s AND %s=ANY(asset_original)",
            (asset.assetFiltered,
             pluginName,
             asset.assetOriginal))
        rows = cur.fetchone()
        if rows:
            # 重复资产，不录入
            return False
        cur.execute(
            "SELECT asset_filtered FROM asset_map WHERE asset_filtered=%s AND plugin_name=%s",
            (asset.assetFiltered,
             pluginName))
        rows = cur.fetchone()
        # 如果存在rows则将asset.original添加到该记录的asset_original字段数组内。如果不存在则新添加一个记录
        if rows:
            cur.execute(
                "UPDATE asset_map SET asset_original=array_append(asset_original,%s) WHERE asset_filtered=%s AND plugin_name=%s",
                (asset.assetOriginal,
                 asset.assetFiltered,
                 pluginName))
        else:
            cur.execute(
                "INSERT INTO asset_map (asset_filtered,asset_original,plugin_name) VALUES (%s,%s,%s)",
                (asset.assetFiltered,
                 [
                     asset.assetOriginal],
                    pluginName))
    # 查询一次该条记录，用hash表记录asset_original和asset_filtered的对应关系存入redis
    with PostgresConnectionContextManager() as cur:
        cur.execute(
            "SELECT asset_filtered,asset_original FROM asset_map WHERE  plugin_name=%s AND asset_filtered=%s",
            (pluginName,
             asset.assetFiltered))
        rows = cur.fetchone()
        store.hset('asset_map' + pluginName, rows[0], json.dumps(rows[1]))


def addAssetOriginalToTable(pluginName, asset_origianl):
    '''
    添加到pluginname_table表中。对于前端表格内数据的更新
    :param asset_origianl:
    :return:
    '''
    pluginName = pluginName.lower()
    with PostgresConnectionContextManager() as cur:
        cur.execute("SELECT asset_original FROM " + pluginName +
                    "_table WHERE asset_original=%s", (asset_origianl,))
        rows = cur.fetchone()
        if rows:
            return False
        else:
            cur.execute(
                "INSERT INTO " +
                pluginName +
                "_table (asset_original) VALUES (%s)",
                (asset_origianl,
                 ))
            return True


def submitRow():
    pass


if __name__ == '__main__':
    registerAsset(
        'test',
        Asset(
            'http://www.bai12312311du.c1om',
            'www.baidu.com'))
    print(getAssetOriginal('test', 'www.baidu.com'))


# def registerFreeTimeQueue(pluginName, host, computerName):
#     '''
#     将本地的空闲进程名注册到空闲队列
#     :return:
#     '''
#     for _ in self.host:
#         self.store.lpush('freeTimeQueue_' + self.pluginName + '_' + self.computerName, _)
#
# def removeFreeTimeQueue(self, host):
#     '''
#     将本地的空闲进程名注册到空闲队列
#     :return:
#     '''
#     self.store.lrem('freeTimeQueue_' + self.pluginName + '_' + self.computerName, 0, host)
#
# def addFreeTimeQueue(self, host):
#     '''
#     将本地的空闲进程名注册到空闲队列
#     :return:
#     '''
#     self.store.lpush('freeTimeQueue_' + self.pluginName + '_' + self.computerName, host)
