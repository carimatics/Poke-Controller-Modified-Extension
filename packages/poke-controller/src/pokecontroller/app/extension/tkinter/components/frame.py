import tkinter as tk
import tkinter.ttk as ttk

from ..mixins import AppAccessorMixIn


class AppFrame(ttk.Frame, AppAccessorMixIn):
    def __init__(self, master: tk.Misc, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
