import tkinter as tk
from tkinter import ttk

from .info import (
    PokeControllerAppInfo as Info,
    INFO,
)
from .model import PokeControllerExtensionAppModel as Model
from .state import (
    PokeControllerAppState as State,
    load_state,
)

from .windows import MainWindow


class PokeControllerExtensionApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self._model: Model = Model(load_state())
        self._info: Info = INFO

        # Theme
        style = ttk.Style(self)
        style.theme_use(self._model.state.theme.get())

        # FIXME
        self.title("PokeController Extension")

        self.build_ui()

    @property
    def app_info(self) -> Info:
        return self._info

    @property
    def app_model(self) -> Model:
        return self._model

    @property
    def app_state(self) -> State:
        return self._model.state

    def run(self):
        self.mainloop()

    def build_ui(self):
        main_window = MainWindow(self,
                                 padding=5)
        main_window.pack(expand=True, fill=tk.BOTH)
