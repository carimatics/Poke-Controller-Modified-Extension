import tkinter as tk
import tkinter.ttk as ttk

from ..mixins import AppAccessor


class AppFrame(ttk.Frame, AppAccessor):
    def __init__(self, master: tk.Misc, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
