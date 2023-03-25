import logging
import time
from collections.abc import Callable
from functools import wraps
from threading import Lock, Thread
from typing import ParamSpec, TypeVar

T, P = TypeVar("T"), ParamSpec("P")
LOG = logging.getLogger(__name__)


# --- DECORATOR ---
def uses_lock(
    func: Callable[P, T] | None = None, *, lock: Lock = None
) -> Callable[P, T]:
    """Decorates a function to acquired exclusive access to a resource with a lock.

    Args:
        func: Function to decorate. Defaults to None.

    Keyword Args:
        lock: Lock to use. Defaults to None, but must be passed a value.

    Raises:
        ValueError: If lock is left at None.

    Returns:
        Function wrapper.

    Examples:
        >>> from threading import Lock
        >>> my_lock = Lock()
        >>> @uses_lock(lock=my_lock)
        ... def my_function():
        ...     ...
    """
    if not lock:
        raise ValueError("You must specify a lock.")

    def wrapper(wfunc: Callable[P, T]) -> Callable[P, T]:
        """Wraps a function call to acquire a lock.

        Args:
            wfunc: Function to wrap.

        Returns:
            Wrapped function.
        """

        @wraps(wfunc)
        def wrapped(*args: P.args, **kwargs: P.kwargs) -> T:
            """Wrapped function call."""
            LOG.info("--> Waiting for %d", id(lock))
            with lock:
                LOG.info("Calling %s", wfunc.__name__)
                result = wfunc(*args, **kwargs)

            LOG.info("<-- Released %d", id(lock))
            return result

        return wrapped

    return wrapper(func) if func else wrapper


# --- END DECORATOR ---

keyboard_lock = Lock()
mouse_lock = Lock()


@uses_lock(lock=keyboard_lock)
def type_a_message():
    """Types a message on the machine."""
    LOG.info("Starting type_a_message")
    time.sleep(1)
    LOG.info("Returning from type_a_message.")


@uses_lock(lock=keyboard_lock)
def send_keys():
    """Sends keystrokes to the machine."""
    LOG.info("Starting send_keys")
    time.sleep(3)
    LOG.info("Returning from send_keys.")


@uses_lock(lock=mouse_lock)
def move_mouse():
    """Moves the mouse on the machine."""
    LOG.info("Starting move_mouse")
    time.sleep(5)
    LOG.info("Returning from move_mouse.")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(levelname).1s %(threadName)s: %(message)s"
    )

    threads = [
        Thread(target=f, name=f"{f.__name__} #{i}")
        for i in range(1, 4)
        for f in (type_a_message, send_keys, move_mouse)
    ]
    LOG.info("Starting threads")
    for t in threads:
        t.start()

    LOG.info("Waiting for threads")
    while any(t.is_alive() for t in threads):
        pass

    LOG.info("Threads complete.")
