import tkinter as tk
import tkinter.ttk as ttk
from typing import Any, Literal

type VariantType = Literal["base", "primary", "error", "success", "warning"]
type SizeType = Literal["xs", "s", "md", "l", "xl"]


class Button(ttk.Button):
    def __init__(
        self,
        master: tk.Misc,
        *,
        variant: VariantType = "base",
        size: SizeType = "md",
        **kwargs: Any,
    ) -> None:
        self._pokecon_style = self._construct_style(variant, size)
        kwargs["style"] = self._pokecon_style
        super().__init__(master, **kwargs)
        self._pokecon_size = size
        self._pokecon_variant = variant

    def configure_style(
        self,
        *,
        variant: VariantType | None = None,
        size: SizeType | None = None,
    ) -> None:
        if variant is None:
            variant = self._pokecon_variant
        if size is None:
            size = self._pokecon_size
        style = self._construct_style(variant, size)
        self.configure(style=style)
        self._pokecon_style = style
        self._pokecon_size = size
        self._pokecon_variant = variant

    @staticmethod
    def _construct_style(
        variant: VariantType,
        size: SizeType,
    ) -> str:
        styles = ["PokeController"]
        if size != "md":
            styles.append(size.capitalize())
        if variant != "base":
            styles.append(variant.capitalize())
        styles.append("TButton")
        return ".".join(styles)
