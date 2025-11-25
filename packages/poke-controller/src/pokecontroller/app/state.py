from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Literal

DEFAULT_STATE = {
    "theme": "default",
    "camera_id": None,
    "camera_name": None,
    "camera_fps": 45,
    "camera_size": "640x360",
    "camera_show_realtime": True,
    "camera_show_matched": False,
    "camera_show_guide": False,
    "serial_port": None,
    "serial_baud_rate": 9600,
    "serial_data_format": "Default",
    "serial_show_data": False,
    "manual_control_enabled_keyboard": False,
    "manual_control_enabled_lstick_mouse": False,
    "manual_control_enabled_rstick_mouse": False,
    "manual_control_enabled_pro_controller": False,
    "manual_control_enabled_record_pro_controller": False,
    "command_python_commands_filter": "-",
    "command_python_command": None,
    "command_mcu_commands_filter": "-",
    "command_mcu_command": None,
    "command_shortcut_number": 1,
    "command_shortcuts": [None for _ in range(10)],
    "notification_enabled_notify_windows_when_command_started": False,
    "notification_enabled_notify_windows_when_command_ended": False,
    "notification_enabled_notify_discord_when_command_started": False,
    "notification_enabled_notify_discord_when_command_ended": False,
    "other_output_size": 50.0,
    "other_output_stdout": 1,
    "other_widget_visible_output1": True,
    "other_widget_visible_output2": True,
    "other_widget_visible_software_controller": True,
    "other_widget_software_controller_position": "bottom",
    "other_widget_dialogue_confirm_buttons_position": "bottom",
}


class Variable[T](ABC):
    @property
    @abstractmethod
    def container[C](self) -> C:
        pass

    @abstractmethod
    def get(self) -> T | None:
        pass

    @abstractmethod
    def set(self, value: T | None) -> None:
        pass

    @abstractmethod
    def register_hook(self, mode: Literal["read", "write"], callback: Callable[[], None]) -> str:
        pass

    @abstractmethod
    def unregister_hook(self, mode: Literal["read", "write"], hook_id: str):
        pass


@dataclass
class PokeControllerAppState:
    # Theme
    theme: Variable[str]

    # Camera Settings
    camera_id: Variable[str]
    camera_name: Variable[str]
    camera_fps: Variable[int]
    camera_size: Variable[str]
    camera_show_realtime: Variable[bool]
    camera_show_matched: Variable[bool]
    camera_show_guide: Variable[bool]

    # Serial Settings
    serial_port: Variable[str]
    serial_baud_rate: Variable[int]
    serial_data_format: Variable[str]
    serial_show_data: Variable[bool]

    # Manual Control Settings
    manual_control_enabled_keyboard: Variable[bool]
    manual_control_enabled_lstick_mouse: Variable[bool]
    manual_control_enabled_rstick_mouse: Variable[bool]
    manual_control_enabled_pro_controller: Variable[bool]
    manual_control_enabled_record_pro_controller: Variable[bool]

    # Command Settings
    command_python_commands_filter: Variable[str]
    command_python_command: Variable[str]
    command_mcu_commands_filter: Variable[str]
    command_mcu_command: Variable[str]
    command_shortcut_number: Variable[int]
    command_shortcuts: list[Variable[str]]

    # Notification Settings
    notification_enabled_notify_windows_when_command_started: Variable[bool]
    notification_enabled_notify_windows_when_command_ended: Variable[bool]
    notification_enabled_notify_discord_when_command_started: Variable[bool]
    notification_enabled_notify_discord_when_command_ended: Variable[bool]

    # Other Settings
    other_output_size: Variable[float]
    other_output_stdout: Variable[int]
    other_widget_visible_output1: Variable[bool]
    other_widget_visible_output2: Variable[bool]
    other_widget_visible_software_controller: Variable[bool]
    other_widget_software_controller_position: Variable[str]
    other_widget_dialogue_confirm_buttons_position: Variable[str]
