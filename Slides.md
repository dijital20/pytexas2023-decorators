---
marp: true
footer: #PyTexas 2023 - Practical Decorators
paginate: true
style: |
    table {
        margin-top: 1em;
        align: center;
    }
---

# Practical Decorators

**Josh Schneider**
[github/dijital20](https://github.com/dijital20)

<!-- 
_class: invert 
_footer: ""
_paginate: false
-->

---

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

---

## The Logging Decorator

```python
LOG = logging.getLogger(__name__)

...

def log_call(func):
    
    @wraps(func)
    def call_logger(*args, **kwargs):
        # Log call
        call_args = ', '.join(
            f'{k}={v!r}' 
            for k, v in inspect.getcallargs(func, args=args, kwargs=kwargs).items()
        )
        LOG.info('Calling %s with (%s)', func.__qualname__, call_args)
        
        # Get result
        try:
            result = func(*args, **kwargs)
        
        # Handle errors
        except:
            LOG.error('ERROR occurred calling %s', func.__qualname__, exc_info=True)
            raise
        
        # Handle result
        else:
            LOG.info('%s returning %r', func.__qualname__, result)
            return result
    
    return call_logger
```

---

## The Locking Decorator

```python

```

---

## The Access Decorator

```python

```
