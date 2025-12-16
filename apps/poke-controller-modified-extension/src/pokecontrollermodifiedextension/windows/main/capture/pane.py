import tkinter as tk
import tkinter.ttk as ttk
from typing import Any

from ....settings import get_app_settings
from ....widgets.app import AppFrame
from .buttons import Buttons
from .capture import Capture


class CapturePane(AppFrame):
    def __init__(self, master: tk.Misc, *args: Any, **kwargs: Any) -> None:
        super().__init__(master, *args, **kwargs)

        self._app_settings = get_app_settings()
        self._size = self._app_settings.capture.size

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

        # Capture Area
        width, height = self._camera_size
        capture = Capture(labelframe)
        capture.configure(width=width, height=height, relief=tk.GROOVE)

        # Layout
        buttons.pack(expand=True, fill=tk.NONE, anchor=tk.CENTER)
        capture.pack(expand=True, fill=tk.NONE, anchor=tk.CENTER, pady=4)
        labelframe.pack(expand=True, fill=tk.BOTH)
