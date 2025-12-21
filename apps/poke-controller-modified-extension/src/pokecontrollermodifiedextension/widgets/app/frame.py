import tkinter as tk
from typing import Any

from pokecontrollermodifiedextension.mixins import AppAccessorMixIn
from pokecontrollermodifiedextension.widgets.frame import Frame


class AppFrame(Frame, AppAccessorMixIn):
    def __init__(self, master: tk.Misc, *args: Any, **kwargs: Any) -> None:
        super().__init__(master, *args, **kwargs)

    def refresh(self) -> None:
        pass
