import tkinter as tk
from typing import Any

from ..app import App
from ..mixins import AppAccessorMixIn


class AppDialog(tk.Toplevel, AppAccessorMixIn):
    def __init__(self, master: AppAccessorMixIn, *args: Any, **kwargs: Any) -> None:
        super().__init__(master, *args, **kwargs)
        self._app: App = master.app

    @property
    def app(self) -> App:
        return self._app
