import tkinter as tk
from typing import Any
from ....components import AppFrame

from .output import Output


class OutputsPane(AppFrame):
    def __init__(
        self,
        master: tk.Misc,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
    ) -> None:
        super().__init__(master, *args, **kwargs)

        # noinspection PyTypeChecker
        self.outputs: list[Output] = []

        self.build_ui()

    def build_ui(self) -> None:
        self.outputs += [
            Output(self, output_id=1),
            Output(self, output_id=2),
        ]
