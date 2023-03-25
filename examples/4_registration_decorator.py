from collections import UserList
from collections.abc import Callable, Iterator
from typing import ParamSpec, TypeVar

T, P = TypeVar("T"), ParamSpec("P")


# --- DECORATOR ---
class CategoryCollection(UserList):
    """Groups functions with the same signature for group operations.

    Examples:
        >>> number_transform = CategoryCollection('number_transform')
        >>> @number_transform
        ... def square(i):
        ...     return i ** 2
        >>> @number_transform
        ... def divide(i):
        ...     return i // 2
        >>> list(number_transform.call_all(2))
        [4, 1]
    """

    def __init__(self, category: str):
        """Prepare a CategoryCollection for use.

        Args:
            category: Category name.
        """
        super().__init__()
        self.category = category

    def __call__(self, func: Callable[P, T]) -> Callable[P, T]:
        """Decorates a function to add it to the collection.

        Args:
            func: Function to add.

        Returns:
            The original function.
        """
        self.append(func)
        return func

    def call_all(self, *args: P.args, **kwargs: P.kwargs) -> Iterator[T]:
        """Call each function and generate its output.

        Yields:
            Output from the function.
        """
        yield from (cb(*args, *kwargs) for cb in self)


# --- END DECORATOR ---

actions = CategoryCollection("actions")


@actions
def double(i: int) -> int:
    """Doubles the input.

    Args:
        i: Input.

    Returns:
        Doubled value.
    """
    return i * 2


@actions
def half(i: int) -> int:
    """Halves the input.

    Args:
        i: Input.

    Returns:
        Half the input.
    """
    return i // 2


@actions
def add_three(i: int) -> int:
    """Adds 3 to the input.

    Args:
        i: Input.

    Returns:
        Input with 3 added.
    """
    return i + 3


if __name__ == "__main__":
    actions(lambda i: i**2)

    print(list(actions.call_all(3)))
    print(list(actions.call_all(21)))
    print(list(actions.call_all(99)))
