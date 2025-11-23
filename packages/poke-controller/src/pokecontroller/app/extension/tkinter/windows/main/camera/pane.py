import tkinter as tk
import tkinter.ttk as ttk

from .buttons import Buttons
from .canvas import Canvas


class CameraPane(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.build_ui()

    def build_ui(self):
        # Create Labelframe
        labelframe = ttk.Labelframe(self,
                                    text="Main Panel")

        # Main Panel
        buttons = Buttons(labelframe)
        canvas = Canvas(labelframe,
                        width=640,
                        height=360,
                        relief=tk.GROOVE)

        # Layout
        buttons.pack(expand=True, fill=tk.NONE, anchor=tk.CENTER)
        canvas.pack(expand=True, fill=tk.NONE, anchor=tk.CENTER, pady=4)
        labelframe.pack(expand=True, fill=tk.BOTH)
