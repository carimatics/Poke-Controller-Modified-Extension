import tkinter as tk
import tkinter.ttk as ttk

from ....components import AppFrame

from .buttons import Buttons
from .canvas import Canvas


class CameraPane(AppFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # noinspection PyTypeChecker
        self._size: tk.StringVar = self.app_state.camera_size
        self._size_callback_id = self._size.trace_add('write', self._on_camera_size_changed)
        self._canvas: Canvas = None

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
        buttons.pack(expand=True, fill=tk.NONE, anchor=tk.CENTER)
        self._canvas.pack(expand=True, fill=tk.NONE, anchor=tk.CENTER, pady=4)
        labelframe.pack(expand=True, fill=tk.BOTH)

    def destroy(self):
        self._size.trace_remove('write', self._size_callback_id)
        super().destroy()

    def _on_camera_size_changed(self, _var_name: str, _index: str, _mode: str):
        width, height = self._camera_size
        self._canvas.configure(width=width, height=height)
