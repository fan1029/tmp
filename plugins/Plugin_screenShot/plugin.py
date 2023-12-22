from typing import List

import nb_log

from plugins.BasePlugin import BasePlugin
from core.asset import Asset
from type.elements import Image,Tag
import base64



class Plugin_screenShot(BasePlugin):
    pluginName = 'plugin_screenshot'
    pluginNameZh = '截图插件'
    tableName = pluginName + '_table'
    author = 'maple'
    scanTargetType = ['original_assets']
    version = '1.0'
    description = '截图插件。'
    columnDict = {
        "screen_img": "截图"
    }
    runMode = 0
    postgreSqlTableCreatteSql = f'''
    CREATE TABLE IF NOT EXISTS {tableName} (
        asset character varying(255) NOT NULL,
        screen_img text,
        time timestamp without time zone DEFAULT now()
    );
    '''

    def onLoad(self):
        pass

    def filter(self, target):
        #如果不是http或者https开头的，就加上http
        if not target.startswith('http'):
            target = 'http://' + target
        return target

    def onBeforePerHandle(self, assets: List[Asset]) ->None:
        for asset in assets:
            asset.clearCell('screen_img')
        #清除原始数据

    @classmethod
    def onResult(cls, asset: Asset, result: dict):
        imgData = result.get('data')
        picBytes = base64.b64decode(imgData.encode('utf-8'))
        path = cls.storePicToStatic(picBytes)
        asset.addCell('screen_img', Image(content=path))

