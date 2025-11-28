import logging
import os
import sys

from ...platform import is_windows


class ColoredFormatter(logging.Formatter):
    """クロスプラットフォーム対応のカラーフォーマッター"""

    COLORS = {
        "DEBUG": "   \033[36m",  # Cyan
        "INFO": "    \033[32m",  # Green
        "WARNING": " \033[33m",  # Yellow
        "ERROR": "   \033[31m",  # Red
        "CRITICAL": "\033[37;41m",  # White on Red
    }
    MAPPING = {level: f"{esc}{level}\033[0m" for level, esc in COLORS.items()}

    def __init__(
        self,
        fmt: str | None = None,
        datefmt: str | None = None,
        use_colors: bool | None = None,
    ) -> None:
        super().__init__(fmt=fmt, datefmt=datefmt)

        if use_colors is None:
            self.use_colors = self._should_use_colors()
        else:
            self.use_colors = use_colors

        if self.use_colors and is_windows():
            self._enable_window_ansi()

    # noinspection PyMethodMayBeStatic
    def _should_use_colors(self) -> bool:
        """色を使用するべきか判定する"""

        if os.getenv("NO_COLOR"):
            return False
        if os.getenv("FORCE_COLOR"):
            return True
        if not hasattr(sys.stdout, "isatty") or not sys.stdout.isatty():
            return False
        if os.getenv("CI"):
            return False
        return True

    def _enable_window_ansi(self) -> None:
        """Windows 10以降でANSIエスケープシーケンスを有効化"""
        try:
            # Windows 10 バージョン1511以降で利用可能
            import ctypes

            kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
            # STD_OUTPUT_HANDLE = -11
            handle = kernel32.GetStdHandle(-11)  # noqa
            # ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
            mode = ctypes.c_ulong()
            kernel32.GetConsoleMode(handle, ctypes.byref(mode))  # noqa
            mode.value |= 0x0004
            kernel32.SetConsoleMode(handle, mode)  # noqa
        except Exception:  # noqa
            # 失敗しても続行(色なし)
            self.use_color = False

    def format(self, record: logging.LogRecord) -> str:
        """ログレコードをフォーマット"""
        if not self.use_colors:
            return super().format(record)

        levelname_original = record.levelname
        if levelname_original not in self.MAPPING:
            return super().format(record)

        record.levelname = self.MAPPING[levelname_original]
        result = super().format(record)
        # 元に戻す(他のHandlerに影響を与えないため)
        record.levelname = levelname_original
        return result
