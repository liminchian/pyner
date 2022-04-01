import sys
from typing import TYPE_CHECKING

from pyner._config import _LazyModule

_import_structure = {
    "decorator": ["logger", "benchmark", "lazyprop"],
    "crawler": ["DataCollector", "Pipe", "Pipeline", "Req", "Selector"],
}

if TYPE_CHECKING:
    from pyner.utils.crawler import (DataCollector, Pipe, Pipeline, Req,
                                     Selector)
    from pyner.utils.decorator import benchmark, lazyprop, logger
else:
    sys.modules[__name__] = _LazyModule(
        __name__,
        globals()["__file__"],
        _import_structure,
        extra_objects={"__version__": __version__},
    )
