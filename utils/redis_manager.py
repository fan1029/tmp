# coding=utf8

import copy
import redis5
import serviceConfig
from aioredis.client import Redis as AioRedis
from utils.decorators2 import cached_method_result



def get_redis_conn_kwargs():
    return {'host': serviceConfig.REDIS_HOST, 'port': serviceConfig.REDIS_PORT,
            'username': serviceConfig.REDIS_USERNAME,
            'password': serviceConfig.REDIS_PASSWORD, 'db': serviceConfig.REDIS_DB}


def _get_redis_conn_kwargs_by_db(db):
    conn_kwargs = copy.copy(get_redis_conn_kwargs())
    conn_kwargs['db'] = db
    return conn_kwargs


class RedisManager(object):
    _redis_db__conn_map = {}

    def __init__(self, host='127.0.0.1', port=6379, db=0, username='', password=''):
        self._key = (host, port, db, username, password,)
        if self._key not in self.__class__._redis_db__conn_map:
            self.__class__._redis_db__conn_map[self._key] = redis5.Redis(host=host, port=port, db=db, username=username,
                                                                         password=password, max_connections=100, decode_responses=True)
        self.redis = self.__class__._redis_db__conn_map[self._key]

    def get_redis(self) -> redis5.Redis:
        """
        :rtype :redis5.Redis
        """
        return self.redis


class AioRedisManager(object):
    _redis_db__conn_map = {}

    def __init__(self, host='127.0.0.1', port=6379, db=0, username='', password=''):
        self._key = (host, port, db, username, password,)
        if self._key not in self.__class__._redis_db__conn_map:
            self.__class__._redis_db__conn_map[self._key] = AioRedis(host=host, port=port, db=db, username=username,
                                                                     password=password, max_connections=100, decode_responses=True)
        self.redis = self.__class__._redis_db__conn_map[self._key]

    def get_redis(self) -> AioRedis:
        """
        :rtype :redis5.Redis
        """
        return self.redis


# noinspection PyArgumentEqualDefault
class RedisMixin(object):
    """
    可以被作为万能mixin能被继承，也可以单独实例化使用。
    """
    @property
    def redis_db_service(self):
        return RedisManager(**_get_redis_conn_kwargs_by_db(4)).get_redis()


    def redis_db_n(self, db):
        return RedisManager(**_get_redis_conn_kwargs_by_db(db)).get_redis()

    @property
    @cached_method_result
    def redis_db_frame(self):
        return RedisManager(**get_redis_conn_kwargs()).get_redis()

    def timestamp(self):
        """ 如果是多台机器做分布式控频 乃至确认消费，每台机器取自己的时间，如果各机器的时间戳不一致会发生问题，改成统一使用从redis服务端获取时间，单位是时间戳秒。"""
        time_tuple = self.redis_db_frame.time()
        # print(time_tuple)
        return time_tuple[0] + time_tuple[1] / 1000000


