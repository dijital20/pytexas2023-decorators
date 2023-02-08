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

## Quick decorator demo

### *To the REPL!!*

---

## "Observer Decorators"

* *Add code before/after wrapped code to observe but not change operation.*
* Logging function calls
* Timing/performance measurements


<!-- _class: invert  -->
---

## The Logging Decorator

```python
LOG = logging.getLogger(__name__)

def log_call(func):
    
    @wraps(func)
    def call_logger(*args, **kwargs):
        call_args = ', '.join(
            f'{k}={v!r}' for k, v in inspect.getcallargs(
                func, args=args, kwargs=kwargs
            ).items()
        )
        LOG.info('Calling %s with (%s)', func.__qualname__, call_args)
        
        try:
            result = func(*args, **kwargs)
        
        except:
            LOG.error('ERROR occurred calling %s', func.__qualname__, exc_info=True)
            raise
        
        else:
            LOG.info('%s returning %r', func.__qualname__, result)
            return result
    
    return call_logger
```

---

## "Parameterized Decorators"

* *Provide input to the decorator and use that in the decorated code.*
* Categorizing objects
* Authorization controls/checks
* Limiting controls/checks

<!-- _class: invert  -->

---

## The Locking Decorator

```python
def uses_lock(func = None, /, lock=None):
    if not lock:
        raise ValueError('You must specify a lock.')
    
    @wraps(func)
    def wait_for_lock(*args, **kwargs):
        LOG.info('Waiting for %r', lock)
        with lock:
            LOG.info('Calling %s', func.__qualname__)
            return func(*args, **kwargs)
        LOG.info('Released %r', lock)
    
    return wait_for_lock(func) if func else wait_for_lock
```

---

## Mutating Decorators

* *Catch input or output, and either validate or change the type.*
* Change input/return values.
* Validate input/output values.

<!-- _class: invert  -->

---

## The Defaulter Decorator

```python
def default_on_fail(func=None, /, type_=None, exceptions=Exception, default=None):
    if not type_:
        raise ValueError('You must specify type_.')

    @wraps(func)
    def change_output(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except exceptions:
            LOG.warning('Caught error executing %s', func.__qualname__, exc_info=True)
            return default
        
        try:
            return type_(result)
        except exceptions:
            LOG.warning(
                'Caught error converting %s to %s', 
                type(result).__name__, type_.__name__, exc_info=True
            )
            return default
    
    return change_output(func) if func else change_output
```

---

## Questions and Closing

<!-- _class: invert  -->
