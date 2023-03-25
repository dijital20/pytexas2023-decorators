# "Observer Decorators"

- *Add code before/after wrapped code to observe but not change operation.*
- Logging function calls
- Timing/performance measurements

---

## Example: The Logging Decorator

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
