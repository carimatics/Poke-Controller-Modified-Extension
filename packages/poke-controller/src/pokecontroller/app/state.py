from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Literal


class Variable[T](ABC):
    @property
    @abstractmethod
    def container(self) -> Any:
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
    other_output_size: Variable[int]
    other_output_stdout: Variable[int]
    other_widget_visible_output1: Variable[bool]
    other_widget_visible_output2: Variable[bool]
    other_widget_visible_software_controller: Variable[bool]
    other_widget_software_controller_position: Variable[str]
    other_widget_dialogue_confirm_buttons_position: Variable[str]
