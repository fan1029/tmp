# 写一个redis工具类，用连接池
import redis


class RedisPool(object):
    def __init__(self, host, port, db, password):
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.db, password=self.password, decode_responses=True)

    def get_conn(self):
        return redis.Redis(connection_pool=self.pool)

    def get_pool(self):
        return self.pool

class Store():
    def __init__(self):
        self.redis_pool = RedisPool('127.0.0.1', 6379, 0, None).get_conn()

    def set(self, key, value):
        self.redis_pool.set(key, value)

    def get(self, key):
        return self.redis_pool.get(key)

    def delete(self, key):
        self.redis_pool.delete(key)

    def exists(self, key):
        return self.redis_pool.exists(key)

    def expire(self, key, time):
        self.redis_pool.expire(key, time)

    def setnx(self, key, value):
        self.redis_pool.setnx(key, value)

    def setex(self, key, time, value):
        self.redis_pool.setex(key, time, value)

    def incr(self, key, amount=1):
        self.redis_pool.incr(key, amount)

    def decr(self, key, amount=1):
        self.redis_pool.decr(key, amount)

    def hset(self, name, key, value):
        self.redis_pool.hset(name, key, value)

    def hget(self, name, key):
        return self.redis_pool.hget(name, key)

    def hgetall(self, name):
        return self.redis_pool.hgetall(name)

    def hdel(self, name, key):
        self.redis_pool.hdel(name, key)

    def hlen(self, name):
        return self.redis_pool.hlen(name)

    def hkeys(self, name):
        return self.redis_pool.hkeys(name)

    def hvals(self, name):
        return self.redis_pool.hvals(name)

    def hexists(self, name, key):
        return self.redis_pool.hexists(name, key)

    #列表插入删除查看等方法
    def lpush(self, name, value):
        self.redis_pool.lpush(name, value)

    def rpush(self, name, value):
        self.redis_pool.rpush(name, value)

    def lpop(self, name):
        return self.redis_pool.lpop(name)

    def rpop(self, name):
        return self.redis_pool.rpop(name)

    def lrange(self, name, start, end):
        return self.redis_pool.lrange(name, start, end)

    def llen(self, name):
        return self.redis_pool.llen(name)

    def lrem(self, name, count, value):
        self.redis_pool.lrem(name, count, value)

    def lindex(self, name, index):
        return self.redis_pool.lindex(name, index)





if __name__ == '__main__':
    store = Store()
    store.lpush('ac', "1")
    store.lpush('ac', '2')
    store.lpush('ac', '3')
    store.lrem('ac', 0,'2')
    store.lrange('ac', 0, -1)
    print(store.exists('ac'))