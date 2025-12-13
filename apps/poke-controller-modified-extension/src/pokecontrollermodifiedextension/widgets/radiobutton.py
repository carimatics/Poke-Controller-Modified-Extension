import tkinter as tk
import tkinter.ttk as ttk
from typing import Any, Literal

type SizeType = Literal["xs", "s", "md", "l", "xl"]


class Radiobutton(ttk.Radiobutton):
    def __init__(
        self,
        master: tk.Misc,
        *,
        size: SizeType = "md",
        **kwargs: Any,
    ) -> None:
        self._pokecon_style = self._construct_style(size)
        kwargs["style"] = self._pokecon_style
        super().__init__(master, **kwargs)
        self._pokecon_size = size

    def configure_style(self, *, size: SizeType) -> None:
        self._pokecon_style = self._construct_style(size)
        self.configure(style=self._pokecon_style)

    @staticmethod
    def _construct_style(size: SizeType) -> str:
        styles = ["PokeController"]
        if size != "md":
            styles.append(size.capitalize())
        styles.append("TRadiobutton")
        return ".".join(styles)
