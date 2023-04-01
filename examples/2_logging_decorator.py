import logging
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

T, P = TypeVar("T"), ParamSpec("P")
LOG = logging.getLogger(__name__)


# --- DECORATOR ---
def log_call(func: Callable[P, T]) -> Callable[P, T]:
    """Decorates a function log calls to it and errors/returns from it.

    Args:
        func: Function to decorate.

    Returns:
        Wrapped function.

    Examples:
        >>> import logging
        >>> @log_call
        ... def my_function():
        ...     ...
    """

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        """Wrapped call, which handles logging."""

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
def my_test_function(is_fail: bool = False) -> bool:
    """Does a thing.

    Args:
        is_fail: Should we fail?. Defaults to False.

    Raises:
        RuntimeError: If is_fail was a truthy value.

    Returns:
        Always returns True.
    """
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
