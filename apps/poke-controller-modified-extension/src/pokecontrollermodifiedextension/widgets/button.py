import tkinter as tk
import tkinter.ttk as ttk
from typing import Any, Literal

from ..mixins.tooltip import TooltipMixIn

type VariantType = Literal["base", "primary", "error", "success", "warning"]
type SizeType = Literal["xs", "s", "md", "l", "xl"]


class Button(TooltipMixIn, ttk.Button):
    def __init__(
        self,
        master: tk.Misc,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self._pokecon_variant = variant = kwargs.pop("variant", "base")
        self._pokecon_size = size = kwargs.pop("size", "md")
        self._pokecon_style = self._construct_style(variant, size)
        kwargs["style"] = self._pokecon_style
        super().__init__(master, *args, **kwargs)

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
