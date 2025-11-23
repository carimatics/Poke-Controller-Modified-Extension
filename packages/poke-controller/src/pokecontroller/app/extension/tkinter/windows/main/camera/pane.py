import tkinter as tk
import tkinter.ttk as ttk

from ....components import AppFrame

from .buttons import Buttons
from .canvas import Canvas


class CameraPane(AppFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        size = [int(s) for s in self.app_state.camera_size.get().split('x')]
        self.size: tuple[int, int] = (size[0], size[1])

        self.build_ui()

    def build_ui(self):
        # Create Labelframe
        labelframe = ttk.Labelframe(self,
                                    text="Main Panel")

        # Main Panel
        buttons = Buttons(labelframe)
        canvas = Canvas(labelframe,
                        width=self.size[0],
                        height=self.size[1],
                        relief=tk.GROOVE)

        # Layout
        buttons.pack(expand=True, fill=tk.NONE, anchor=tk.CENTER)
        canvas.pack(expand=True, fill=tk.NONE, anchor=tk.CENTER, pady=4)
        labelframe.pack(expand=True, fill=tk.BOTH)
