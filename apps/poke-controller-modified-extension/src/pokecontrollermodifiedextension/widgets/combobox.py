import tkinter as tk
import tkinter.ttk as ttk
from typing import Any, Literal

type SizeType = Literal["xs", "s", "md", "l", "xl"]


class Combobox(ttk.Combobox):
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

        self._disable_text_selection()

    def configure_style(self, *, size: SizeType) -> None:
        self._pokecon_style = self._construct_style(size)
        self.configure(style=self._pokecon_style)

    def _disable_text_selection(self) -> None:
        """Disable text selection in combobox."""
        self.bind("<<ComboboxSelected>>", lambda _: self.selection_clear)
        self.bind("<Button-1>", lambda _: self.after_idle(self.selection_clear))
        self.bind("<B1-Motion>", lambda _: "break")
        self.bind("<Double-Button-1>", lambda _: "break")
        self.bind("<Triple-Button-1>", lambda _: "break")
        self.bind("<Control-a>", lambda _: "break")

    @staticmethod
    def _construct_style(size: SizeType) -> str:
        styles = ["PokeController"]
        if size != "md":
            styles.append(size.capitalize())
        styles.append("TCombobox")
        return ".".join(styles)
