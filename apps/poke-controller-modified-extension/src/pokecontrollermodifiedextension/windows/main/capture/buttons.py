import logging
import tkinter as tk
from typing import Any

from .... import widgets
from ....core.command import get_app_command_state
from ....core.command.info import get_current_command_info
from ....core.papico import get_papico
from ....model import get_app_model
from ....runtime_info import get_app_runtime_info
from ....widgets.app import AppDialog, AppFrame
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
    _buttons: dict[str, widgets.Button]

    def __init__(self, master: tk.Misc, *args: Any, **kwargs: Any) -> None:
        super().__init__(master, *args, **kwargs)
        self._open_dir_button_image: tk.PhotoImage = tk.PhotoImage(
            file="../assets/icons8-OpenDir-16.png"
        )
        self._papico = get_papico()
        self._runtime_info = get_app_runtime_info()
        self._app_model = get_app_model()
        self._command_state = get_app_command_state()
        self._controller_window: AppDialog | None = None

        self.build_ui()

        self._register_traces()

    def build_ui(self) -> None:
        # Create Buttons
        self._buttons: dict[str, widgets.Button] = {
            button: widgets.Button(self, command=command, **kwargs)  # type: ignore[arg-type]
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
            self._buttons[button].pack(
                expand=True, anchor=tk.CENTER, side=tk.LEFT, padx=4
            )

    def _on_start_pushed(self) -> None:
        current_command_info = get_current_command_info()
        if current_command_info is not None:
            self._papico.start_command(current_command_info)

    def _on_stop_pushed(self) -> None:
        self._papico.stop_command()

    def _on_controller_pushed(self) -> None:
        self._controller_window = ControllerWindow(self)
        self._controller_window.protocol(
            "WM_DELETE_WINDOW", self._on_controller_window_closed
        )

    def _on_clear_outputs_pushed(self) -> None:
        self._app_model.clear_log_outputs()

    def _on_capture_pushed(self) -> None:
        self._app_model.save_screencapture()

    def _on_open_dir_pushed(self) -> None:
        self._app_model.open_screencapture_directory_window()

    def _on_notify_discord_pushed(self) -> None:
        self._app_model.notify_discord()

    def _on_controller_window_closed(self) -> None:
        if (window := self._controller_window) is None:
            return
        window.destroy()
        self._controller_window = None

    def _on_running_changed(self, *_: str) -> None:
        if self._command_state.is_running.get():
            self._buttons[START].config(text="Stop", command=self._on_stop_pushed)
            self.update_idletasks()

    def _on_stopped_changed(self, *_: str) -> None:
        if self._command_state.is_stopped.get():
            self._buttons[START].config(text="Start", command=self._on_start_pushed)
            self.update_idletasks()

    def _register_traces(self) -> None:
        self.register_trace(
            "write",
            self._command_state.is_running,
            self._on_running_changed,
        )
        self.register_trace(
            "write",
            self._command_state.is_stopped,
            self._on_stopped_changed,
        )
