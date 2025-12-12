import tkinter as tk
import tkinter.ttk as ttk
from dataclasses import dataclass, field
from typing import Any

from pokecontroller.utils import platform
from pokecontroller.utils.collection import deep_merge


@dataclass
class ComponentStyle:
    base: dict[str, Any] = field(default_factory=dict)
    variants: dict[str, dict[str, Any]] = field(default_factory=dict)
    sizes: dict[str, dict[str, Any]] = field(default_factory=dict)

    def to_dict(self, class_name: str) -> dict[str, Any]:
        result: dict[str, Any] = {f"PokeController.{class_name}": self.base}

        for variant_name, variant_style in self.variants.items():
            if variant_style:
                k = f"PokeController.{variant_name.capitalize()}.{class_name}"
                result[k] = deep_merge(self.base, variant_style)

        for size_name, size_style in self.sizes.items():
            if size_style:
                k = f"PokeController.{size_name.capitalize()}.{class_name}"
                result[k] = deep_merge(self.base, size_style)

        for variant_name, variant_style in self.variants.items():
            for size_name, size_style in self.sizes.items():
                if variant_style and size_style:
                    k = f"PokeController.{size_name.capitalize()}.{variant_name.capitalize()}.{class_name}"
                    merged = deep_merge(self.base, size_style)
                    merged = deep_merge(merged, variant_style)
                    result[k] = merged

        return result


@dataclass
class StyleSettings:
    button: ComponentStyle = field(default_factory=ComponentStyle)
    text: ComponentStyle = field(default_factory=ComponentStyle)
    label: ComponentStyle = field(default_factory=ComponentStyle)
    entry: ComponentStyle = field(default_factory=ComponentStyle)
    combobox: ComponentStyle = field(default_factory=ComponentStyle)
    spinbox: ComponentStyle = field(default_factory=ComponentStyle)
    radiobutton: ComponentStyle = field(default_factory=ComponentStyle)
    checkbutton: ComponentStyle = field(default_factory=ComponentStyle)
    scale: ComponentStyle = field(default_factory=ComponentStyle)
    frame: ComponentStyle = field(default_factory=ComponentStyle)
    labelframe: ComponentStyle = field(default_factory=ComponentStyle)
    scrollbar: ComponentStyle = field(default_factory=ComponentStyle)

    def to_dict(self) -> dict[str, Any]:
        return {
            **self.button.to_dict("Button"),
            **self.text.to_dict("Text"),
            **self.label.to_dict("Label"),
            **self.entry.to_dict("Entry"),
            **self.combobox.to_dict("Combobox"),
            **self.spinbox.to_dict("Spinbox"),
            **self.radiobutton.to_dict("Radiobutton"),
            **self.checkbutton.to_dict("Checkbutton"),
            **self.scale.to_dict("Scale"),
            **self.frame.to_dict("Frame"),
            **self.labelframe.to_dict("Labelframe"),
            **self.scrollbar.to_dict("Scrollbar"),
        }


class StyleManager:
    _root: tk.Tk
    _style: ttk.Style
    _os_name: str
    _base_style: StyleSettings
    _theme_styles: dict[str, StyleSettings]

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
        self._base_style = StyleSettings()

    def _initialize_styles_for_windows(self) -> None:
        self._theme_styles = {
            "clam": StyleSettings(),
            "default": StyleSettings(),
            "alt": StyleSettings(),
            "classic": StyleSettings(),
        }

    def _initialize_styles_for_macos(self) -> None:
        self._theme_styles = {
            "aqua": StyleSettings(),
            "clam": StyleSettings(),
            "default": StyleSettings(),
            "alt": StyleSettings(),
            "classic": StyleSettings(),
        }

    def _initialize_styles_for_linux(self) -> None:
        self._theme_styles = {
            "clam": StyleSettings(),
            "default": StyleSettings(),
            "alt": StyleSettings(),
            "classic": StyleSettings(),
        }
