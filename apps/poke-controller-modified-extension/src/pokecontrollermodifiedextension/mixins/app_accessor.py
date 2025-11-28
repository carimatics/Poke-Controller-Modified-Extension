import tkinter as tk
from typing import cast

from ..app import App
from ..info import AppInfo
from ..model import AppModel
from ..state import AppState


class AppAccessorMixIn(tk.Misc):
    @property
    def app(self) -> App:
        return cast(App, self.winfo_toplevel())

    @property
    def app_info(self) -> AppInfo:
        return self.app.app_info

    @property
    def app_model(self) -> AppModel:
        return self.app.app_model

    @property
    def app_state(self) -> AppState:
        return self.app.app_state
