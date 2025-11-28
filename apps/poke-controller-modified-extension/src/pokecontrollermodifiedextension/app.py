import tkinter as tk
from tkinter import ttk
from typing import Any

from .info import AppInfo
from .model import AppModel
from .state import AppState, load_state

INFO = AppInfo(
    name="PokeController Modified Extension",
)


class App(tk.Tk):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self._app_info = INFO
        self._app_state = load_state()
        self._app_model = AppModel(self._app_info, self._app_state)

        # Theme
        style = ttk.Style(self)
        style.theme_use(self._app_state.theme.get())

        # FIXME
        self.title("PokeController Extension")

    @property
    def app_info(self) -> AppInfo:
        return self._app_info

    @property
    def app_model(self) -> AppModel:
        return self._app_model

    @property
    def app_state(self) -> AppState:
        return self._app_state

    def run(self) -> None:
        self.mainloop()
