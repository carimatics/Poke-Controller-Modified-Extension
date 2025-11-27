import tkinter as tk
from typing import Any

from ..mixins import AppAccessorMixIn
from ... import PokeControllerExtensionApp as App


class AppDialog(tk.Toplevel, AppAccessorMixIn):
    def __init__(self, master: AppAccessorMixIn, *args: Any, **kwargs: Any) -> None:
        super().__init__(master, *args, **kwargs)
        self._app: App = master.app

    @property
    def app(self) -> App:
        return self._app
