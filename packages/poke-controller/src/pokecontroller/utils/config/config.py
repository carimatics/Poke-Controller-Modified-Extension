import configparser
import os
from pathlib import Path


class Config:
    def __init__(self, path: str) -> None:
        self._path: str = path
        self._config: configparser.ConfigParser = configparser.ConfigParser(
            allow_no_value=True,
            comment_prefixes=("#", ";"),
        )
        self._config.optionxform = str  # type: ignore[assignment]

    def __getitem__(self, section: str) -> configparser.SectionProxy:
        return self._config[section]

    def __setitem__(self, section: str, value: dict[str, str]) -> None:
        self._config[section] = value

    def load(self, encoding: str | None = "utf-8-sig") -> None:
        if not Path(self._path).exists():
            raise FileNotFoundError(self._path)
        self._config.read(self._path, encoding=encoding)

    def save(
        self,
        *,
        encoding: str | None = "utf-8",
        chmod: int | None = None,
        create_directory: bool = True,
    ) -> None:
        if not self._exists_directory() and create_directory:
            self._create_directories()

        with open(self._path, mode="w", encoding=encoding) as file:
            self._config.write(file)

        if chmod is not None:
            os.chmod(path=self._path, mode=chmod)

    def get(self, section: str, option: str, default: str | None = None) -> str | None:
        value = self._config[section][option]
        return value if value is not None else default

    def has_option(self, section: str, option: str) -> bool:
        return self._config.has_option(section, option)

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
        if not self._config.has_section(section):
            self._config.add_section(section)
        self._config[section][option] = value

    def sections(self) -> list[str]:
        return self._config.sections()

    def add_section(self, section: str) -> None:
        self._config.add_section(section)

    def options(self, section: str) -> dict[str, str]:
        return dict(self._config[section])

    def keys(self, section: str) -> list[str]:
        return list(self._config[section].keys())

    def _check_exists_directory(self, should_create: bool) -> None:
        directory = Path(self._path).parent
        exists_dir = self._exists_directory()
        if not exists_dir and not should_create:
            # FIXME: declare better error
            raise FileNotFoundError(directory)
        self._create_directories()

    def _exists_directory(self) -> bool:
        path = Path(self._path)
        directory = path.parent
        return directory.exists() and directory.is_dir()

    def _create_directories(self) -> None:
        directory = Path(self._path).parent
        directory.mkdir(parents=True, exist_ok=True)
