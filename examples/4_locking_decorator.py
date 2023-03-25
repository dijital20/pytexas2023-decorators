import logging
import time
from functools import wraps
from threading import Lock, Thread

LOG = logging.getLogger(__name__)


# --- DECORATOR ---
def uses_lock(func=None, *, lock=None):
    if not lock:
        raise ValueError("You must specify a lock.")

    def wrapper(wfunc):
        @wraps(wfunc)
        def wait_for_lock(*args, **kwargs):
            LOG.info("--> Waiting for %d", id(lock))
            with lock:
                LOG.info("Calling %s", wfunc.__name__)
                result = wfunc(*args, **kwargs)
            LOG.info("<-- Released %d", id(lock))
            return result

        return wait_for_lock

    return wrapper(func) if func else wrapper


# --- END DECORATOR ---

keyboard_lock = Lock()
mouse_lock = Lock()


@uses_lock(lock=keyboard_lock)
def type_a_message():
    LOG.info("Starting type_a_message")
    time.sleep(1)
    LOG.info("Returning from type_a_message.")


@uses_lock(lock=keyboard_lock)
def send_keys():
    LOG.info("Starting send_keys")
    time.sleep(3)
    LOG.info("Returning from send_keys.")


@uses_lock(lock=mouse_lock)
def move_mouse():
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
