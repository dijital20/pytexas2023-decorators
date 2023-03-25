# Mutating Decorators

- *Catch input or output, and either validate or change the type.*
- Change input/return values.
- Validate input/output values.

<!-- _class: invert  -->

---

## Example: The Defaulter Decorator

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
                LOG.warning('Caught error executing %s', wfunc.__name__, exc_info=True)
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