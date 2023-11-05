from hashlib import md5
from store import Store
from typing import List,Type

#md5加密
def md5Encode(str:str)->str:
    '''

    :param str:MD5编码
    :return:
    '''
    return md5(str.encode('utf-8')).hexdigest()

def assertFilter(type:str,urls:List[str])->List[str]:
    '''
        :param type: 1:提取url中的域名(http://www.baidu.com/=>www.baidu.com
                        2:提取url中的域名(http://www.baidu.com/=>baidu.com
                        3:判断格式是否是ip，是的化有http://就去掉，然后删除ip中的端口号，不是ip而是域名则不做处理
                        4：去重
        :param urls: url列表
        :return: 返回处理后的url列表
    '''

    if type=='1':
        #提取url中的域名(http://www.baidu.com/=>www.baidu.com
        for i in range(len(urls)):
            if urls[i].startswith('http'):
                urls[i]=urls[i].split('//')[1]
            if urls[i].endswith('/'):
                urls[i]=urls[i][:-1]
        return list(set(urls))
    elif type=='2':
        #提取url中的域名(http://www.baidu.com/=>baidu.com
        for i in range(len(urls)):
            if urls[i].startswith('http'):
                urls[i]=urls[i].split('//')[1]
            if urls[i].endswith('/'):
                urls[i]=urls[i][:-1]
            #判断i是url还是ip如果是url则只取到二级域名.，如果是ip则不做处理

            if urls[i].count('.')==3:
                urls[i]=urls[i].split(':')[0]
            else:
                urls[i]=urls[i].split('.')[-2]+'.'+urls[i].split('.')[-1]
        return list(set(urls))
    elif type=='3':
        #判断格式是否是ip，是的化有http://就去掉，然后删除ip中的端口号，不是ip而是域名则不做处理
        for i in range(len(urls)):
            if urls[i].startswith('http'):
                urls[i]=urls[i].split('//')[1]
            if urls[i].endswith('/'):
                urls[i]=urls[i][:-1]
            if urls[i].count('.')==3:
                urls[i]=urls[i].split(':')[0]
        return list(set(urls))
    elif type=='4':
        #去重
        return list(set(urls))

class RowDataSetter():
    '''
    用于将数据放入数据库中
    规范化数据格式
    '''
    pass



if __name__ == '__main__':
    urls=["https://www.baidu.com","www.baidu.com","https://www.baidu.com/",'www.baidu.com','ccc.baidu.com'
          ,'8.8.8.8:80',"http://1.1.1.1:80/","8.8.8.8:80","8.8.8.8"]
    print(asserFilter('2',urls))


