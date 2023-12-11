import functools
import time


def loggable(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"S - {func.__name__}")
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"E - {func.__name__} in {end_time - start_time:.2f} seconds")
        return result

    return wrapper
