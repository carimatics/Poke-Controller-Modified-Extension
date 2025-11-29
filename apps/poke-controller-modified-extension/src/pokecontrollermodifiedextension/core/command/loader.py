import glob
import importlib
import logging
import inspect
import os
import sys
from os import PathLike
from os.path import relpath
from pathlib import Path
from types import ModuleType
from pokecontroller.core.path import join

logger = logging.getLogger(__name__)


class CommandLoader[T]:
    def __init__(self, base_path: str | PathLike[T], base_class: type[T]) -> None:
        self.path: Path = Path(base_path)
        self.base_type: type[T] = base_class
        self.modules: list[ModuleType] = []

    def load(self) -> list[type[T]]:
        """指定ディレクトリからCommandクラスを動的に読み込む"""
        if not self.path.exists():
            raise FileNotFoundError(f"Commands directory not found:  {self.path}")

        if self.modules:
            module_names = self._load_module_names()
            self.modules = self._load_modules(module_names)
        return self._get_command_classes()

    def reload(self) -> list[type[T]]:
        current_modules = {mod.__name__: mod for mod in self.modules}

        current_module_names = set(current_modules.keys())
        renewed_module_names = set(self._load_module_names())

        # Load only not loaded modules
        unloaded_module_names = list(renewed_module_names - current_module_names)
        if unloaded_module_names:
            self.modules.extend(self._load_modules(unloaded_module_names))

        # Reload commands except deleted ones
        old_module_names = list(renewed_module_names & current_module_names)
        for mod_name in old_module_names:
            importlib.reload(current_modules[mod_name])

        # Unload deleted commands
        deleted_module_names = list(current_module_names - renewed_module_names)
        for mod_name in deleted_module_names:
            self.modules.remove(current_modules[mod_name])
            # Un-import module forcefully
            sys.modules.pop(current_modules[mod_name].__name__)

        # return command class types
        return self._get_command_classes()

    def getCommandClasses(self):
        return self._get_command_classes()

    # noinspection PyMethodMayBeStatic
    def _load_modules(self, module_names: list[str]) -> list[ModuleType]:
        """self.path内の.pyファイルをモジュールとして読み込んで返す"""
        return [
            importlib.import_module(name)
            for name in module_names
        ]

    def _load_module_names(self) -> list[str]:
        """self.path内の.pyファイルをモジュール名を返す"""
        # globで検索するパスの構築
        search_path = join(str(self.path), "**", "*.py")

        return [
            # 相対パスから拡張子(.py)を除いてファイルの区切り文字をドット(.)に変換する
            (relpath(py_file)[:-3]).replace(os.sep, ".")
            for py_file in glob.glob(search_path, recursive=True)
        ]

    def _get_command_classes(self) -> list[type[T]]:
        """self.modulesからbase_typeクラスのサブクラスを取得する"""
        classes = []
        for mod in self.modules:
            class_list = [
                obj
                for _, obj in inspect.getmembers(mod, inspect.isclass)
                if (
                    issubclass(obj, self.base_type) and
                    obj is not self.base_type and
                    hasattr(obj, "NAME") and obj.NAME
                )
            ]

            # add TAGS
            for c in class_list:
                dir_name = "/".join(mod.__name__.split(".")[2:])
                dir_tags = ["@" + t for t in mod.__name__.split(".")[2:-1]]

                if hasattr(c, "TAGS"):
                    if isinstance(c.TAGS, list):
                        logger.debug(f"TAGS name add: {dir_tags}")
                        c.TAGS = c.TAGS + dir_tags
                    elif isinstance(c.TAGS, str):
                        logger.debug(f"TAGS name add: {dir_tags}")
                        c.TAGS = [c.TAGS] + dir_tags
                    else:
                        logger.debug(f"TAGS Type error: {mod.__name__} {c.NAME} {type(c.TAGS)}")
                else:
                    logger.debug(f"TAGS do not exist: {mod.__name__} {c.NAME}")
                    c.TAGS = dir_tags

                c.NAME = f"{c.NAME} ({dir_name})"
                classes.append(c)

        return classes
