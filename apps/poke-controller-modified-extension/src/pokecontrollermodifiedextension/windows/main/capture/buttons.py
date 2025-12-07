import logging
import tkinter as tk
import tkinter.ttk as ttk
from typing import Any

from ....model import AppModel
from ....values import literals as l
from ....widgets import AppDialog, AppFrame
from ...controller import ControllerWindow

logger = logging.getLogger(__name__)

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
    def __init__(self, master: tk.Misc, *args: Any, **kwargs: Any) -> None:
        super().__init__(master, *args, **kwargs)
        self._open_dir_button_image: tk.PhotoImage = tk.PhotoImage(
            file="../assets/icons8-OpenDir-16.png"
        )
        self._controller_window: AppDialog | None = None
        self.build_ui()

    @property
    def app_model(self) -> AppModel:
        return self.app.app_model

    def build_ui(self) -> None:
        # Create Buttons
        buttons: dict[str, ttk.Button] = {
            button: ttk.Button(self, command=command, **kwargs)  # type: ignore[arg-type]
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

    def _on_start_pushed(self) -> None:
        # FIXME: あとで消す
        logger.info(f"profile={self.app.profile} base_dir={self.app.base_dir}")

        self.app_model.start_command()

    def _on_controller_pushed(self) -> None:
        self._controller_window = ControllerWindow(self)
        self._controller_window.protocol(
            "WM_DELETE_WINDOW", self._on_controller_window_closed
        )

    def _on_clear_outputs_pushed(self) -> None:
        self.app_model.clear_log_outputs()

    def _on_capture_pushed(self) -> None:
        self.app_model.save_screencapture()

    def _on_open_dir_pushed(self) -> None:
        self.app_model.open_screencapture_directory_window()

    def _on_notify_discord_pushed(self) -> None:
        self.app_model.notify_discord()

    def _on_controller_window_closed(self) -> None:
        if (window := self._controller_window) is None:
            return
        window.destroy()
        self._controller_window = None
