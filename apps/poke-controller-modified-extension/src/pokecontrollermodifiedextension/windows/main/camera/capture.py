import tkinter as tk
from typing import Any

from ....widgets import AppFrame


class Capture(AppFrame):
    def __init__(self, master: tk.Misc, *args: Any, **kwargs: Any) -> None:
        super().__init__(master, *args, **kwargs)
