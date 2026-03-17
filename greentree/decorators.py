import time


def timeit(func):
    def wrapper(*args, **kwargs):
        start = time.monotonic()
        result = func(*args, **kwargs)
        end = time.monotonic()

        duration = end - start
        print(f"[TIMEIT] {func.__name__} took {duration:.6f} seconds")

        return result

    return wrapper
