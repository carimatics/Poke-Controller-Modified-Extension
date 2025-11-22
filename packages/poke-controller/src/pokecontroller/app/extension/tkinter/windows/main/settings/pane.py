import tkinter as tk
import tkinter.ttk as ttk

from .camera import CameraSettings
from .commands import CommandsSettings
from .manual_control import ManualControlSettings
from .notification import NotificationSettings
from .others import OthersSettings
from .serial import SerialSettings

CAMERA = 'camera'
SERIAL = 'serial'
MANUAL_CONTROL = 'manual_control'
COMMANDS = 'commands'
NOTIFICATION = 'notification'
OTHERS = 'others'

SETTINGS: list[tuple[str, type[ttk.Frame], str]] = [
    (CAMERA, CameraSettings, 'Camera'),
    (SERIAL, SerialSettings, 'Serial'),
    (MANUAL_CONTROL, ManualControlSettings, 'Manual Control'),
    (COMMANDS, CommandsSettings, 'Commands'),
    (NOTIFICATION, NotificationSettings, 'Notification'),
    (OTHERS, OthersSettings, 'Others'),
]


class SettingsPane(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.build_ui()

    def build_ui(self):
        # Create Notebook
        notebook = ttk.Notebook(self)

        # Create Notebook Children
        settings: dict[str, ttk.Frame] = {}
        for name, settings_class, tag_text in SETTINGS:
            settings[name] = settings_class(notebook)
            notebook.add(settings[name], text=tag_text, padding=5, sticky=tk.NSEW)

        # Layout
        notebook.pack(expand=True, fill=tk.BOTH, padx=0)
