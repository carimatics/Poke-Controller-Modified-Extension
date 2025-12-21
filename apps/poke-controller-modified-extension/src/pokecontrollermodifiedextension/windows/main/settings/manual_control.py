import tkinter as tk
from typing import Any

from pokecontrollermodifiedextension.core.model import get_app_model
from pokecontrollermodifiedextension.core.settings import get_app_settings

from .... import widgets
from ....translation import t
from ....widgets.app import AppFrame


class ManualControlSettings(AppFrame):
    def __init__(self, master: tk.Misc, *args: Any, **kwargs: Any) -> None:
        super().__init__(master, *args, **kwargs)

        self._app_settings = get_app_settings()
        self._app_model = get_app_model()

        self._enabled_keyboard = self._app_settings.device.keyboard.enabled
        self._enabled_lstick_mouse = self._app_settings.device.mouse.enabled_lclick
        self._enabled_rstick_mouse = self._app_settings.device.mouse.enabled_rclick
        self._enabled_pro_controller = self._app_settings.device.pro_controller.enabled
        self._enabled_record_pro_controller = (
            self._app_settings.device.pro_controller.enabled_record
        )

        self.build_ui()

    def build_ui(self) -> None:
        # Create Labelframes
        software_settings = self._build_software_settings()
        hardware_settings = self._build_hardware_settings()

        # Layout
        software_settings.pack(expand=False, fill=tk.X, anchor=tk.N, pady=4)
        hardware_settings.pack(expand=False, fill=tk.X, anchor=tk.N, pady=4)

    def _build_software_settings(self) -> widgets.Labelframe:
        labelframe = widgets.Labelframe(self, text="Software")

        upper_frame = widgets.Frame(labelframe)
        lower_frame = widgets.Frame(labelframe)

        # Controller Button
        controller_button = widgets.Button(
            upper_frame,
            text=t("main.settings.manual_control.software.controller"),
            tooltip=t("main.settings.manual_control.software.controller.tooltip"),
            width=15,
            command=self._on_controller_pushed,
        )

        # Use Keyboard
        use_keyboard_checkbutton = widgets.Checkbutton(
            lower_frame,
            text=t("main.settings.manual_control.software.keyboard.use_keyboard"),
            tooltip=t(
                "main.settings.manual_control.software.keyboard.use_keyboard.tooltip"
            ),
            variable=self._enabled_keyboard,
            command=self._on_enabled_keyboard_changed,
        )

        # Use LStick Mouse
        use_lstick_mouse_checkbutton = widgets.Checkbutton(
            lower_frame,
            text=t("main.settings.manual_control.software.mouse.use_lclick"),
            tooltip=t("main.settings.manual_control.software.mouse.use_lclick.tooltip"),
            variable=self._enabled_lstick_mouse,
            command=self._on_enabled_lstick_mouse_changed,
        )

        # Use RStick Mouse
        use_rstick_mouse_checkbutton = widgets.Checkbutton(
            lower_frame,
            text=t("main.settings.manual_control.software.mouse.use_rclick"),
            tooltip=t("main.settings.manual_control.software.mouse.use_rclick.tooltip"),
            variable=self._enabled_rstick_mouse,
            command=self._on_enabled_rstick_mouse_changed,
        )

        # Layout
        controller_button.pack(expand=False, fill=tk.NONE, side=tk.LEFT, padx=4, pady=4)
        use_keyboard_checkbutton.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4)
        use_lstick_mouse_checkbutton.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=8)
        use_rstick_mouse_checkbutton.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4)
        upper_frame.pack(expand=False, fill=tk.X, anchor=tk.N)
        lower_frame.pack(expand=False, fill=tk.X, anchor=tk.N, pady=4)

        return labelframe

    def _build_hardware_settings(self) -> widgets.Labelframe:
        labelframe = widgets.Labelframe(self, text="Hardware")

        # Use Pro Controller
        use_pro_controller_checkbutton = widgets.Checkbutton(
            labelframe,
            text=t("main.settings.manual_control.hardware.pro_controller.use"),
            tooltip=t(
                "main.settings.manual_control.hardware.pro_controller.use.tooltip"
            ),
            variable=self._enabled_pro_controller,
            command=self._on_enabled_pro_controller_changed,
        )

        # Record Pro Controller
        record_pro_controller_checkbutton = widgets.Checkbutton(
            labelframe,
            text=t("main.settings.manual_control.hardware.pro_controller.record"),
            tooltip=t(
                "main.settings.manual_control.hardware.pro_controller.record.tooltip"
            ),
            variable=self._enabled_record_pro_controller,
            command=self._on_enabled_record_pro_controller_changed,
        )

        # Layout
        use_pro_controller_checkbutton.pack(
            expand=False,
            fill=tk.X,
            side=tk.LEFT,
            padx=4,
            pady=4,
        )
        record_pro_controller_checkbutton.pack(
            expand=False,
            fill=tk.X,
            side=tk.LEFT,
            padx=8,
            pady=4,
        )

        return labelframe

    def _on_controller_pushed(self) -> None:
        self._app_model.open_software_controller_window()

    def _on_enabled_keyboard_changed(self) -> None:
        self._app_model.apply_enabled_keyboard()

    def _on_enabled_lstick_mouse_changed(self) -> None:
        self._app_model.apply_enabled_lstick_mouse()

    def _on_enabled_rstick_mouse_changed(self) -> None:
        self._app_model.apply_enabled_rstick_mouse()

    def _on_enabled_pro_controller_changed(self) -> None:
        self._app_model.apply_enabled_pro_controller()

    def _on_enabled_record_pro_controller_changed(self) -> None:
        self._app_model.apply_enabled_record_pro_controller()
