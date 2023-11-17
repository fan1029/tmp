from plugins.Plugin_Goby.gobyTypes import ScanModel, AssetSearchModel
import requests
from psycopg2.extras import Json
import json

from utils.sqlHelper import PostgresConnectionContextManager

# burp0_url = "http://127.0.0.1:8361/api/v1/startScan"
burp0_headers = {"Content-Type": "application/json;charset=UTF-8", "Authorization": "Basic Og==", "Connection": "close"}


def runScan(host: str, scanModel: ScanModel) -> tuple:
    url = "http://" + host + '/api/v1/startScan'
    print(scanModel.toDict())
    res = requests.post(url, headers=burp0_headers, json=scanModel.toDict())
    res = json.loads(res.text)
    if res['statusCode'] == 200:
        return True, res['data']['taskId']
    else:
        return False, res['message']


def checkProgress(host: str, taskId: str) -> tuple:
    url = "http://" + host + '/api/v1/getProgress'
    res = requests.post(url, headers=burp0_headers, json={'taskId': taskId}).json()
    if res['statusCode'] == 200:
        if res['data']['progress'] ==1:
            return False, False
        else:
            return True, res['data']['progress']
    else:
        return False, res['message']


def getStatisticsData(host: str, taskId: str) -> tuple:
    url = "http://" + host + '/api/v1/getStatisticsData'
    res = requests.post(url, headers=burp0_headers, json={'taskId': taskId}).json()
    if res['statusCode'] == 200:
        return True, res['data']
    else:
        return False, res['message']


def assetSearch(host: str, taskId: str) -> tuple:
    url = "http://" + host + '/api/v1/assetSearch'
    searchStr = "taskId=\"" + taskId + "\" && ()"
    searchModel = AssetSearchModel(searchStr)
    res = requests.post(url, headers=burp0_headers, json=searchModel.toDict()).json()
    if res['statusCode'] == 200:
        assetNumber = res['data']['total']['assets']
    else:
        return False, res['message']
    searchModel.options.page.size = assetNumber + 10
    res = requests.post(url, headers=burp0_headers, json=searchModel.toDict()).json()
    if res['statusCode'] == 200:
        if res['data']['ips'] is None:
            return False,False
        else:
            return True, res['data']['ips']
    else:
        return False, res['message']


def stopScan(host: str, taskId: str) -> tuple:
    url = "http://" + host + '/api/v1/stopScan'
    requests.post(url, headers=burp0_headers, json={'taskId': taskId}).json()
    return True, 'success'
    pass


