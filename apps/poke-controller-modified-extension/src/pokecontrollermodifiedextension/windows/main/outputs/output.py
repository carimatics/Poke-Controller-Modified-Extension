import tkinter as tk
import tkinter.ttk as ttk
from typing import Any

from ....widgets.app import AppFrame


class Output(AppFrame):
    def __init__(
        self, master: tk.Misc, output_id: int, *args: Any, **kwargs: Any
    ) -> None:
        super().__init__(master, *args, **kwargs)

        self._id: int = output_id
        self.text_area: tk.Text | None = None

        self.build_ui()

    def build_ui(self) -> None:
        labelframe = ttk.Labelframe(self, text=f"Output#{self._id}", relief=tk.GROOVE)

        # Text Area
        self.text_area = tk.Text(
            labelframe,
            width=62,
            blockcursor=True,
            insertunfocussed=tk.NONE,
            undo=False,
            maxundo=0,
            relief=tk.FLAT,
            state=tk.DISABLED,
        )
        scroll = tk.Scrollbar(
            labelframe,
            orient=tk.VERTICAL,
            command=self.text_area.yview,
        )
        self.text_area.configure(yscrollcommand=scroll.set)

        # Layout
        self.text_area.pack(
            expand=True, fill=tk.BOTH, side=tk.LEFT, padx=(5, 0), pady=5
        )
        scroll.pack(expand=False, fill=tk.Y, side=tk.LEFT, pady=5)
        labelframe.pack(expand=True, fill=tk.BOTH)
