from  core.notify import Notify




a = Notify('test')
for i in range(10):
    a.info('test')
    a.waring('test2')
    a.error('test3')
    a.high('test4')
    a.medium('test5')
    a.low('test6')

from utils.redis_manager import RedisMixin

c = RedisMixin().redis_db_service.blpop('notify', 10)
print(c[1])