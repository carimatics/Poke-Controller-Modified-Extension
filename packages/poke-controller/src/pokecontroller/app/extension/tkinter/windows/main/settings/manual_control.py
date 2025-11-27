import tkinter as tk
import tkinter.ttk as ttk
from typing import Any

from ....components import AppFrame
from ....values import literals as l


class ManualControlSettings(AppFrame):
    def __init__(
        self,
        master: tk.Misc,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
    ) -> None:
        super().__init__(master, *args, **kwargs)

        self._enabled_keyboard = self.app_state.manual_control_enabled_keyboard
        self._enabled_lstick_mouse = self.app_state.manual_control_enabled_lstick_mouse
        self._enabled_rstick_mouse = self.app_state.manual_control_enabled_rstick_mouse
        self._enabled_pro_controller = (
            self.app_state.manual_control_enabled_pro_controller
        )
        self._enabled_record_pro_controller = (
            self.app_state.manual_control_enabled_record_pro_controller
        )

        self.build_ui()

    def build_ui(self) -> None:
        # Create Labelframes
        software_settings = self._build_software_settings()
        hardware_settings = self._build_hardware_settings()

        # Layout
        software_settings.pack(expand=False, fill=l.X, anchor=l.N, pady=4)
        hardware_settings.pack(expand=False, fill=l.X, anchor=l.N, pady=4)

    def _build_software_settings(self) -> ttk.Labelframe:
        labelframe = ttk.Labelframe(self, text="Software")

        upper_frame = ttk.Frame(labelframe)
        lower_frame = ttk.Frame(labelframe)

        # Controller Button
        controller_button = ttk.Button(
            upper_frame,
            width=15,
            text="Controller",
            command=self._on_controller_pushed,
        )

        # Use Keyboard
        use_keyboard_checkbutton = ttk.Checkbutton(
            lower_frame,
            text="Use Keyboard",
            variable=self._enabled_keyboard.container,
            command=self._on_enabled_keyboard_changed,
        )

        # Use LStick Mouse
        use_lstick_mouse_checkbutton = ttk.Checkbutton(
            lower_frame,
            text="Use LStick Mouse",
            variable=self._enabled_lstick_mouse.container,
            command=self._on_enabled_lstick_mouse_changed,
        )

        # Use RStick Mouse
        use_rstick_mouse_checkbutton = ttk.Checkbutton(
            lower_frame,
            text="Use RStick Mouse",
            variable=self._enabled_rstick_mouse.container,
            command=self._on_enabled_rstick_mouse_changed,
        )

        # Layout
        controller_button.pack(expand=False, fill=l.NONE, side=l.LEFT, padx=4, pady=4)
        use_keyboard_checkbutton.pack(expand=False, fill=l.X, side=l.LEFT, padx=4)
        use_lstick_mouse_checkbutton.pack(expand=False, fill=l.X, side=l.LEFT, padx=8)
        use_rstick_mouse_checkbutton.pack(expand=False, fill=l.X, side=l.LEFT, padx=4)
        upper_frame.pack(expand=False, fill=l.X, anchor=l.N)
        lower_frame.pack(expand=False, fill=l.X, anchor=l.N, pady=4)

        return labelframe

    def _build_hardware_settings(self) -> ttk.Labelframe:
        labelframe = ttk.Labelframe(self, text="Hardware")

        # Use Pro Controller
        use_pro_controller_checkbutton = ttk.Checkbutton(
            labelframe,
            text="Use Pro Controller",
            variable=self._enabled_pro_controller.container,
            command=self._on_enabled_pro_controller_changed,
        )

        # Record Pro Controller
        record_pro_controller_checkbutton = ttk.Checkbutton(
            labelframe,
            text="Record Pro Controller",
            variable=self._enabled_record_pro_controller.container,
            command=self._on_enabled_record_pro_controller_changed,
        )

        # Layout
        use_pro_controller_checkbutton.pack(
            expand=False,
            fill=l.X,
            side=l.LEFT,
            padx=4,
            pady=4,
        )
        record_pro_controller_checkbutton.pack(
            expand=False,
            fill=l.X,
            side=l.LEFT,
            padx=8,
            pady=4,
        )

        return labelframe

    def _on_controller_pushed(self) -> None:
        self.app_model.open_software_controller_window()

    def _on_enabled_keyboard_changed(self) -> None:
        self.app_model.apply_enabled_keyboard()

    def _on_enabled_lstick_mouse_changed(self) -> None:
        self.app_model.apply_enabled_lstick_mouse()

    def _on_enabled_rstick_mouse_changed(self) -> None:
        self.app_model.apply_enabled_rstick_mouse()

    def _on_enabled_pro_controller_changed(self) -> None:
        self.app_model.apply_enabled_pro_controller()

    def _on_enabled_record_pro_controller_changed(self) -> None:
        self.app_model.apply_enabled_record_pro_controller()
