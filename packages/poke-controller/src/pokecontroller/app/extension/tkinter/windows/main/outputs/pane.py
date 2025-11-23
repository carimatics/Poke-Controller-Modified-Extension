import tkinter as tk

from ....components import AppFrame

from .output import Output


class OutputsPane(AppFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.build_ui()

    def build_ui(self):
        outputs = [
            Output(self, id=1),
            Output(self, id=2),
        ]
        outputs[0].pack(expand=True, fill=tk.BOTH, pady=(0, 4))
        outputs[1].pack(expand=True, fill=tk.BOTH)
