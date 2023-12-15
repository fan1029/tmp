from dataclasses import dataclass, field, fields,asdict
from typing import List, Union


@dataclass
class Base:


    # def toDict(self):
    #     return asdict(self)


    def toDict(self):
        # 遍历每个属性的值
        return asdict(self)
        # bak = self.__dict__.copy()
        # for f in vars(self):
        #     if isinstance(self.__dict__[f], Base):
        #         self.__dict__[f] = self.__dict__[f].toDict()
        # tmp = self.__dict__.copy()
        # self.__dict__ = bak
        # return tmp

    def toDataclass(self, data):
        self.__dict__ = data
        return self


@dataclass
class Vulnerability(Base):
    type: str = field(default='0')
    pocs_hosts: dict = field(default_factory=dict)


@dataclass
class Options(Base):
    jumpCDN: bool = field(default=False)
    jumpWAF: bool = field(default=False)
    queue: int = field(default=0)
    random: bool = field(default=False)
    rate: int = field(default=1000)
    pathDict: List[str] = field(default_factory=list)
    jumpDefend: bool = field(default=False)
    portscanmode: int = field(default=0)
    disableMdns: bool = field(default=True)
    disableUpnp: bool = field(default=True)
    CheckHoneyPot: bool = field(default=False)
    enableCrawler: bool = field(default=False)
    crawlerScope: int = field(default=0)
    crawlerConcurrent: int = field(default=5)
    crawlerMaxLinks: int = field(default=50)
    crawlerMaxCrawlLinks: int = field(default=1000)
    connectionSize: int = field(default=50)
    screenshotRDP: bool = field(default=False)
    screenshot: bool = field(default=False)
    deepAnalysis: bool = field(default=False)
    extracthost: bool = field(default=False)
    fofaFetchSubdomainEnabled: bool = field(default=False)
    fofaEmail: str = field(default='')
    fofaKey: str = field(default='')
    fofaFetchSize: int = field(default=100)
    pingFirst: bool = field(default=False)
    pingCheckSize: int = field(default=10)
    pingConcurrent: int = field(default=2)
    pingSendCount: int = field(default=2)
    defaultUserAgent: str = field(default='')
    defaultDeepAnalysisCheckString: str = field(default='')
    enableSutraCloud: bool = field(default=False)
    enableSutraQueryJson: bool = field(default=False)
    socketTimeout: int = field(default=3)
    retryTimes: int = field(default=0)
    checkAliveMode: int = field(default=1)
    isEmptyScan: bool = field(default=False)


@dataclass
class PluginInfo(Base):
    plugin_name: str
    process_num: int
    thread_num: int
    columnPage: bool
    singlePage: bool
    infoPage: bool


@dataclass
class GobyAsset(Base):
    ips: List[str]
    ports: Union[str, List[str]]

    def __post_init__(self):
        # 将传入的列表类型的端口以,为间隔变为字符串
        if isinstance(self.ports, list):
            self.ports = ','.join(self.ports)


