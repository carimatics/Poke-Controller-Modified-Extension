import tkinter as tk
import tkinter.ttk as ttk

from ....components import AppFrame
from ....values import literals as l

from .buttons import Buttons
from .canvas import Canvas


class CameraPane(AppFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self._canvas: Canvas = None

        self._size = self.app_state.camera_size
        self._register_hooks()

        self.build_ui()

    @property
    def _camera_size(self) -> tuple[int, int]:
        # noinspection PyTypeChecker
        return tuple(map(int, self._size.get().split('x')))

    def build_ui(self):
        # Create Labelframe
        labelframe = ttk.Labelframe(self,
                                    text="Main Panel")

        # Main Panel
        buttons = Buttons(labelframe)

        width, height = self._camera_size
        self._canvas = Canvas(labelframe,
                              width=width,
                              height=height,
                              relief=tk.GROOVE)

        # Layout
        buttons.pack(expand=True, fill=l.NONE, anchor=l.CENTER)
        self._canvas.pack(expand=True, fill=l.NONE, anchor=l.CENTER, pady=4)
        labelframe.pack(expand=True, fill=l.BOTH)

    def _register_hooks(self):
        self._size.register_hook("write", self._on_camera_size_changed)

    def _on_camera_size_changed(self):
        width, height = self._camera_size
        self._canvas.configure(width=width, height=height)
