# Decorator Syntax

This...

```python
@silence_exceptions  # <--- Sweet, beautiful syntactic sugar
def my_activity():
    ...
```

Is the same as...

```python
my_activity = silence_exceptions(my_activity)
```

A decorator is a **function**, that takes a **function** as an input, and returns a **function** in its place.

## Anatomy of a Decorator

```python
from functools import wraps
from typing import ParamSpec, TypeVar

P, T = ParamSpec('P'), TypeVar('T')

def decorator(func: Callable[P, T]) -> Callable[P, T]:
    """Decorates a function."""
    
    @wraps(func)  # Make decorated_func look like func.
    def decorated_func(*args: P.args, **kwargs: P.kwargs) -> T:
        """Decorated function call."""
        # ...
        result = func(*args, **kwargs)
        # ...
        return result
    
    return decorated_func  # Return that decorated function.

```
