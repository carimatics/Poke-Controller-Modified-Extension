import logging
import logging.config
import os
import sys
import tomllib
from typing import Any

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
level = "WARNING"
formatter = "pokecontroller"
filters = []
filename = "log/pokecontroller.log"
when = "midnight"
backupCount = 10
encoding = "utf-8"

# loggers
[loggers.pokecontroller]
level = "INFO"
handlers = [
    "pokecontrollerConsole",
    "pokecontrollerFile",
]
""".strip()


def setup_logging(
    config_path: str | None = None,
    *,
    debug: bool | None = None,
    show_config: bool | None = False,
) -> None:
    """
    Python標準のloggingモジュールを設定する

    Args:
        config_path: 設定ファイル(toml形式)のパス
        debug: Trueの場合、登録済みのLogger、HandlerをロギングレベルをDEBUGレベルに設定する
        show_config: Trueの場合、現在の設定を標準出力に表示します
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

    if show_config:
        _show_current_config()


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

    func_logger = logging.getLogger(__name__)
    func_logger.setLevel(logging.DEBUG)

    def _log_logger(target: logging.Logger) -> None:
        func_logger.debug(f"Logger: '{target.name}' to DEBUG level.")

    def _log_handler(target_logger: logging.Logger, target: logging.Handler) -> None:
        func_logger.debug(
            f"Handler: '{target_logger.name}#{target.name}' to DEBUG leve."
        )

    # root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    _log_logger(root_logger)

    # all handers
    for handler in root_logger.handlers:
        handler.setLevel(logging.DEBUG)
        _log_handler(root_logger, handler)

    # all loggers
    for logger_name in logging.Logger.manager.loggerDict:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        _log_logger(logger)
        for handler in logger.handlers:
            handler.setLevel(logging.DEBUG)
            _log_handler(logger, handler)

    logging.getLogger(__name__).debug(
        "Debug mode enabled: All loggers set to DEBUG level."
    )


def _show_current_config() -> None:
    """現在のロギング設定を標準出力に表示"""
    print("\n" + "=" * 60)
    print("Logging Configuration")
    print("=" * 60)

    # Root logger
    root_logger = logging.getLogger()
    print("\n[Root Logger]")
    print(f"  Level: {logging.getLevelName(root_logger.level)}")
    print(f"  Handlers: {len(root_logger.handlers)}")
    print(f"  Filters: {len(root_logger.filters)}")

    # Root logger's filters
    if root_logger.filters:
        for i, filter_obj in enumerate(root_logger.filters):
            _print_filter(filter_obj, i, indent=4)

    # Root logger's handlers
    for i, handler in enumerate(root_logger.handlers):
        _print_handler(handler, i, indent=4)

    # Registered loggers
    logger_dict = logging.Logger.manager.loggerDict
    actual_loggers = {
        name: obj
        for name, obj in logger_dict.items()
        if isinstance(obj, logging.Logger)
    }

    if actual_loggers:
        print(f"\n[Registered Loggers] ({len(actual_loggers)} total)")
        for logger_name in sorted(actual_loggers.keys()):
            logger = logging.getLogger(logger_name)
            print(f"  '{logger_name}'")
            print(f"    Level: {logging.getLevelName(logger.level)}")
            print(f"    Propagate: {logger.propagate}")
            print(f"    Filters: {len(logger.filters)}")

            # Logger's filters
            if logger.filters:
                for i, filter_obj in enumerate(logger.filters):
                    _print_filter(filter_obj, i, indent=6)

            # Logger's handlers
            if logger.handlers:
                print(f"    Handlers: {len(logger.handlers)}")
                for i, handler in enumerate(logger.handlers):
                    _print_handler(handler, i, indent=6)

    print("=" * 60 + "\n")


def _print_handler(handler: logging.Handler, index: int, indent: int = 0) -> None:
    """ハンドラー情報を表示"""
    prefix = " " * indent
    print(f"{prefix}[{index}] {handler.__class__.__name__}")
    print(f"{prefix}    Level: {logging.getLevelName(handler.level)}")

    # ファイルハンドラーの場合はファイル名も表示
    if hasattr(handler, "baseFilename"):
        print(f"{prefix}    File: {handler.baseFilename}")

    # ストリームハンドラーの場合はストリーム情報
    if hasattr(handler, "stream"):
        stream = handler.stream
        if hasattr(stream, "name"):
            print(f"{prefix}    Stream: {stream.name}")
        else:
            print(f"{prefix}    Stream: {type(stream).__name__}")

    # フォーマッター情報
    if handler.formatter:
        _print_formatter(handler.formatter, indent=indent + 4)
    else:
        print(f"{prefix}    Formatter: None")

    # フィルター情報
    if handler.filters:
        print(f"{prefix}    Filters: {len(handler.filters)}")
        for i, filter_obj in enumerate(handler.filters):
            _print_filter(filter_obj, i, indent=indent + 6)
    else:
        print(f"{prefix}    Filters: 0")


def _print_formatter(formatter: logging.Formatter, indent: int = 0) -> None:
    """フォーマッター情報を表示"""
    prefix = " " * indent
    print(f"{prefix}Formatter: {formatter.__class__.__name__}")

    # フォーマット文字列
    if hasattr(formatter, "_fmt"):
        fmt = formatter._fmt
    else:
        fmt = None

    if fmt:
        print(f"{prefix}  Format: {fmt}")

    # 日付フォーマット
    if formatter.datefmt:
        print(f"{prefix}  DateFormat: {formatter.datefmt}")

    # カスタムフォーマッターの追加属性（ColoredFormatterなど）
    if hasattr(formatter, "use_colors"):
        print(f"{prefix}  UseColors: {formatter.use_colors}")


def _print_filter(filter_obj: Any, index: int, indent: int = 0) -> None:
    """フィルター情報を表示"""
    prefix = " " * indent

    # フィルタークラス名
    filter_class = filter_obj.__class__.__name__
    print(f"{prefix}[{index}] {filter_class}")

    # 標準のFilterの場合はnameを表示
    if isinstance(filter_obj, logging.Filter) and hasattr(filter_obj, "name"):
        if filter_obj.name:
            print(f"{prefix}    Name: {filter_obj.name}")

    # カスタムフィルターの場合、主要な属性を表示
    # __dict__から内部属性(_で始まるもの)を除外して表示
    custom_attrs = {
        k: v
        for k, v in filter_obj.__dict__.items()
        if not k.startswith("_") and k != "name"
    }
    if custom_attrs:
        for key, value in custom_attrs.items():
            value_str = str(value)
            print(f"{prefix}    {key}: {value_str}")
