import logging
from functools import wraps


LOG = logging.getLogger(__name__)


def default_on_fail(func=None, *, type_=None, exceptions=Exception, default=None):
    if not type_:
        raise ValueError('You must specify type_.')

    def wrapper(wfunc):
        @wraps(wfunc)
        def change_output(*args, **kwargs):
            try:
                result = wfunc(*args, **kwargs)
            except exceptions:
                LOG.warning('Caught error executing %s', wfunc.__qualname__, exc_info=True)
                return default
            
            try:
                return type_(result)
            except exceptions as e:
                LOG.warning(
                    'Caught error converting %s to %s: %s: %s', 
                    type(result).__name__, type_.__name__, type(e).__name__, e
                )
                return default
        
        return change_output
    
    return wrapper(func) if func else wrapper


@default_on_fail(type_=int, default=1)
def get_session(payload):
    return payload['session']


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(levelname).1s %(funcName)s: %(message)s')

    LOG.info(f'--> %r\n', get_session({'session': 5}))
    LOG.info(f'--> %r\n', get_session({'session': '5'}))
    LOG.info(f'--> %r\n', get_session({'session': None}))
    LOG.info(f'--> %r\n', get_session(None))
