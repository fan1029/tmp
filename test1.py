from lib.pluginManager import PluginManager
from plugins import importPlugins

plugin_table = []
importPlugins()
pm = PluginManager()
tableInfoList = pm.getPluginTableList()
tableListUsed = {}
print(tableInfoList)
for _ in tableInfoList:
    tmp = _.popitem()
    tableListUsed[tmp[0]] = list(tmp[1].keys())

# for _ in tableInfoList:
#       item = _.popitem()
#       plugin_table.append(item[0])
#       tmp = item[1]
#       tableListUsed.append({item[0]: list(tmp.keys())})
