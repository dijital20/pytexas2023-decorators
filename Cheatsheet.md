---
title: PyTexas Cheat Sheet
---

# Practical Decorators Cheat Sheet

## Simple Decorator

```python
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar


P = ParamSpec('P')
T = TypeVar('T')


def decorator(func: Callable[P, T]) -> Callable[P, T]:

    @wraps(func)
    def wrapped(*args: P.args, **kwargs: P.kwargs) -> T:
        # ... Do things before the wrapped function
        result = func(*args, **kwargs)
        # ... Do things after the wrapped function
        return result

    return wrapped


# --- Usage ---
@decorator
def my_func():
    ...

my_func = decorator(my_func)
```

---

## Parameterized Decorator (Function)

```python
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar


P = ParamSpec('P')
T = TypeVar('T')


def decorator(kwarg1, kwarg2=None) -> Callable[[Callable[P, T]], Callable[P, T]]:

    def wrapper(func: Callable[P, T]) -> Callable[P, T]:

        @wraps(func)
        def wrapped(*args: P.args, **kwargs: P.kwargs) -> T:
            # ... Do things before the wrapped function
            # ... Note that kwarg1 and kwarg2 are accessible in this scope.
            result = func(*args, **kwargs)
            # ... DO things after the wrapped function
            return result

        return wrapped

    return wrapper


# --- Usage ---
@decorator('foo', kwarg2='bar')
def my_func():
    ...

my_func = decorator('foo', kwarg2='bar')(my_func)
```

---

## Parameterized Decorator (Pytest Style)

```python
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar


P = ParamSpec('P')
T = TypeVar('T')


def decorator(func: Callable[P, T] | None = None, *, kwarg1=None, kwarg2=None) -> Callable[P, T]:

    def wrapper(func: Callable[P, T]):
        
        @wraps(func)
        def wrapped(*args: P.args, **kwargs: P.kwargs) -> T:
            # ... Do things before the wrapped function.
            # ... Note that kwarg1 and kwarg2 are accessible in this scope.
            result = func(*args, **kwargs)
            # ... Do things after the wrapped function.
            return result
        
        return wrapped

    return wrapper(func) if func else wrapper


# --- Usage ---
@decorator(kwarg1='foo', kwarg2='bar')
def my_func():
    ...

my_func = decorator(func, kwarg1='foo', kwarg2='bar')
```

---

## Parameterized Decorator (Class)

```python
from collections.abc import Callable
from functools import update_wrapper
from typing import ParamSpec, TypeVar


P = ParamSpec('P')
T = TypeVar('T')


class Decorator:
    def __init__(func: Callable[P, T], *, kwarg1=None, kwarg2=None):
        self.func = func
        update_wrapper(self, func)
        
        self.kwarg1 = kwarg1
        self.kwarg2 = kwarg2

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        # ... Do things before the wrapped function.
        # ... Note that self is completely accessible.
        result = self.func(*args, **kwargs)
        # ... Do things after the wrapped function.
        return result


# --- Usage ---
@Decorator(kwarg1='foo', kwarg2='bar')
def my_func():
    ...

my_func = Decorator(func, kwarg1='foo', kwarg2='bar')
```

## Some useful functions/libraries/decorators

- Built-in
  - `property` - Decorator that turns the wrapped function into a descriptor (object with a `__get__`, `__set__`, 
    and `__del__`).
- `functools`
  - `lru_cache` - Decorator that memoizes outputs based on their input arguments.
  - `wraps` - Decorator that decorates the function wrapper and takes the wrapped function as an argument, and updates 
    the wrapper to look like the wrapped function.
  - `update_wrapper` - Function that takes a wrapper function and the wrapped function, and then updates the wrapper to 
    look like the wrapped function.
- `contextlib`
  - `contextmanager` - Decorator that turns a function with a single `yield` statement into a context manager.