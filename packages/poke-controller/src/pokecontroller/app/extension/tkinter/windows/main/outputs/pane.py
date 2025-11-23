import tkinter as tk
import tkinter.ttk as ttk

from .output import Output


class OutputsPane(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.build_ui()

    def build_ui(self):
        outputs = [
            Output(self, id=1),
            Output(self, id=2),
        ]
        outputs[0].pack(expand=True, fill=tk.BOTH, pady=(0, 8))
        outputs[1].pack(expand=True, fill=tk.BOTH)