def dataStore(ipAsset: dict):
    '''
    将资产搜索结果存入数据库
    :param assetSearchResult:
    :return:
    '''
    # {"ip":"10.1.72.124","mac":"","os":"","hostname":"elasticsearch.May Parker","honeypot":"0","ipTag":"","ports":[{"port":"123","baseprotocol":"udp"},{"port":"8081","baseprotocol":"tcp"},{"port":"22","baseprotocol":"tcp"},{"port":"9200","baseprotocol":"tcp"},{"port":"8080","baseprotocol":"tcp"}],"protocols":{"10.1.72.124:123":{"port":"123","hostinfo":"10.1.72.124:123","url":"","product":"NTP server","protocol":"ntp","json":"","fid":[""],"products":["NTP server"],"protocols":["ntp"]},"10.1.72.124:22":{"port":"22","hostinfo":"10.1.72.124:22","url":"","product":"OpenSSH|debian-操作系统","protocol":"ssh","json":"","fid":[""],"products":["OpenSSH","debian-操作系统"],"protocols":["ssh"]},"10.1.72.124:8080":{"port":"8080","hostinfo":"10.1.72.124:8080","url":"","product":"Apache-Tomcat|Apache-Web-Server","protocol":"http","json":"","fid":[],"products":["Apache-Tomcat","Apache-Web-Server"],"protocols":["http","web"]},"10.1.72.124:8081":{"port":"8081","hostinfo":"10.1.72.124:8081","url":"","product":"Nginx","protocol":"http","json":"","fid":["ZvJCtGzrqEyHLFflRL595vwXT9k+bh/O"],"products":["Nginx"],"protocols":["http","web"]},"10.1.72.124:9200":{"port":"9200","hostinfo":"10.1.72.124:9200","url":"","product":"Log4j2|Elasticsearch|Java|Linux","protocol":"elastic","json":"","fid":[],"products":["Log4j2","Elasticsearch","Java","Linux"],"protocols":["elastic","web"]}},"tags":[{"rule_id":"17291","product":"NTP server","company":"other","level":"3","category":"Other Support System","parent_category":"Support System","softhard":"0","version":""},{"rule_id":"4531","product":"debian-操作系统","company":"Public Interest, Inc.","level":"2","category":"Operating System","parent_category":"Software System","softhard":"2","version":""},{"rule_id":"7512","product":"OpenSSH","company":"other","level":"3","category":"Other Support System","parent_category":"Support System","softhard":"2","version":""},{"rule_id":"209","product":"Nginx","company":"other","level":"3","category":"Service","parent_category":"Support System","softhard":"2","version":"1.16.1"},{"rule_id":"30000005","product":"Linux","company":"Linux","level":"2","category":"Operating System","parent_category":"Software System","softhard":"2","version":"4.9.0"},{"rule_id":"30000008","product":"Java","company":"Oracle","level":"4","category":"Development Framework","parent_category":"Support System","softhard":"2","version":"25.222-b10"},{"rule_id":"12","product":"Elasticsearch","company":"Elastic, Inc.","level":"3","category":"Database System","parent_category":"Software System","softhard":"2","version":"2.4.0"},{"rule_id":"855434","product":"Log4j2","company":"其他","level":"4","category":"Component","parent_category":"Support System","softhard":"2","version":""},{"rule_id":"211","product":"Apache-Web-Server","company":"Apache Software Foundation.","level":"3","category":"Service","parent_category":"Support System","softhard":"2","version":""},{"rule_id":"210","product":"Apache-Tomcat","company":"Apache Software Foundation.","level":"3","category":"Service","parent_category":"Support System","softhard":"2","version":""}],"vulnerabilities":[{"hostinfo":"10.1.72.124:9200","name":"Elasticsearch unauthorized","filename":"Elasticsearch_Unauthorized.json","level":"3","vulurl":"http://10.1.72.124:9200/_cat","keymemo":"","hasexp":false}],"screenshots":null,"favicons":[{"hostinfo":"10.1.72.124:9200","imgpath":"\\screenshots\\20231110195039\\10.1.72.124-9200-f.ico","imgsize":"1150","phash":"1552860581"}],"hostnames":[""]}
    # ips = assetSearchResult['ips']
    # for ipAsset in ips:
    if ipAsset.get("hostnames") is not None:
        hostnames = ipAsset['hostnames'][0]
        if hostnames:
            asset_filtered = hostnames
        else:
            asset_filtered = ipAsset['ip']
    else:
        asset_filtered = ipAsset['ip']

    ip = ipAsset['ip']
    iptag = ipAsset['ipTag']
    ports = Json(ipAsset['ports'])
    protocols = Json(ipAsset['protocols'])
    tags = Json(ipAsset['tags'])
    os = ipAsset['os']
    hostname = ipAsset['hostname']
    hostnames = ipAsset['hostnames']
    with PostgresConnectionContextManager() as cur:
        # 检测是否存在ip记录存在则update不存在则insert
        cur.execute("SELECT ip FROM plugin_goby_result WHERE ip=%s", (ip,))
        rows = cur.fetchone()
        if rows:
            cur.execute(
                "UPDATE plugin_goby_result SET asset_filtered=%s,ipTag=%s,ports=%s,protocols=%s,tags=%s,os=%s,hostname=%s,hostnames=%s WHERE ip=%s",
                (asset_filtered, iptag, ports, protocols, tags, os, hostname, hostnames, ip))
        else:
            cur.execute(
                "INSERT INTO plugin_goby_result (ip,asset_filtered,ipTag,ports,protocols,tags,os,hostname,hostnames) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (ip, asset_filtered, iptag, ports, protocols, tags, os, hostname, hostnames))

        return True


if __name__ == '__main__':
    a = '{"ips":[{"ip":"10.1.72.114","mac":"1","os":"1","hostname":"elasticsearch.May Parker","honeypot":"0","ipTag":"123123","ports":[{"port":"123","baseprotocol":"udp"},{"port":"8081","baseprotocol":"tcp"},{"port":"22","baseprotocol":"tcp"},{"port":"9200","baseprotocol":"tcp"},{"port":"8080","baseprotocol":"tcp"}],"protocols":{"10.1.72.124:123":{"port":"123","hostinfo":"10.1.72.124:123","url":"","product":"NTP server","protocol":"ntp","json":"","fid":[""],"products":["NTP server"],"protocols":["ntp"]},"10.1.72.124:22":{"port":"22","hostinfo":"10.1.72.124:22","url":"","product":"OpenSSH|debian-操作系统","protocol":"ssh","json":"","fid":[""],"products":["OpenSSH","debian-操作系统"],"protocols":["ssh"]},"10.1.72.124:8080":{"port":"8080","hostinfo":"10.1.72.124:8080","url":"","product":"Apache-Tomcat|Apache-Web-Server","protocol":"http","json":"","fid":[],"products":["Apache-Tomcat","Apache-Web-Server"],"protocols":["http","web"]},"10.1.72.124:8081":{"port":"8081","hostinfo":"10.1.72.124:8081","url":"","product":"Nginx","protocol":"http","json":"","fid":["ZvJCtGzrqEyHLFflRL595vwXT9k+bh/O"],"products":["Nginx"],"protocols":["http","web"]},"10.1.72.124:9200":{"port":"9200","hostinfo":"10.1.72.124:9200","url":"","product":"Log4j2|Elasticsearch|Java|Linux","protocol":"elastic","json":"","fid":[],"products":["Log4j2","Elasticsearch","Java","Linux"],"protocols":["elastic","web"]}},"tags":[{"rule_id":"17291","product":"NTP server","company":"other","level":"3","category":"Other Support System","parent_category":"Support System","softhard":"0","version":""},{"rule_id":"4531","product":"debian-操作系统","company":"Public Interest, Inc.","level":"2","category":"Operating System","parent_category":"Software System","softhard":"2","version":""},{"rule_id":"7512","product":"OpenSSH","company":"other","level":"3","category":"Other Support System","parent_category":"Support System","softhard":"2","version":""},{"rule_id":"209","product":"Nginx","company":"other","level":"3","category":"Service","parent_category":"Support System","softhard":"2","version":"1.16.1"},{"rule_id":"30000005","product":"Linux","company":"Linux","level":"2","category":"Operating System","parent_category":"Software System","softhard":"2","version":"4.9.0"},{"rule_id":"30000008","product":"Java","company":"Oracle","level":"4","category":"Development Framework","parent_category":"Support System","softhard":"2","version":"25.222-b10"},{"rule_id":"12","product":"Elasticsearch","company":"Elastic, Inc.","level":"3","category":"Database System","parent_category":"Software System","softhard":"2","version":"2.4.0"},{"rule_id":"855434","product":"Log4j2","company":"其他","level":"4","category":"Component","parent_category":"Support System","softhard":"2","version":""},{"rule_id":"211","product":"Apache-Web-Server","company":"Apache Software Foundation.","level":"3","category":"Service","parent_category":"Support System","softhard":"2","version":""},{"rule_id":"210","product":"Apache-Tomcat","company":"Apache Software Foundation.","level":"3","category":"Service","parent_category":"Support System","softhard":"2","version":""}],"vulnerabilities":[{"hostinfo":"10.1.72.124:9200","name":"Elasticsearch unauthorized","filename":"Elasticsearch_Unauthorized.json","level":"3","vulurl":"http://10.1.72.124:9200/_cat","keymemo":"","hasexp":false}],"screenshots":null,"favicons":[{"hostinfo":"10.1.72.124:9200","imgpath":"\\\\screenshots\\\\20231110195039\\\\10.1.72.124-9200-f.ico","imgsize":"1150","phash":"1552860581"}],"hostnames":[""]}]}'
    c = json.loads(a)
    print(c)
    dataStore(c)

    # searchStr = "taskId=\""+'1122333'+"\" && ()"
    # searchModel = AssetSearchModel(searchStr)
    # print(searchModel)
    # print(searchModel.serialize())
