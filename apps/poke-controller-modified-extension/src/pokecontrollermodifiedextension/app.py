import tkinter as tk
from tkinter import ttk
from typing import Any

from .info import AppInfo
from .model import AppModel
from .state import AppGuiState, load_state

INFO = AppInfo(
    name="Poke-Controller Modified Extension",
    version="0.2.0",
)


class App(tk.Tk):
    def __init__(
        self,
        base_dir: str,
        profile: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._base_dir = base_dir
        self._profile = profile

        self._app_info = INFO
        self._app_state = load_state(base_dir=base_dir, profile=profile)
        self._app_model = AppModel(self._app_info, self._app_state)

        # Theme
        style = ttk.Style(self)
        style.theme_use(self._app_state.general.theme.get())

        self.title(f"{INFO.name}(v{INFO.version})")

    @property
    def base_dir(self) -> str:
        return self._base_dir

    @property
    def profile(self) -> str:
        return self._profile

    @property
    def app_info(self) -> AppInfo:
        return self._app_info

    @property
    def app_model(self) -> AppModel:
        return self._app_model

    @property
    def app_state(self) -> AppGuiState:
        return self._app_state

    def run(self) -> None:
        self.mainloop()
