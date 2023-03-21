import logging
import random
import time
from functools import wraps
from threading import Lock, Thread

LOG = logging.getLogger(__name__)


def uses_lock(func = None, *, lock=None):
    if not lock:
        raise ValueError('You must specify a lock.')
    
    def wrapper(wfunc):
        @wraps(wfunc)
        def wait_for_lock(*args, **kwargs):
            LOG.info('--> Waiting for %r', lock)
            with lock:
                LOG.info('Calling %s', wfunc.__name__)
                result = wfunc(*args, **kwargs)
            LOG.info('<-- Released %r', lock)
            return result

        return wait_for_lock
    
    return wrapper(func) if func else wrapper


lock1 = Lock()
lock2 = Lock()


@uses_lock(lock=lock1)
def function1():
    LOG.info('Starting function1')
    time.sleep(1)
    LOG.info('Returning from function1.')


@uses_lock(lock=lock1)
def function2():
    LOG.info('Starting function2')
    time.sleep(3)
    LOG.info('Returning from function2.')


@uses_lock(lock=lock2)
def function3():
    LOG.info('Starting function3')
    time.sleep(5)
    LOG.info('Returning from function3.')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(levelname).1s %(thread)05d %(funcName)s: %(message)s')

    threads = [Thread(target=f) for _ in range(3) for f in (function1, function2, function3)]
    LOG.info('Starting threads')
    for t in threads:
        t.start()
    
    LOG.info('Waiting for threads')
    while any(t.is_alive() for t in threads):
        pass

    LOG.info('Threads complete.')
