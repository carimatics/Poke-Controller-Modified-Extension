import configparser
import os

from .. import path as libpath


class Config:
    def __init__(self, path: str) -> None:
        self._path: str = path
        self._config: configparser.ConfigParser = configparser.ConfigParser(
            allow_no_value=True
        )

    def load(self, encoding: str | None = "utf-8-sig") -> None:
        if not libpath.exists_file(self._path):
            raise FileNotFoundError(self._path)
        self._config.read(self._path, encoding=encoding)

    def save(
        self,
        *,
        encoding: str | None = "utf-8",
        chmod: int | None = None,
        create_directory: bool = True,
    ) -> None:
        self._check_exists_directory(create_directory)
        with open(self._path, mode="w", encoding=encoding) as file:
            self._config.write(file)
        if chmod is not None:
            os.chmod(path=self._path, mode=chmod)

    def get(self, section: str, option: str, default: str | None = None) -> str | None:
        value = self._config.get(section, option)
        return value if value is not None else default

    def get_boolean(
        self,
        section: str,
        option: str,
        default: bool | None = None,
    ) -> bool | None:
        value = self._config.getboolean(section, option)
        return value if value is not None else default

    def get_int(
        self,
        section: str,
        option: str,
        default: int | None = None,
    ) -> int | None:
        value = self._config.getint(section, option)
        return value if value is not None else default

    def get_float(
        self,
        section: str,
        option: str,
        default: float | None = None,
    ) -> float | None:
        value = self._config.getfloat(section, option)
        return value if value is not None else default

    def set(self, section: str, option: str, value: str) -> None:
        self._config.set(section, option, value)

    def sections(self) -> list[str]:
        return list(self._config.keys())

    def keys(self, section: str) -> list[str]:
        return list(self._config[section].keys())

    def read_dict(self, section: str) -> dict[str, str]:
        return dict(self._config[section])

    def _check_exists_directory(self, should_create: bool) -> None:
        directory = libpath.directory_name(self._path)
        exists_dir = libpath.exists(directory) and libpath.exists_directory(directory)
        if not exists_dir and not should_create:
            # FIXME: declare better error
            raise FileNotFoundError(directory)
        libpath.make_directory(directory)
