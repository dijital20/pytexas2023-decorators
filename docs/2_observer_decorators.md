# Observer Decorators

- *Add code before/after wrapped code to observe but not change operation.*
- Logging function calls
- Timing/performance measurements

---
## Example: The Logging Decorator

This decorator is a quick, simple mainstay of codebases I have worked in, and does a good job of reducing boilerplate code in functions. This decorator simply logs the function call, parameters, and then the return, whether it was from a raised exception or a returned value. It's also very easy to add logic to this to log out performance measures, such as the elapsed time of the function.

```python
{% 
    include "../examples/2_logging_decorator.py" 
    start="# --- DECORATOR ---"
    end="# --- END DECORATOR ---"
    trailing-newlines=false
%}
```
