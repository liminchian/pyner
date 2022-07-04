import functools
import itertools
import logging

logger = logging.Logger(__name__)


class _Pipe:
    DEBUG: bool = False
    ENCODING: str = "utf-8"


def watch(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        res = method(self, *args, **kwargs)
        msg = f"[{self.__class__.__name__}.{method.__name__}] {locals()['args']} ::: {res}"
        if self.DEBUG:
            print(msg, end="\r")
        logger.debug(msg)

        return res

    return wrapper
