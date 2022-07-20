import functools
import logging

logger = logging.Logger(__name__)


def watch(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        res = method(self, *args, **kwargs)
        msg = f"[{self.__class__.__name__}.{method.__name__}] {locals()['args']} ::: {res}"
        if self.DEBUG or globals()["DEBUG"]:
            print(msg, end="\r")
        logger.debug(msg)

        return res

    return wrapper
