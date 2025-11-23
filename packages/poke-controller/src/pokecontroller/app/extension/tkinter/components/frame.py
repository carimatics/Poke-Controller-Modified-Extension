import tkinter.ttk as ttk

from ..mixins import AppAccessor


class AppFrame(ttk.Frame, AppAccessor):
    def __init__(self, master, *args, **kwargs):
        ttk.Frame.__init__(self, master, *args, **kwargs)
        AppAccessor.__init__(self)
