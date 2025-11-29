import tkinter as tk
import tkinter.ttk as ttk
from typing import Any

from ....widgets import AppFrame
from ....values import literals as l
from .buttons import Buttons
from .canvas import Canvas


class CameraPane(AppFrame):
    def __init__(self, master: tk.Misc, *args: Any, **kwargs: Any) -> None:
        super().__init__(master, *args, **kwargs)

        self._canvas: Canvas | None = None

        self._size = self.app_state.camera_size
        self._register_hooks()

        self.build_ui()

    @property
    def _camera_size(self) -> tuple[int, int]:
        width, height = map(int, self._size.get().split("x"))
        return width, height

    def build_ui(self) -> None:
        # Create Labelframe
        labelframe = ttk.Labelframe(self, text="Main Panel")

        # Main Panel
        buttons = Buttons(labelframe)

        width, height = self._camera_size
        self._canvas = Canvas(labelframe)
        self._canvas.configure(width=width, height=height, relief=l.GROOVE)

        # Layout
        buttons.pack(expand=True, fill=l.NONE, anchor=l.CENTER)
        self._canvas.pack(expand=True, fill=l.NONE, anchor=l.CENTER, pady=4)
        labelframe.pack(expand=True, fill=l.BOTH)

    def _register_hooks(self) -> None:
        self._size.trace_add("write", self._on_camera_size_changed)

    def _on_camera_size_changed(self, *_: Any) -> None:
        if (canvas := self._canvas) is None:
            raise RuntimeError("Canvas is not initialized.")

        width, height = self._camera_size
        canvas.configure(width=width, height=height)
