# Decorator Pros and Cons

## Pros

* Makes code very portable
* Reduces boilerplate
* When decorators' functions are understood, aid in readability.

## Cons

* Gives no insight into code complexity behind the decorator.
* Can create a layer of indirection which can make debugging complicated.
* Parameterized decorators can be complicated to maintain.

## Decorators in the standard library

- `classmethod` - Decorator that turns a bound function into being bound to the class instead of an instance of the class.
- `property` - Decorator that turns the wrapped function into a descriptor (object with a `__get__`, `__set__`, 
  and `__del__`).
- `contextlib.contextmanager` - Decorator that turns a function with a single `yield` statement into a context manager.
- `dataclasses.dataclass` - Decorator for a class, instead of a function, that generates boilerplate methods for classes with annotated class-level attributes.
- `functools.lru_cache` - Decorator that memoizes outputs based on their input arguments.
- `functools.wraps` - Decorator that decorates the function wrapper and takes the wrapped function as an argument, and updates the wrapper to look like the wrapped function.
- `functools.update_wrapper` - Function that takes a wrapper function and the wrapped function, and then updates the wrapper to look like the wrapped function.