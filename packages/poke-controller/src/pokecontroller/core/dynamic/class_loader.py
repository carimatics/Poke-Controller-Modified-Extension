import importlib
import importlib.util
import inspect
import logging
import sys
from pathlib import Path
from types import ModuleType
from typing import Generator

from ..exception import PokeControllerException

logger = logging.getLogger(__name__)


class PokeControllerDynamicClassLoaderException(PokeControllerException):
    pass


class DynamicClassLoader[T]:
    def __init__(
        self,
        *,
        base_dir: Path,
        search_root: Path,
        klass: type[T],
        namespace: str = "",
    ) -> None:
        self._base_dir = base_dir
        self._search_root = search_root
        self._klass = klass
        self._base_namespace = namespace

    def load(self) -> Generator[tuple[ModuleType, str, type[T]], None, None]:
        if not self._search_root.exists():
            raise PokeControllerDynamicClassLoaderException(
                f"{self._search_root} is not found."
            )

        for py_file in self._search_root.rglob("*.py"):
            if py_file.name.startswith("_"):
                continue

            try:
                module = self._load_module_from_file(py_file)
                yield from self._load_class_from_module(module)
            except PokeControllerDynamicClassLoaderException as e:
                logger.warning(f"Failed to load command from {py_file}: {e}")
                continue

    def _load_module_from_file(self, file_path: Path) -> ModuleType:
        # construct module name
        relative_path = file_path.relative_to(self._base_dir)
        parts = list(relative_path.with_suffix("").parts)
        if self._base_namespace:
            parts.insert(0, self._base_namespace)
        module_name = ".".join(parts)

        # remove existing module for clean reload
        if module_name in sys.modules:
            logger.debug(f"Removing module {module_name}")
            del sys.modules[module_name]

        # load module
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None or spec.loader is None:
            logger.warning(f"Cannot load module from {file_path}")
            raise PokeControllerDynamicClassLoaderException(
                f"Cannot load module from {file_path}"
            )

        # execute module
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        try:
            spec.loader.exec_module(module)
        except Exception as e:
            sys.modules.pop(module_name, None)
            raise PokeControllerDynamicClassLoaderException(
                f"Failed to execute module from {file_path}: {e}"
            ) from e

        return module

    def _load_class_from_module(
        self, module: ModuleType
    ) -> Generator[tuple[ModuleType, str, type[T]], None, None]:
        for name, obj in inspect.getmembers(module, inspect.isclass):
            try:
                if obj is self._klass:
                    continue
                if not issubclass(obj, self._klass):
                    continue
                yield module, name, obj
            except TypeError:
                continue
