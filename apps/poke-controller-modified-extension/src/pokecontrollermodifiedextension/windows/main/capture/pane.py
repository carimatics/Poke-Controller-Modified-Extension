import tkinter as tk
from typing import Any

from pokecontrollermodifiedextension.singletons.app.settings import get_app_settings
from pokecontrollermodifiedextension.widgets.frame import Frame
from pokecontrollermodifiedextension.widgets.labelframe import Labelframe
from pokecontrollermodifiedextension.windows.main.capture.buttons import Buttons
from pokecontrollermodifiedextension.windows.main.capture.capture import Capture


class CapturePane(Frame):
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
        labelframe = Labelframe(self, text="Main Panel")

        # Main Panel
        buttons = Buttons(labelframe)

        # Capture Area
        width, height = self._camera_size
        capture = Capture(labelframe)
        capture.configure(width=width, height=height, relief=tk.GROOVE)

        # Layout
        buttons.pack(expand=True, fill=tk.NONE, anchor=tk.CENTER, pady=(4, 0))
        capture.pack(expand=True, fill=tk.NONE, anchor=tk.CENTER, pady=4)
        labelframe.pack(expand=True, fill=tk.BOTH)
