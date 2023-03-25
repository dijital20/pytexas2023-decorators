# Parameterized Decorators

- *Provide input to the decorator and use that in the decorated code.*
- Categorizing objects
- Authorization controls/checks
- Limiting controls/checks

---

## Example: The Locking Decorator

This decorator uses a syntax that I first saw using [pytest](https://docs.pytest.org/en/7.2.x/). This particular syntax (having `func=None` and then requiring parameters to be keyword args) allows for usage both with or without parenthesis. In this particular case, you must use with parenthesis, but in other cases where you may not need to, the syntax is good.

```python
{% 
    include "../examples/3_locking_decorator.py" 
    start="# --- DECORATOR ---"
    end="# --- END DECORATOR ---"
    trailing-newlines=false
%}
```

---

## Example: The Registration Decorator

This decorator uses a class instance as the decorator instead of a function. This allows us to store parameters as part of the object's state, and mutate it as necessary.

```python
{% 
    include "../examples/4_registration_decorator.py" 
    start="# --- DECORATOR ---"
    end="# --- END DECORATOR ---"
    trailing-newlines=false
%}
```
