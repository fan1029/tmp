from plugins.BasePlugin import BasePlugin
import multiprocessing



class Plugin_screenShot(BasePlugin):
    pluginName = 'screenshot'
    tableName = pluginName + '_table'
    author = 'maple'
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
        return target

    # def startService(self):
    #     from services.screenshot.main import runFromPythonImport
    #     p = multiprocessing.Process(target=runFromPythonImport)
    #     p.start()

    @classmethod
    def onResult(self, url: str, result: dict):
        pass
