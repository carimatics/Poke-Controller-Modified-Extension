import tkinter as tk
import tkinter.ttk as ttk
from typing import Any, Literal

type SizeType = Literal["xs", "s", "md", "l", "xl"]
type OrientType = Literal["horizontal", "vertical"]


class Scrollbar(ttk.Scrollbar):
    def __init__(
        self,
        master: tk.Misc,
        *,
        size: SizeType = "md",
        orient: OrientType = "vertical",
        **kwargs: Any,
    ) -> None:
        self._pokecon_style = self._construct_style(size)
        kwargs["style"] = self._pokecon_style
        kwargs["orient"] = orient
        super().__init__(master, **kwargs)
        self._pokecon_size = size
        self._pokecon_orient = orient

    def configure_style(self, *, size: SizeType) -> None:
        self._pokecon_style = self._construct_style(size)
        self.configure(style=self._pokecon_style)

    def _construct_style(self, size: SizeType) -> str:
        styles = ["PokeController"]
        if size != "md":
            styles.append(size.capitalize())
        if self._pokecon_orient == "vertical":
            styles.append("Vertical")
        else:
            styles.append("Horizontal")
        styles.append("TScrollbar")
        return ".".join(styles)
