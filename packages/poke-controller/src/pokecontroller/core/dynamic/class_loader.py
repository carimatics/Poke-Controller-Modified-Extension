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
    def __init__(self, *, base_dir: Path, klass: type[T], namespace: str = "") -> None:
        self.klass = klass
        self.base_namespace = namespace
        self.base_dir = base_dir

    def load(self) -> Generator[type[T], None, None]:
        if not self.base_dir.exists():
            raise PokeControllerDynamicClassLoaderException(
                f"{self.base_dir} is not found."
            )

        for py_file in self.base_dir.rglob("*.py"):
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
        relative_path = file_path.relative_to(self.base_dir)
        parts = list(relative_path.with_suffix("").parts)
        if self.base_namespace:
            parts.insert(0, self.base_namespace)
        module_name = ".".join(parts)

        # reload module if already exists
        if module_name in sys.modules:
            return importlib.reload(sys.modules[module_name])

        # load module
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None or spec.loader is None:
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
    ) -> Generator[type[T], None, None]:
        for name, obj in inspect.getmembers(module, inspect.isclass):
            try:
                if issubclass(obj, self.klass) and obj is not self.klass:
                    yield obj
            except TypeError:
                continue
