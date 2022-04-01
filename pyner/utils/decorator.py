import functools
import logging
import time
import tracemalloc
from types import FunctionType
from typing import Iterable

from pyner._config import DEBUG_VAR_NAME


def logger(obj):
    enabled = globals()[DEBUG_VAR_NAME]

    def _log(name, res):
        if isinstance(res, Iterable):
            for idx, o in enumerate(res):
                msg = f"[{name}/{idx}]: {o}"
                logging.debug(msg)
                if enabled:
                    print(msg)
        else:
            msg = f"[{name}]: {res}"
            logging.debug(msg)
            if enabled:
                print(msg)

    @functools.wraps(obj)
    def wrapper_func(*args, **kwargs):
        name = obj.__name__
        res = obj(*args, **kwargs)
        _log(name, res)
        return res

    @functools.wraps(obj)
    def wrapper_method(self, *args, **kwargs):
        name = f"{self.__class__.__name__}.{obj.__name__}"
        res = obj(self, *args, **kwargs)
        _log(name, res)
        return res

    if isinstance(obj, FunctionType):
        return wrapper_func
    return wrapper_method


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
