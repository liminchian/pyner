import functools
import logging

logger = logging.Logger(__name__)


def watch(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        res = method(self, *args, **kwargs)
        msg = f"[{self.__class__.__name__}.{method.__name__}] {locals()['args']} ::: {res}"
        logger.debug(msg)
        if not self.DEBUG or not globals()["DEBUG"]:
            return res
        print(msg, end="\r")
        return res

    return wrapper
