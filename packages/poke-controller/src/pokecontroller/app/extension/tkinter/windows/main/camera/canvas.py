from typing import Any
import tkinter as tk

from ....components import AppFrame


class Canvas(AppFrame):
    def __init__(self, master: tk.Misc, *args: Any, **kwargs: Any) -> None:
        super().__init__(master, *args, **kwargs)
