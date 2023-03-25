import logging
from functools import wraps


LOG = logging.getLogger(__name__)


# --- DECORATOR ---
def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        LOG.info("--> Calling %s", func.__name__)

        try:
            result = func(*args, **kwargs)

        except:
            LOG.error("<!- ERROR occurred calling %s", func.__name__, exc_info=True)
            raise

        else:
            LOG.info("<-- %s returning %r", func.__name__, result)
            return result

    return wrapper


# --- END DECORATOR ---


@log_call
def my_test_function(is_fail=False):
    LOG.info("Inside my_test_function, where is_fail=%r", bool(is_fail))
    if is_fail:
        raise RuntimeError("I am a scary failure!")
    return True


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(levelname).1s %(funcName)s: %(message)s"
    )

    my_test_function()
    my_test_function(0)
    my_test_function(is_fail=True)
