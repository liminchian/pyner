import functools
import time
import tracemalloc
from typing import Iterable


def print_iter(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        res = method(self, *args, **kwargs)
        if isinstance(res, Iterable):
            print(f"\nFunction:  {self.__class__.__name__}.{method.__name__}")
            for idx, obj in enumerate(res):
                print(f"   [{idx}]     {obj}")
            print("-" * 40)
        return res

    return wrapper


def benchmark(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        tracemalloc.start()
        start_time = time.perf_counter()
        res = method(self, *args, **kwargs)
        duration = time.perf_counter() - start_time
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print(
            f"\nFunction:           {self.__class__.__name__}.{method.__name__} - {method.__doc__}"
            f"\nMemory usage:       {current / 10**6:.6f} MB"
            f"\nPeak memory usage:  {peak / 10**6:.6f} MB"
            f"\nDuration:           {duration:.6f} sec"
            f"\n{'-' * 40}"
        )

        return res

    return wrapper


def lazyprop(method):
    name = method.__name__

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not hasattr(self, name):
            setattr(self, name, method(self, *args, **kwargs))
        return getattr(self, name)

    return property(fget=wrapper, doc=method.__doc__)
