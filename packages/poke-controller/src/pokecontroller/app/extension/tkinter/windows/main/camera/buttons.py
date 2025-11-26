import tkinter as tk
import tkinter.ttk as ttk

from ....components import AppFrame
from ....values import literals as l

START = "start"
CONTROLLER = "controller"
CLEAR_OUTPUTS = "clear_outputs"
CAPTURE = "capture"
OPEN_CAPTURE_DIR = "open_capture_dir"
NOTIFY_DISCORD = "notify_discord"

BUTTONS = [
    START,
    CONTROLLER,
    CLEAR_OUTPUTS,
    CAPTURE,
    OPEN_CAPTURE_DIR,
    NOTIFY_DISCORD,
]


class Buttons(AppFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._open_dir_button_image: tk.PhotoImage = tk.PhotoImage(
            file="../assets/icons8-OpenDir-16.png"
        )
        self.build_ui()

    def build_ui(self):
        # Create Buttons
        buttons: dict[str, ttk.Button] = {
            button: ttk.Button(self, command=command, **kwargs)
            for button, command, kwargs in [
                (START, self._on_start_pushed, {"text": "Start"}),
                (CONTROLLER, self._on_controller_pushed, {"text": "Controller"}),
                (
                    CLEAR_OUTPUTS,
                    self._on_clear_outputs_pushed,
                    {"text": "Clear Outputs"},
                ),
                (CAPTURE, self._on_capture_pushed, {"text": "Capture"}),
                (
                    OPEN_CAPTURE_DIR,
                    self._on_open_dir_pushed,
                    {"image": self._open_dir_button_image, "padding": 1},
                ),
                (NOTIFY_DISCORD, self._on_notify_discord_pushed, {"text": "Discord"}),
            ]
        }

        # Layout
        for button in BUTTONS:
            buttons[button].pack(expand=True, anchor=l.CENTER, side=l.LEFT, padx=4)

    def _on_start_pushed(self):
        self.app_model.start_command()

    def _on_controller_pushed(self):
        self.app_model.open_software_controller_window()

    def _on_clear_outputs_pushed(self):
        self.app_model.clear_log_outputs()

    def _on_capture_pushed(self):
        self.app_model.save_screencapture()

    def _on_open_dir_pushed(self):
        self.app_model.open_screencapture_directory_window()

    def _on_notify_discord_pushed(self):
        self.app_model.notify_discord()