@dataclass
class ScanModel(Base):
    '''
    {"taskName":"","asset":{"ips":["47.106.90.142"],"ports":"21,22,23,25,53,U:53,U:69,80,81,U:88,110,111,U:111,123,U:123,135,U:137,139,U:161,U:177,389,U:427,443,445,465,500,515,U:520,U:523,548,623,U:626,636,873,902,1080,1099,1433,U:1434,1521,U:1604,U:1645,U:1701,1883,U:1900,2049,2181,2375,2379,U:2425,3128,3306,3389,4730,U:5060,5222,U:5351,U:5353,5432,5555,5601,5672,U:5683,5900,5938,5984,6000,6379,7001,7077,8080,8081,8443,8545,8686,9000,9001,9042,9092,9200,9418,9999,11211,U:11211,27017,U:33848,37777,50000,50070,61616","blackIps":[]},"vulnerability":{"type":"0","pocs_hosts":{}},"options":{"jumpCDN":true,"jumpWAF":false,"queue":0,"random":true,"rate":200,"pathDict":["/adminer/","/arcgis/","/axis2/","/axis/","/druid/","/uis/","/imc/","/manager/","/minio/login","/nacos/","/phpmyadmin/","/pma/","/swagger-ui.html","/swagger/","/api/docs/","/console/","/webroot/decision/","/harbor/","/xxl-job/","/xxl-job-admin/","/xxl/","/wui/","/smartbi/","/webroot/decision/","/xxl-job/","/xxl-job-admin/","/xxl/","/admin/","/login/","/mail/","/client/","/blog/","/old/","/email/","/office/","/oa/","/crm/","/stack/","/dashboard/","/cms/","/news/","/user/","/member/","/forum/","/mobile/","/app/","/home/","/cas/","/portal/","/sys/","/wiki/","/im/","/spaces/","/homepage/","/default/","/Page/"],"jumpDefend":false,"portscanmode":0,"disableMdns":true,"disableUpnp":true,"CheckHoneyPot":false,"enableCrawler":false,"crawlerScope":0,"crawlerConcurrent":5,"crawlerMaxLinks":50,"crawlerMaxCrawlLinks":1000,"connectionSize":50,"screenshotRDP":false,"screenshot":false,"deepAnalysis":false,"extracthost":false,"fofaFetchSubdomainEnabled":false,"fofaEmail":"","fofaKey":"","fofaFetchSize":100,"pingFirst":false,"pingCheckSize":10,"pingConcurrent":2,"pingSendCount":2,"defaultUserAgent":"","defaultDeepAnalysisCheckString":"","enableSutraCloud":false,"enableSutraQueryJson":false,"socketTimeout":3,"retryTimes":0,"checkAliveMode":1,"isEmptyScan":false,"fofaDataSourceMode":false}}
    将上面的json转为类属性
    '''
    taskName: str
    asset: GobyAsset
    vulnerability: Vulnerability
    options: Options

    # def serialize(self):
    #     # 遍历每个属性的值
    #     for f in vars(self):
    #         if isinstance(self.__dict__[f], Base):
    #             self.__dict__[f] = self.__dict__[f].serialize()
    #     return self.__dict__


@dataclass
class OrderAssetSearch(Base):
    vulnerabilities: str = field(default='desc')
    assets: str = field(default='desc')


@dataclass
class PageAssetSearch(Base):
    page: int = field(default=1)
    size: int = field(default=10)


@dataclass
class OptionsAssetSearch(Base):
    # "options":{"order":{"vulnerabilities":"desc","assets":"desc"},"page":{"page":1,"size":20}}
    order: OrderAssetSearch = field(default=OrderAssetSearch())
    page: PageAssetSearch = field(default=PageAssetSearch())


@dataclass
class AssetSearchModel(Base):
    query: str
    options: OptionsAssetSearch = field(default=OptionsAssetSearch())

    # def serialize(self):
    #     # 遍历每个属性的值
    #
    #     for f in vars(self):
    #         if isinstance(self.__dict__[f], Base):
    #             self.__dict__[f] = self.__dict__[f].serialize()
    #     return self.__dict__





@dataclass
class GobyScanResult_Ip(Base):
    port: str
    baseProtocol: str


@dataclass
class GobyScanResult_ip(Base):
    ip: str
    mac: str
    os: str
    hostname: str
    ipTag: ""
    ports: dict
    protocols: dict
    tags: dict
    vulnerabilities: dict
    screenshots: str
    favicons: str
    hostname: List[str]


@dataclass
class GobyScanResult(Base):
    ips: List[GobyScanResult_ip]


if __name__ == '__main__':
    # 构造以个ScanModel的例子

    a = ScanModel(
        taskName='test',
        asset=GobyAsset(
            ips=['1.1.1.1'],
            ports=['80', '443']
        ),
        vulnerability=Vulnerability(
            type='0',
            pocs_hosts={}
        ),
        options=Options(
            jumpCDN=True,
            jumpWAF=False,
            queue=0,
            random=True,
            rate=50))
    print(a)
    c = AssetSearchModel('123')
    print(c)
    print(c.toDict())
    print(c)
