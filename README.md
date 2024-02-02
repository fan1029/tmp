

# 简介

本平台用于在面对大量资产批量扫描时信息整理混乱，攻击人员沟通麻烦的问题。你可以将你的任何扫描工具通过本工具插件化，并将结果进行显示。同时本工具支持分布式运行。测试人员只需在本地开启消费端即可在本机运行指定插件。

**本平台仍然在开发测试之中，实际安装使用过程可能比较麻烦，建议等我完善了再用。**

## 使用效果

![image-20240202205355406](https://github.com/fan1029/tmp/blob/master/README.assets/image-20240202205355406.png?raw=true)

点击资产旁边的小本本调用笔记本功能

![image-20240202220843722](https://github.com/fan1029/tmp/blob/master/README.assets/image-20240202220843722.png?raw=true)

右键一键调用插件，你可以将你喜欢的插件集成进来。

![image-20240202205405586](https://github.com/fan1029/tmp/blob/master/README.assets/image-20240202205405586.png?raw=true)

![image-20240202205434238](https://github.com/fan1029/tmp/blob/master/README.assets/image-20240202205434238.png?raw=true)

中间打开控制面板可以控制各个消费端开启关闭。可以精准控制每台机器上执行什么插件什么任务。

![image-20240202205621767](https://github.com/fan1029/tmp/blob/master/README.assets/image-20240202205621767.png?raw=true)



## 运行

要求 redis  postgresql  python 3.8+

redis要求不能使用低版本(windows上的)  要有支持stream结构的版本

配置去serviceConfig.py里面去改。

运行

main_api.py   后端。  

main_plugin  插件回调端

client_plugin_manager.py  插件消费端

请确保每个插件消费端的网能连接到redis
消费端单独运行要把service放到同目录下 才能调用里面的插件运行



## 如何写插件

由于一个人开发精力有限，并没有集成什么插件，你需要自己去写。每个插件运行后结果将会变成一列显示在主页表格中。

现阶段步骤比较麻烦。

首先关注两个文件夹，其中的插件的作用如下。

plugin    web端用的  用于发布目标信息，预处理目标格式等到pluginService

services   接受任务，运行插件，返回结果

以截图插件为例（plugin/plugin_screenshot/plugin.py）

请继承BasePlugin。详细写法见注释。

```
from typing import List

import nb_log

from plugins.BasePlugin import BasePlugin
from core.asset import Asset
from type.elements import Image,Tag
import base64



class Plugin_screenShot(BasePlugin):
    pluginName = 'plugin_screenshot'   #插件名
    pluginNameZh = '截图插件'  #插件中文名
    tableName = pluginName + '_table'   #插件存表格数据的表名
    author = 'maple'
    scanTargetType = ['original_assets']  
    #扫描类型original_assets指的是表中关联资产对应的多个页面。还有['domain', 'ip']可以选 这个就是单独的一个资产。
    #比如表格中有一个资产为 8.8.8.8  扫描完后他有好几个端口开web服务，那么就会出现在关联资产里面。http://8.8.8.8:8080/ http://8.8.8.8:8000/ 。original_assets就是指的这些资产
    version = '1.0'
    description = '截图插件。'
    columnDict = {
        "screen_img": "截图"   #在前端表格中展示的列名字
    }
    runMode = 0
    postgreSqlTableCreatteSql = f'''   #创建表格的sql语句 ，这边暂时预留的。目前请自己到数据库里面创建。。
    CREATE TABLE IF NOT EXISTS {tableName} (
        asset character varying(255) NOT NULL,
        screen_img text,
        time timestamp without time zone DEFAULT now()
    );
    '''

    def onLoad(self):   #插件第一次被加载的时候会干嘛。web端启动后会加载一次 调用这个方法。没有就不写或者pass
        pass

    def filter(self, target):   #用于对目标过滤的，比如我要写截图插件，肯定要访问网址 这边就是规范数据格式的
        #如果不是http或者https开头的，就加上http
        if not target.startswith('http'):
            target = 'http://' + target
        return target

    def onBeforePerHandle(self, assets: List[Asset]) ->None:  
    #数据准备发送到消息队列给service处理前要干嘛。这边就是清理之前表格里面的数据，把以前的结果清理掉。
        for asset in assets:
            asset.clearCell('screen_img')
        #清除原始数据

    @classmethod
    def onResult(cls, asset: Asset, result: dict):   #  结果回调。扫描任务扫描完后结果会运行这个函数。你可以对结果做处理，吧他添加到表格中
        imgData = result.get('data')
        picBytes = base64.b64decode(imgData.encode('utf-8'))
        path = cls.storePicToStatic(picBytes)
        asset.addCell('screen_img', Image(content=path))    
        #asset类的addCell   第一个传列名 Image表示要显示的是个图片对象这样设置完前端就会显示了


```

### 关于Asset类的一些方法 

addCell  clearCell  setCell这些方法就是对前端你看到的表格的单元格操作的

第二个参数你可以传 

Text (以纯文本显示)  Tag (以标签显示 ) Image(是个图片)





## Service端编写

```
from pluginService.lifeCycleFuntion_manager import LifeCycle
from pluginService.plugin_service import PlguinService

导入这两个
然后初始化以下
service = PlguinService(pluginConfig)
然后实现两个函数  1个是插件启动后初始化的动作 一个是扫描的动作  加上两个装饰器就行
其中运行接受targets参数个config参数。
targets就是发过来的目标
```

![image-20240202215847562](https://github.com/fan1029/tmp/blob/master/README.assets/image-20240202215847562.png?raw=true)





然后编写自己插件的扫描逻辑

```
service.setResult(url, "data:image/png;base64,"+base64.b64encode(res).decode('utf-8'),finish=True)
这个是设置结果，如果finish为TRUE则默认当前资产扫描完毕不为True则表示暂时的结果，还没扫描完，但是现在扫描的内容会同步实时更新到前端
service.reportError('截图出错', [url])
报错的逻辑   里面放出错的资产就行

```

基础属性设置

```
pluginConfig = {
    'pluginName': 'plugin_screenshot',
    'author': 'maple',
    'maxThread': 2,   #最大运行线程
    'pluginType': 2,
    'semaphore': 10
}
```



建立插件表

asset_id作为主键

其他是这个插件有的列名 jsonb格式

![image-20240202220647946](https://github.com/fan1029/tmp/blob/master/README.assets/image-20240202220647946.png?raw=true)