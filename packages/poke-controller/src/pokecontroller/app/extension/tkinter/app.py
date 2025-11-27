import tkinter as tk
from tkinter import ttk
from typing import Any

from .info import (
    PokeControllerAppInfo as Info,
    INFO,
)
from .model import PokeControllerExtensionAppModel as Model
from .state import (
    PokeControllerAppState as State,
    load_state,
)


class PokeControllerExtensionApp(tk.Tk):
    def __init__(
        self,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
    ) -> None:
        super().__init__(*args, **kwargs)  # type: ignore[arg-type]

        self._state: State = load_state()
        self._model: Model = Model(self._state)
        self._info: Info = INFO

        # Theme
        style = ttk.Style(self)
        style.theme_use(self._state.theme.get())

        # FIXME
        self.title("PokeController Extension")

    @property
    def app_info(self) -> Info:
        return self._info

    @property
    def app_model(self) -> Model:
        return self._model

    @property
    def app_state(self) -> State:
        return self._state

    def run(self) -> None:
        self.mainloop()
