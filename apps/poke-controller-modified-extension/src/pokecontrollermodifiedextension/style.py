import tkinter as tk
import tkinter.ttk as ttk
from dataclasses import dataclass, field
from typing import Any

from pokecontroller.utils import platform
from pokecontroller.utils.collection import deep_merge


@dataclass
class ThemeStyleSettings:
    button: dict[str, Any] = field(default_factory=dict)
    label: dict[str, Any] = field(default_factory=dict)
    entry: dict[str, Any] = field(default_factory=dict)
    combobox: dict[str, Any] = field(default_factory=dict)
    spinbox: dict[str, Any] = field(default_factory=dict)
    radiobutton: dict[str, Any] = field(default_factory=dict)
    checkbutton: dict[str, Any] = field(default_factory=dict)
    scale: dict[str, Any] = field(default_factory=dict)
    frame: dict[str, Any] = field(default_factory=dict)
    labelframe: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "TButton": self.button,
            "TLabel": self.label,
            "TEntry": self.entry,
            "TCombobox": self.combobox,
            "TSpinbox": self.spinbox,
            "TRadiobutton": self.radiobutton,
            "TCheckbutton": self.checkbutton,
            "TScale": self.scale,
            "TFrame": self.frame,
            "TLabelFrame": self.labelframe,
        }


class StyleManager:
    _root: tk.Tk
    _style: ttk.Style
    _os_name: str
    _fundamental_styles: ThemeStyleSettings
    _theme_styles: dict[str, ThemeStyleSettings]

    def __init__(self, root: tk.Tk) -> None:
        self._root = root
        self._style = ttk.Style(self._root)
        self._os_name = platform.get_name()
        self._theme_styles = {}
        self._initialize_styles()
        self._setup_all_themes()

    @property
    def root(self) -> tk.Tk:
        return self._root

    @property
    def style(self) -> ttk.Style:
        return self._style

    @property
    def os_name(self) -> str:
        return self._os_name

    def change_theme(self, theme: str) -> None:
        self._style.theme_use(theme)

    def get_themes(self) -> tuple[str, ...]:
        return self._style.theme_names()

    def _initialize_styles(self) -> None:
        self._initialize_fundamental_styles()
        if platform.is_windows():
            self._initialize_styles_for_windows()
        elif platform.is_macos():
            self._initialize_styles_for_macos()
        elif platform.is_linux():
            self._initialize_styles_for_linux()
        else:
            raise RuntimeError(f"Unsupported OS: {self._os_name}")

    def _setup_all_themes(self) -> None:
        for theme, settings in self._theme_styles.items():
            s = deep_merge(self._fundamental_styles.to_dict(), settings.to_dict())
            self._style.theme_settings(theme, s)

    def _initialize_fundamental_styles(self) -> None:
        self._fundamental_styles = ThemeStyleSettings()

    def _initialize_styles_for_windows(self) -> None:
        self._theme_styles = {
            "clam": ThemeStyleSettings(),
            "default": ThemeStyleSettings(),
            "alt": ThemeStyleSettings(),
            "classic": ThemeStyleSettings(),
        }

    def _initialize_styles_for_macos(self) -> None:
        self._theme_styles = {
            "aqua": ThemeStyleSettings(),
            "clam": ThemeStyleSettings(),
            "default": ThemeStyleSettings(),
            "alt": ThemeStyleSettings(),
            "classic": ThemeStyleSettings(),
        }

    def _initialize_styles_for_linux(self) -> None:
        self._theme_styles = {
            "clam": ThemeStyleSettings(),
            "default": ThemeStyleSettings(),
            "alt": ThemeStyleSettings(),
            "classic": ThemeStyleSettings(),
        }
