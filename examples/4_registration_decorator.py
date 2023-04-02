from collections import UserList
from collections.abc import Callable
from string import ascii_uppercase
from typing import ParamSpec

P = ParamSpec("P")


# --- DECORATOR ---
class CategoryCollection(UserList):
    """Groups functions with the same signature that define rules.

    Examples:
        >>> number_rules = CategoryCollection('number_rules')
        >>> @number_rules
        ... def multiple_of_5(i):
        ...     return i % 5 == 0
        >>> @number_rules
        ... def even(i):
        ...     return i % 2 == 0
        >>> number_rules.violates(2)
        ['multiple_of_5']
        >>> number_rules.violates(5)
        ['even']
        >>> number_rules.violates(10)
        []
    """

    def __init__(self, category: str):
        """Prepare a CategoryCollection for use.

        Args:
            category: Category name.
        """
        super().__init__()
        self.category = category

    def __call__(self, func: Callable[P, bool]) -> Callable[P, bool]:
        """Decorates a function to add it to the collection.

        Args:
            func: Function to add.

        Returns:
            The original function.
        """
        self.append(func)
        return func

    def violates(self, *args: P.args, **kwargs: P.kwargs) -> list[str]:
        """Find registered functions that return false for the input.

        Returns:
            List of function names that returned False.
        """
        return [f.__name__ for f in self if not f(*args, **kwargs)]


# --- END DECORATOR ---

grammar_rules = CategoryCollection("grammar_rules")


@grammar_rules
def starts_with_a_capital(stuff: str) -> int:
    """Doubles the input.

    Args:
        stuff: Input.

    Returns:
        Doubled value.
    """
    return stuff.strip()[0] in ascii_uppercase


@grammar_rules
def ends_with_punctuation(sentence: str) -> int:
    """Halves the input.

    Args:
        sentence: Input.

    Returns:
        Half the input.
    """
    return sentence.strip()[-1] in ".?!"


@grammar_rules
def i_is_capitalized(sentence: str) -> int:
    """Adds 3 to the input.

    Args:
        i: Input.

    Returns:
        Input with 3 added.
    """
    return not any(w == "i" for w in sentence.split(" "))


if __name__ == "__main__":
    for s in ("i am someone!", "what is punctuation?", "foodle dee doodle dee"):
        print(f'"{s}" violates: {", ".join(grammar_rules.violates(s))}')
