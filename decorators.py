import time


def timer(func: callable) -> callable(object):
    """Decorator for timing api calls.

    Assumes the second argument in *args is the endpoint for printing purposes.
    :param func: function to be timed
    :return: wrapper function
    """

    def wrapper(*args: list | set | tuple, **kwargs: dict) -> callable(object):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed = end_time - start_time
        elapsed = round(elapsed, 2)
        print(f'url: {args[1]} took {elapsed} seconds')
        return result

    return wrapper
