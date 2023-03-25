# Parameterized Decorators

- *Provide input to the decorator and use that in the decorated code.*
- Categorizing objects
- Authorization controls/checks
- Limiting controls/checks

---

## Example: The Locking Decorator

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

## Example: The Registration Decorator

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
