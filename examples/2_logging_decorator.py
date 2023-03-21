import logging
from functools import wraps



LOG = logging.getLogger(__name__)

def log_call(func):
    
    @wraps(func)
    def call_logger(*args, **kwargs):
        LOG.info('--> Calling %s', func.__qualname__)
        
        try:
            result = func(*args, **kwargs)
        
        except:
            LOG.error('<!- ERROR occurred calling %s', func.__qualname__, exc_info=True)
            raise
        
        else:
            LOG.info('<-- %s returning %r', func.__qualname__, result)
            return result
    
    return call_logger


@log_call
def my_test_function(is_fail=False):
    LOG.info('Inside my_test_function, where is_fail=%r', bool(is_fail))
    if is_fail:
        raise RuntimeError('I am a scary failure!')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(levelname).1s %(funcName)s: %(message)s')

    my_test_function()
    my_test_function(0)
    my_test_function(is_fail=True)