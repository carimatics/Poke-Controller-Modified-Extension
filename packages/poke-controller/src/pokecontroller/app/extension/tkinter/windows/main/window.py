import tkinter as tk
import tkinter.ttk as ttk

from .camera import CameraPane
from .controller import ControllerPane
from .outputs import OutputsPane
from .settings import SettingsPane

CAMERA = 'camera'
SETTINGS = 'settings'
OUTPUTS = 'outputs'
CONTROLLER = 'controller'

PANES = [
    (CAMERA, CameraPane, tk.LEFT),
    (SETTINGS, SettingsPane, tk.LEFT),
    (OUTPUTS, OutputsPane, tk.RIGHT),
    (CONTROLLER, ControllerPane, tk.RIGHT),
]


class MainWindow(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.panes: dict[str, ttk.Frame] = {}
        self.build_ui()

    def build_ui(self):
        # Frames
        frames = {
            tk.LEFT: ttk.Frame(self, relief=tk.SOLID, borderwidth=5),
            tk.RIGHT: ttk.Frame(self, relief=tk.SOLID, borderwidth=5),
        }

        # Create Panes
        for name, pane_class, side in PANES:
            self.panes[name] = pane_class(frames[side], relief=tk.SOLID, borderwidth=5)

        # Layout
        self.panes[CAMERA].pack(expand=True, fill=tk.BOTH, padx=0)
        self.panes[SETTINGS].pack(expand=False, fill=tk.BOTH, padx=0)
        self.panes[OUTPUTS].pack(expand=True, fill=tk.BOTH, padx=0)
        self.panes[CONTROLLER].pack(expand=True, fill=tk.BOTH, padx=0)
        frames[tk.LEFT].pack(expand=True, fill=tk.BOTH, side=tk.LEFT, padx=0)
        frames[tk.RIGHT].pack(expand=True, fill=tk.BOTH, side=tk.LEFT, padx=0)
