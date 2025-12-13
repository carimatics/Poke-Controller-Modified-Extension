import tkinter as tk
import tkinter.ttk as ttk
from typing import Any, Callable, Literal

type SizeType = Literal["xs", "s", "md", "l", "xl"]


class Labelframe(ttk.Labelframe):
    def __init__(
        self,
        master: tk.Misc,
        *,
        size: SizeType = "md",
        **kwargs: Any,
    ) -> None:
        self._pokecon_size = size
        self._pokecon_style = self._construct_style(size)
        kwargs["style"] = self._pokecon_style
        super().__init__(master, **kwargs)

        self._trace_ids: list[
            tuple[tk.Variable, Literal["array", "read", "write", "unset"], str]
        ] = []

    def configure_style(self, *, size: SizeType) -> None:
        self._pokecon_style = self._construct_style(size)
        self.configure(style=self._pokecon_style)

    def register_trace(
        self,
        mode: Literal["write"],
        variable: tk.Variable,
        callback: Callable[[str, str, str], Any],
    ) -> None:
        self._trace_ids.append((variable, mode, variable.trace_add(mode, callback)))

    def destroy(self) -> None:
        self._unregister_traces()
        super().destroy()

    def _unregister_traces(self) -> None:
        for variable, mode, trace_id in self._trace_ids:
            variable.trace_remove(mode, trace_id)

    @staticmethod
    def _construct_style(size: SizeType) -> str:
        styles = ["PokeController"]
        if size != "md":
            styles.append(size.capitalize())
        styles.append("TLabelframe")
        return ".".join(styles)
