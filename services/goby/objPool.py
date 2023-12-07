import queue
import threading
from contextlib import contextmanager


class ObjectPool(object):
    def __init__(self, fn_cls, *args, **kwargs):
        super(ObjectPool, self).__init__()
        self.fn_cls = fn_cls
        self._myinit(*args, **kwargs)

    def _myinit(self, *args, **kwargs):
        self.args = args
        self.maxSize = int(kwargs.get("maxSize", 1))
        self.queue = queue.Queue()

    def _get_obj(self):
        if isinstance(self.fn_cls, type):
            return self.fn_cls(*self.args)
        else:
            return self.fn_cls(self.args)

    def borrow_obj(self):
        if self.queue.qsize() < self.maxSize and self.queue.empty():
            self.queue.put(self._get_obj())
        return self.queue.get()

    def recover_obj(self, obj):
        self.queue.put(obj)


@contextmanager
def poolobj(pool):
    obj = pool.borrow_obj()
    try:
        yield obj
    except Exception:
        yield None
    finally:
        pool.recover_obj(obj)
