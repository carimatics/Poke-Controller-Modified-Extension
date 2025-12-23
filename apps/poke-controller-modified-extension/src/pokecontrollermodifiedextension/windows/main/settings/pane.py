import tkinter as tk
import tkinter.ttk as ttk
from typing import Any

from pokecontrollermodifiedextension.widgets.frame import Frame
from pokecontrollermodifiedextension.windows.main.settings.capture import (
    CameraSettings,
)
from pokecontrollermodifiedextension.windows.main.settings.commands import (
    CommandsSettings,
)
from pokecontrollermodifiedextension.windows.main.settings.manual_control import (
    ManualControlSettings,
)
from pokecontrollermodifiedextension.windows.main.settings.notification import (
    NotificationSettings,
)
from pokecontrollermodifiedextension.windows.main.settings.others import (
    OthersSettings,
)
from pokecontrollermodifiedextension.windows.main.settings.serial import (
    SerialSettings,
)

CAPTURE = "capture"
SERIAL = "serial"
MANUAL_CONTROL = "manual_control"
COMMANDS = "commands"
NOTIFICATION = "notification"
OTHERS = "others"

SETTINGS: list[tuple[str, type[Frame], str]] = [
    (CAPTURE, CameraSettings, "Capture"),
    (SERIAL, SerialSettings, "Serial"),
    (MANUAL_CONTROL, ManualControlSettings, "Manual Control"),
    (COMMANDS, CommandsSettings, "Commands"),
    (NOTIFICATION, NotificationSettings, "Notification"),
    (OTHERS, OthersSettings, "Others"),
]


class SettingsPane(Frame):
    def __init__(self, master: tk.Misc, *args: Any, **kwargs: Any) -> None:
        super().__init__(master, *args, **kwargs)
        self.build_ui()

    def build_ui(self) -> None:
        # Create Notebook
        notebook = ttk.Notebook(self)

        # Create Notebook Children
        settings: dict[str, Frame] = {}
        for name, settings_class, tag_text in SETTINGS:
            settings[name] = settings_class(notebook)
            notebook.add(settings[name], text=tag_text, padding=5, sticky=tk.NSEW)

        # Layout
        notebook.pack(expand=True, fill=tk.BOTH, padx=0)
