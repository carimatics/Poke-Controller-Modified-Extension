import tkinter as tk
import tkinter.ttk as ttk

from typing import Any
from ..mixins import AppAccessorMixIn


class AppFrame(ttk.Frame, AppAccessorMixIn):
    def __init__(
        self,
        master: tk.Misc,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
    ):
        super().__init__(master, *args, **kwargs)  # type: ignore[arg-type]
