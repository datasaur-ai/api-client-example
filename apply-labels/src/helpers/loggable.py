import functools
import logging
import time


def loggable(func, with_args=False):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if with_args:
            logging.info(f"S - {func.__qualname__} {kwargs=}")
        else:
            logging.info(f"S - {func.__qualname__}")
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logging.info(f"E - {func.__qualname__} in {end_time - start_time:.2f} seconds")
        return result

    return wrapper


def loggable_with_args(func):
    return loggable(func, with_args=True)
