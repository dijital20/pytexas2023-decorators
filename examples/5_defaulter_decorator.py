import logging
from functools import wraps
from collections.abc import Callable
from typing import Any, ParamSpec, TypeVar

T, P = TypeVar("T"), ParamSpec("P")
LOG = logging.getLogger(__name__)


# --- DECORATOR ---
def default_on_fail(
    func: Callable[P, T] = None,
    *,
    type_: type | None = None,
    exceptions: type[Exception] = Exception,
    default: Any = None,
) -> Callable[P, T]:
    """Decorates a function to handle data conversion and exceptions.

    Args:
        func: Function to decorate. Defaults to None.

    Keyword Args:
        type_: Type that the output should be converted to. Defaults to None, but must
            be overridden.
        exceptions: Exception types to catch from call or conversion. Defaults to
            Exception.
        default: Default value in the event of an error. Defaults to None.

    Raises:
        ValueError: If type_ is not specified.

    Returns:
        _type_: Function wrapper.
    """
    if not type_:
        raise ValueError("You must specify type_.")

    def wrapper(wfunc: Callable[P, T]) -> Callable[P, T]:
        """Decorates a function to convert output and handle errors.

        Args:
            wfunc: Function to wrap.

        Returns:
            Wrapped function.
        """

        @wraps(wfunc)
        def change_output(*args: P.args, **kwargs: P.kwargs) -> T:
            """Wrapped function call."""
            try:
                result = wfunc(*args, **kwargs)
            except exceptions:
                LOG.warning("Caught error executing %s", wfunc.__name__, exc_info=True)
                return default

            try:
                return type_(result)
            except exceptions as e:
                LOG.warning(
                    "Caught error converting %s to %s: %s: %s",
                    type(result).__name__,
                    type_.__name__,
                    type(e).__name__,
                    e,
                )
                return default

        return change_output

    return wrapper(func) if func else wrapper


# --- END DECORATOR ---


@default_on_fail(type_=int, default=1)
def get_session(payload) -> int:
    """Extracts the Session field from the payload.

    Args:
        payload: Decoded JSON payload.

    Returns:
        Session value.
    """
    return payload["session"]


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(levelname).1s %(funcName)s: %(message)s"
    )

    LOG.info("--> %r\n", get_session({"session": 5}))
    LOG.info("--> %r\n", get_session({"session": "5"}))
    LOG.info("--> %r\n", get_session({"session": None}))
    LOG.info("--> %r\n", get_session(None))
