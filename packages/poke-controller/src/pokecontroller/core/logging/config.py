import logging
import logging.config
import os
import tomllib

from .. import path

# FIXME: PR出す前にロギングの調整する
DEFAULT_TOML: str = """# See: https://docs.python.org/ja/3.12/howto/logging.html

version = 1
disable_existing_loggers = false

# formatters
[formatters.pokecontroller]
format = "%(asctime)s [%(levelname)8s] %(name)s#%(funcName)s: %(message)s"
datefmt = "%Y-%m-%d %H:%M:%S"

[formatters.pokecontrollerColored]
class = "pokecontroller.core.logging.ColoredFormatter"
format = "%(asctime)s [%(levelname)8s] %(name)s#%(funcName)s: %(message)s"
datefmt = "%Y-%m-%d %H:%M:%S"

# handlers
[handlers.pokecontrollerConsole]
class = "logging.StreamHandler"
level = "DEBUG"
formatter = "pokecontrollerColored"
stream = "ext://sys.stdout"

[handlers.pokecontrollerFileWarning]
class = "logging.handlers.TimedRotatingFileHandler"
level = "WARNING"
formatter = "pokecontroller"
filters = []
filename = "log/warning.log"
when = "midnight"
backupCount = 10
encoding = "utf-8"

[handlers.pokecontrollerFileDebug]
class = "logging.handlers.TimedRotatingFileHandler"
level = "DEBUG"
formatter = "pokecontroller"
filters = []
filename = "log/debug.log"
when = "midnight"
backupCount = 10
encoding = "utf-8"

# loggers
[loggers.pokecontroller]
level = "DEBUG"
handlers = [
    "pokecontrollerConsole",
    "pokecontrollerFileWarning",
    "pokecontrollerFileDebug",
]
"""


def setup_logging(config_path: str | None = None) -> None:
    if config_path is None:
        _apply_defaults()
    elif path.exists_file(config_path):
        _load_from_file(config_path)
    else:
        raise FileNotFoundError(
            os.linesep.join(
                [
                    f"Logging config file not found: {config_path}",
                    "To generate a default config file, run:",
                    f"python -m pokecontroller.core.logging.config {config_path}",  # FIXME: command
                ]
            )
        )


def generate_default_config(output_path: str, force: bool = False) -> None:
    if path.exists_file(output_path) and not force:
        raise FileExistsError(
            os.linesep.join(
                [
                    f"Config file already exists: {output_path}.",
                    "Use --force to overwrite it.",
                ]
            )
        )

    _save_to_file(output_path, DEFAULT_TOML)


def _load_from_file(config_path: str, encoding: str | None = "utf-8-sig") -> None:
    logging.config.fileConfig(config_path, encoding=encoding)


# FIXME: 後回し
def _save_to_file(config_path: str, conf_str: str) -> None: ...


def _apply_defaults() -> None:
    logging.config.dictConfig(tomllib.loads(DEFAULT_TOML))
