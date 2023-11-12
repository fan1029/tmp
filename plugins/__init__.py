import importlib
import os
import inspect
from lib.pluginManager import PluginManager
import nb_log


# 遍历当前文件夹下的所有子文件夹导入子文件夹下 的pluginpy中的子文件夹名同名的类与子文件夹名+'_Run'的函数
def importPlugins():
    '''
    自动搜索导入所有子文件夹下的plugin.py中的类，类名与目录同名
    :return:
    '''
    for root, dirs, files in os.walk(os.path.dirname(__file__)):
        for dir in dirs:
            if dir == '__pycache__':
                continue
            try:
                # 导入plugin.py中的类
                module = importlib.import_module('plugins.' + dir + '.plugin')
                for name, obj in inspect.getmembers(module):
                    if name == dir:
                        if inspect.isclass(obj):
                            # 将类注册到插件管理器中
                            nb_log.info('注册插件类：' + dir+' Version:'+obj.version)
                            PluginManager.pluginClassRegister(dir)(obj)
                            nb_log.info(obj.description)
                            nb_log.info(obj.columnDict)
                            continue
                    if name == dir + '_Run':
                        if inspect.isfunction(obj):
                            nb_log.info('注册插件函数：' + dir+'_Run')
                            # 将函数注册到插件管理器中
                            PluginManager.pluginRunFunctionRegister(dir)(obj)

            except Exception as e:
                print(e)
                pass



