import tkinter as tk
import tkinter.ttk as ttk
from dataclasses import dataclass, field
from typing import Any

from pokecontroller.utils import platform
from pokecontroller.utils.collection import deep_merge


@dataclass
class VariantStyle:
    base: dict[str, Any] = field(default_factory=dict)
    primary: dict[str, Any] = field(default_factory=dict)
    success: dict[str, Any] = field(default_factory=dict)
    warning: dict[str, Any] = field(default_factory=dict)
    error: dict[str, Any] = field(default_factory=dict)

    def to_dict(self, class_name: str) -> dict[str, Any]:
        result = {class_name: self.base}
        if self.primary:
            result[f"Primary.{class_name}"] = deep_merge(self.base, self.primary)
        if self.success:
            result[f"Success.{class_name}"] = deep_merge(self.base, self.success)
        if self.warning:
            result[f"Warning.{class_name}"] = deep_merge(self.base, self.warning)
        if self.error:
            result[f"Error.{class_name}"] = deep_merge(self.base, self.error)
        return result


@dataclass
class VariantStyleSettings:
    button: VariantStyle = field(default_factory=VariantStyle)
    label: VariantStyle = field(default_factory=VariantStyle)
    entry: VariantStyle = field(default_factory=VariantStyle)
    combobox: VariantStyle = field(default_factory=VariantStyle)
    spinbox: VariantStyle = field(default_factory=VariantStyle)
    radiobutton: VariantStyle = field(default_factory=VariantStyle)
    checkbutton: VariantStyle = field(default_factory=VariantStyle)
    scale: VariantStyle = field(default_factory=VariantStyle)
    frame: VariantStyle = field(default_factory=VariantStyle)
    labelframe: VariantStyle = field(default_factory=VariantStyle)

    def to_dict(self) -> dict[str, Any]:
        return {
            **self.button.to_dict("TButton"),
            **self.label.to_dict("TLabel"),
            **self.entry.to_dict("TEntry"),
            **self.combobox.to_dict("TCombobox"),
            **self.spinbox.to_dict("TSpinbox"),
            **self.radiobutton.to_dict("TRadiobutton"),
            **self.checkbutton.to_dict("TCheckbutton"),
            **self.scale.to_dict("TScale"),
            **self.frame.to_dict("TFrame"),
            **self.labelframe.to_dict("TLabelframe"),
        }


class StyleManager:
    _root: tk.Tk
    _style: ttk.Style
    _os_name: str
    _base_style: VariantStyleSettings
    _theme_styles: dict[str, VariantStyleSettings]

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
            s = deep_merge(self._base_style.to_dict(), settings.to_dict())
            self._style.theme_settings(theme, s)

    def _initialize_fundamental_styles(self) -> None:
        self._base_style = VariantStyleSettings()

    def _initialize_styles_for_windows(self) -> None:
        self._theme_styles = {
            "clam": VariantStyleSettings(),
            "default": VariantStyleSettings(),
            "alt": VariantStyleSettings(),
            "classic": VariantStyleSettings(),
        }

    def _initialize_styles_for_macos(self) -> None:
        self._theme_styles = {
            "aqua": VariantStyleSettings(),
            "clam": VariantStyleSettings(),
            "default": VariantStyleSettings(),
            "alt": VariantStyleSettings(),
            "classic": VariantStyleSettings(),
        }

    def _initialize_styles_for_linux(self) -> None:
        self._theme_styles = {
            "clam": VariantStyleSettings(),
            "default": VariantStyleSettings(),
            "alt": VariantStyleSettings(),
            "classic": VariantStyleSettings(),
        }
