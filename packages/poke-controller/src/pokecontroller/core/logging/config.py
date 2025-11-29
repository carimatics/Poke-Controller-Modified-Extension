import logging
import logging.config
import os
import sys
import tomllib

from .. import path

# FIXME: PR出す前にロギングの調整する
DEFAULT_TOML: str = """
# 注意:
# Python標準のloggingモジュールにおけるロギング設定を理解している場合のみ編集してください。
# また、アプリケーションのデフォルトの設定は将来変更される可能性があります。
# See: https://docs.python.org/ja/3.12/howto/logging.html

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
level = "INFO"
formatter = "pokecontrollerColored"
stream = "ext://sys.stdout"

[handlers.pokecontrollerFile]
class = "logging.handlers.TimedRotatingFileHandler"
formatter = "pokecontroller"
filters = []
filename = "log/debug.log"
when = "midnight"
backupCount = 10
encoding = "utf-8"

# loggers
[loggers.pokecontroller]
level = "WARNING"
handlers = [
    "pokecontrollerConsole",
    "pokecontrollerFile",
]
""".strip()


def setup_logging(config_path: str | None = None, debug: bool | None = None) -> None:
    """
    Python標準のloggingモジュールの設定を行う

    Args:
        config_path: 設定ファイル(toml形式)のパス
        debug: Trueの場合、デバッグモードでの設定を行う
    """
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

    if _should_enable_debug(debug=debug):
        _enable_debug_mode()


def generate_default_config(output_path: str, force: bool = False) -> None:
    """
    output_pathにデフォルト設定の設定ファイル(toml形式)を作成する

    Args:
        output_path: 設定ファイルの出力先のパス
        force: Trueの場合、設定ファイルが存在する場合に上書きする
    """
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
    """設定ファイルから設定を読み込む"""
    logging.config.fileConfig(config_path, encoding=encoding)


# FIXME: 後回し
def _save_to_file(config_path: str, conf_str: str) -> None: ...


def _apply_defaults() -> None:
    """デフォルト設定を適用"""
    logging.config.dictConfig(tomllib.loads(DEFAULT_TOML))


def _should_enable_debug(debug: bool | None = None) -> bool:
    """デバッグモードを有効にすべきか判定"""

    # 明示的に指定された場合はそれに従う
    if debug is not None:
        return debug

    # 環境変数をチェック
    if os.getenv("DEBUG", "").lower() in ("1", "true", "yes"):
        return True

    # -X dev フラグをチェック
    if sys.flags.dev_mode:
        return True

    return False


def _enable_debug_mode() -> None:
    """すべてのロガーをDEBUGレベルに設定"""

    # root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # all handers
    for handler in root_logger.handlers:
        handler.setLevel(logging.DEBUG)

    # all loggers
    for logger_name in logging.Logger.manager.loggerDict:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        logger.debug(f"Logger '{logger_name}' to DEBUG level.")
        for handler in logger.handlers:
            handler.setLevel(logging.DEBUG)
            logger.debug(f"Handler '{logger_name}#{handler.name}' to DEBUG level.")

    logging.getLogger(__name__).debug(
        "Debug mode enabled: All loggers set to DEBUG level."
    )
