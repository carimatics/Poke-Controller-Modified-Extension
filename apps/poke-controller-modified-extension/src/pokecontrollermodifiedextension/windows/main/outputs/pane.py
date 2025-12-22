import tkinter as tk
from typing import Any

from pokecontrollermodifiedextension.state.widget_catalog import get_app_widget_catalog
from pokecontrollermodifiedextension.widgets.app import AppFrame
from pokecontrollermodifiedextension.windows.main.outputs.output import Output


class OutputsPane(AppFrame):
    def __init__(self, master: tk.Misc, *args: Any, **kwargs: Any) -> None:
        super().__init__(master, *args, **kwargs)

        # noinspection PyTypeChecker
        self.outputs: list[Output] = []

        self.build_ui()

        widget_catalog = get_app_widget_catalog()
        widget_catalog.outputs.textarea1 = self.outputs[0].textarea
        widget_catalog.outputs.textarea2 = self.outputs[1].textarea

    def build_ui(self) -> None:
        self.outputs += [
            Output(self, output_id=1),
            Output(self, output_id=2),
        ]
