import pytest


def print_test(assert_out):
    def decorator(test_func):
        def wrapper(capsys, *args, **kwargs):
            res = test_func(*args, **kwargs)
            out, _ = capsys.readouterr()
            assert out == assert_out
            return res

        return wrapper

    return decorator
