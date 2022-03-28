import sys
from typing import TYPE_CHECKING

from pyner._config import _LazyModule

_import_structure = {"decorator": ["print_iter", "benchmark"]}

if TYPE_CHECKING:
    from pyner.utils.decorator import benchmark, print_iter
else:
    sys.modules[__name__] = _LazyModule(
        __name__,
        globals()["__file__"],
        _import_structure,
        extra_objects={"__version__": __version__},
    )
