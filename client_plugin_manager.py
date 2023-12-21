import json
import time
import nb_log
import time
from utils.redis_manager import RedisMixin
import socket
from services.init import regPlugins
import multiprocessing
import threading

if __name__ == '__main__':
    hostName = socket.gethostname()
    regDict = regPlugins()
    processDict = {}
    while True:
        time.sleep(5)
        # 循环监听plugin-center中的key，检测与regDict中key相同的值
        for k, v in regDict.items():
            result = RedisMixin().redis_db_service.hget('plugin-center', k)
            tmp = json.loads(result)
            if 'open' == tmp.get('status'):
                nb_log.info(f'开启{k}')
                tmp['status'] = 'opening'
                RedisMixin().redis_db_service.hset('plugin-center',k,json.dumps(tmp))
                p = multiprocessing.Process(target=v)
                processDict[k] = p
                p.start()
            elif 'shutDown' == tmp.get('status'):
                nb_log.info(f'关闭{k}')
                tmp['status'] = 'close'
                RedisMixin().redis_db_service.hset('plugin-center',k,json.dumps(tmp))
                processDict[k].terminate()
                processDict[k].join()


