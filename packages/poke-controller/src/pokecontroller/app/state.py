from dataclasses import dataclass
from typing import TypeVar, Generic, Literal

T = TypeVar("T")


class Value(Generic[T]):
    def get(self) -> T | None:
        return self._container.get()

    def set(self, value: T | None) -> None:
        self._container.set(value)


@dataclass
class PokeControllerAppState:
    theme: Value[str]

    # Camera Settings
    camera_id: Value[str]
    camera_name: Value[str]
    camera_fps: Value[int]
    camera_size: Value[str]
    camera_show_realtime: Value[bool]
    camera_show_value: Value[bool]
    camera_show_guide: Value[bool]

    # Serial Settings
    serial_port: Value[str]
    serial_baud_rate: Value[int]
    serial_data_format: Value[str]
    serial_show_data: Value[bool]

    # Manual Control Settings
    manual_control_enabled_keyboard: Value[bool]
    manual_control_enabled_lstick_mouse: Value[bool]
    manual_control_enabled_rstick_mouse: Value[bool]
    manual_control_enabled_pro_controller: Value[bool]
    manual_control_enabled_record_pro_controller: Value[bool]

    # Command Settings
    command_python_commands_filter: Value[str]
    command_python_command: Value[str]
    command_mcu_commands_filter: Value[str]
    command_mcu_command: Value[str]
    command_shortcut_number: Value[int]
    command_shortcuts: list[Value[str]]

    # Notification Settings
    notification_enabled_windows_start: Value[bool]
    notification_enabled_windows_end: Value[bool]
    notification_enabled_discord_start: Value[bool]
    notification_enabled_discord_end: Value[bool]

    # Other Settings
    other_output_size: Value[int]
    other_output_standard: Value[int]
    other_widget_visibled_output1: Value[bool]
    other_widget_visibled_output2: Value[bool]
    other_widget_visibled_software_controller: Value[bool]
    other_software_controller_position: Value[str]
    other_dialogue_confirm_buttons_position: Value[str]
