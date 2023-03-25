# Mutating Decorators

- *Catch input or output, and either validate or change the type.*
- Change input/return values.
- Validate input/output values.

<!-- _class: invert  -->

---

## Example: The Defaulter Decorator

This decorator does a good job of ensuring that a value is always of an expected type, and always returns a value. The decorator is configurable with the type, exceptions to catch, and default value. This can be good if you are, say, extracting or calculating values from a data structure you do not control, and want to ensure that the function always return a value of the specified type. 

This decorator also makes sure to log exceptions that it handles, so that debugging is easier.

```python
{% 
    include "../examples/5_defaulter_decorator.py" 
    start="# --- DECORATOR ---"
    end="# --- END DECORATOR ---"
    trailing-newlines=false
%}
```
