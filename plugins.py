import abc
from typing import List,Type
from plugins.abstractPlugin import AbstractPlugin
import os,importlib
plugins: List[Type['AbstractPlugin']] = []

plugins_dir = 'plugins'

#plugins文件夹下有插件文件夹，插件文件夹下有plugin.py，plugin.py中有插件类，插件类名与插件文件夹同名，遍历plugins文件夹全部导入插件类
for plugin_dir in os.listdir(plugins_dir):
    if os.path.isdir(os.path.join(plugins_dir, plugin_dir)):
        plugin_file = os.path.join(plugins_dir, plugin_dir, 'plugin.py')
        if os.path.isfile(plugin_file):
            plugin_module = importlib.import_module('plugins.' + plugin_dir + '.plugin')
            plugin_class = getattr(plugin_module, plugin_dir)
            plugins.append(plugin_class)

print(plugins)
for i in plugins:
    a = i()
    a.onLoad()



