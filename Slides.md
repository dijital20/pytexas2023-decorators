---
marp: true
footer: #PyTexas 2023 - Practical Decorators
paginate: true
style: |
    table {
        margin-top: 1em;
        align: center;
    }
    .columns {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 1rem;
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

## Decorator Syntax

This...

```python
@silence_exceptions  # <---
def my_activity():
    ...
```

Is the same as...

```python
my_activity = silence_exceptions(my_activity)
```

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

## "Observer Decorators"

- *Add code before/after wrapped code to observe but not change operation.*
- Logging function calls
- Timing/performance measurements


<!-- _class: invert  -->
---

## The Logging Decorator

```python
LOG = logging.getLogger(__name__)

def log_call(func):
    
    @wraps(func)
    def call_logger(*args, **kwargs):
        LOG.info('Calling %s', func.__qualname__)
        
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

- *Provide input to the decorator and use that in the decorated code.*
- Categorizing objects
- Authorization controls/checks
- Limiting controls/checks

<!-- _class: invert  -->

---

## The Registration Decorator

```python
from collections import UserList

class CategoryCollection(UserList):
    def __init__(self, category):
        super().__init__()
        self.category = category

    def __call__(self, func):
        self.append(func)
        return func

    def call_all(self, *args, **kwargs):
        yield from (cb(*args, *kwargs) for cb in self)

...

actions = CategoryCollection('actions')

@actions
def do_something():
    ...
```

---

## The Locking Decorator

```python
def uses_lock(func = None, *, lock=None):
    if not lock:
        raise ValueError('You must specify a lock.')
    
    def wrapper(wfunc):
        @wraps(wfunc)
        def wait_for_lock(*args, **kwargs):
            LOG.info('--> Waiting for %r', lock)
            with lock:
                LOG.info('Calling %s', wfunc.__name__)
                result = wfunc(*args, **kwargs)
            LOG.info('<-- Released %r', lock)
            return result

        return wait_for_lock
    
    return wrapper(func) if func else wrapper
```

---

## Mutating Decorators

- *Catch input or output, and either validate or change the type.*
- Change input/return values.
- Validate input/output values.

<!-- _class: invert  -->

---

## The Defaulter Decorator

```python
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
```

---

## Pros and Cons

<div class="columns">
<div>

### Pros

* Makes code very portable
* Reduces boilerplate
* When decorators' functions are understood, aid in readability.

</div>
<div>

### Cons

* Gives no insight into code complexity behind the decorator.
* Can create a layer of indirection which can make debugging complicated.
* Parameterized decorators can be complicated to maintain.

</div>
</div>

---

## Questions and Closing

<!-- _class: invert  -->
