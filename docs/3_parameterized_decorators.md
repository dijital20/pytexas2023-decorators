# Parameterized Decorators

- *Provide input to the decorator and use that in the decorated code.*
- Categorizing objects
- Authorization controls/checks
- Limiting controls/checks

---

## Example: The Locking Decorator

This decorator is useful for both signaling to the reader that the function needs a specific lock, and handles acquiring and releasing the lock around the function call. This reduces boilerplate that might otherwise need to be written into multiple functions.

The parameters take advantage of namespace rules. When you try to access the contents of a name, Python first checks the local namespace. Failing that, it begins checking each parent namespace, returning the value from the first namespace where the name is defined, or raising a `NameError` if it gets beyond the global namespace and still has not found the name defined.

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
