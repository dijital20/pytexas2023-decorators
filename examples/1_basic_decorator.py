from functools import wraps


def basic_decorator(func):
    print(f'<-> basic_decorator decorating {func.__name__}')
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f'--> Running from wrapper with {args}, {kwargs}')
        result = func(*args, **kwargs)
        print(f'<-- Finished running wrapper, returning {result}')
        return result

    return wrapper



@basic_decorator
def example1(foo, bar=1):
    print('    This is inside example1')


if __name__ == '__main__':
    print('    Starting __main__')
    example1('hello there')
    example1(True, bar=2)
