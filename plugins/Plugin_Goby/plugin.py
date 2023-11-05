from ..abstractPlugin import AbstractPlugin

def run_function():
    Plugin_Goby


class Plugin_Goby(AbstractPlugin):


    def __init__(self):
        AbstractPlugin.__init__(self)
        self.pluginName = 'Plugin_Goby'
        self.processNum = 1
        self.threadNum = 1
        self.hasMoreInfoPage = True
        self.hasColumn = True
        # self.columns = [
        #     {
        #         "type": "tag",
        #         "label": "asset_tag",
        #         "max_width": 0,
        #         "column_name": "资产标签"
        #     },
        #     {
        #         "type": "tag",
        #         "label": "vul_tag",
        #         "max_width": 0,
        #         "column_name": "漏洞"
        #     },
        #     {
        #         "type": "text",
        #         "label": "portInfo",
        #         "max_width": 0,
        #         "column_name": "port"
        #     }
        # ]
        self.MoreInfoPageContent = None
        self.perUrlTimeOut = None

    def say(self):
        print(1)
