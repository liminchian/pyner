import importlib
import os
from types import ModuleType
from typing import Any, Iterable


class _LazyModule(ModuleType):
    def __init__(
        self,
        name: str,
        module_file: str,
        import_structure: dict,
        extra_objects=None,
    ):
        super().__init__(name)
        self._modules = set(import_structure.keys())
        self._class_to_module = {
            val: key for key, vals in import_structure.items() for val in vals
        }
        self.__all__ = list(import_structure.keys()) + sum(
            import_structure.values(), []
        )
        self.__file__ = module_file
        self.__path__ = [os.path.dirname(module_file)]
        self._objects = {} if not extra_objects else extra_objects
        self._name = name
        self._import_structure = import_structure

    def __dir__(self) -> Iterable[str]:
        dirs = list(super().__dir__())
        return dirs + self.__all__

    def __getattr__(self, name: str) -> Any:
        if name in self._objects:
            return self._objects[name]
        if name in self._modules:
            val = self._get_module(name)
        elif name in self._class_to_module.keys():
            module = self._get_module(name)
            val = getattr(module, name)
        else:
            raise AttributeError(f"module {self.__name__} has no attribute {name}")

        setattr(self, name, val)
        return val

    def _get_module(self, module_name: str):
        return importlib.import_module("." + module_name, self.__name__)

    def __reduce__(self):
        return (
            self.__class__,
            (self._name, self.__file__, self._import_structure),
        )


if __name__ == "__main__":
    ROOT = os.path.abspath(os.path.dirname(__file__))
