from collections import UserList


# --- DECORATOR ---
class CategoryCollection(UserList):
    def __init__(self, category):
        super().__init__()
        self.category = category

    def __call__(self, func):
        self.append(func)
        return func

    def call_all(self, *args, **kwargs):
        yield from (cb(*args, *kwargs) for cb in self)


# --- END DECORATOR ---

actions = CategoryCollection("actions")


@actions
def double(i):
    return i * 2


@actions
def half(i):
    return i // 2


@actions
def add_three(i):
    return i + 3


if __name__ == "__main__":
    actions(lambda i: i**2)

    print(list(actions.call_all(3)))
    print(list(actions.call_all(21)))
    print(list(actions.call_all(99)))
