import importlib
import sys
import nb_log
import inspect
import os
import socket


def regPlugins():
    hostName = socket.gethostname()
    regPluginDict = {}
    importlib.reload(sys)
    for root, dirs, files in os.walk(os.path.dirname(__file__)):
        for dir in dirs:
            if dir != '__pycache__':
                try:
                    module = importlib.import_module('services.' + dir + '.main')
                    for name, obj in inspect.getmembers(module):
                        if name == 'reg':
                            obj()
                        if name == 'runFromPythonImport':
                            regPluginDict[dir + '-' + hostName + '-info'] = obj
                            nb_log.info(f'{dir}插件加载成功')
                except Exception as e:
                    print(e)
                    continue
    return regPluginDict
