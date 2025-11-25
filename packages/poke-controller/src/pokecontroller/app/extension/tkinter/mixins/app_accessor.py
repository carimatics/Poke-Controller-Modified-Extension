import tkinter as tk
from typing import cast

from ..app import PokeControllerExtensionApp as App
from ..info import PokeControllerAppInfo as AppInfo
from ..model import PokeControllerExtensionAppModel as AppModel
from ..state import PokeControllerAppState as AppState


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
