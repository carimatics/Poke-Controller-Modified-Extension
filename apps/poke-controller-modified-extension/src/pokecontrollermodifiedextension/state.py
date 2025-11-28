from dataclasses import dataclass
from tkinter import Variable, StringVar, IntVar, BooleanVar, DoubleVar
from typing import Any

DEFAULT_STATE = {
    "theme": "default",
    "camera_id": "",
    "camera_name": "",
    "camera_fps": 45,
    "camera_size": "640x360",
    "camera_show_realtime": True,
    "camera_show_matched": False,
    "camera_show_guide": False,
    "serial_port": "",
    "serial_baud_rate": 9600,
    "serial_data_format": "Default",
    "serial_show_data": False,
    "manual_control_enabled_keyboard": False,
    "manual_control_enabled_lstick_mouse": False,
    "manual_control_enabled_rstick_mouse": False,
    "manual_control_enabled_pro_controller": False,
    "manual_control_enabled_record_pro_controller": False,
    "command_python_commands_filter": "-",
    "command_python_command": "",
    "command_mcu_commands_filter": "-",
    "command_mcu_command": "",
    "command_shortcut_number": 1,
    "command_shortcuts": ["" for _ in range(10)],
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


@dataclass
class AppState:
    # Theme
    theme: StringVar

    # Camera Settings
    camera_id: StringVar
    camera_name: StringVar
    camera_fps: IntVar
    camera_size: StringVar
    camera_show_realtime: BooleanVar
    camera_show_matched: BooleanVar
    camera_show_guide: BooleanVar

    # Serial Settings
    serial_port: StringVar
    serial_baud_rate: IntVar
    serial_data_format: StringVar
    serial_show_data: BooleanVar

    # Manual Control Settings
    manual_control_enabled_keyboard: BooleanVar
    manual_control_enabled_lstick_mouse: BooleanVar
    manual_control_enabled_rstick_mouse: BooleanVar
    manual_control_enabled_pro_controller: BooleanVar
    manual_control_enabled_record_pro_controller: BooleanVar

    # Command Settings
    command_python_commands_filter: StringVar
    command_python_command: StringVar
    command_mcu_commands_filter: StringVar
    command_mcu_command: StringVar
    command_shortcut_number: IntVar
    command_shortcuts: list[StringVar]

    # Notification Settings
    notification_enabled_notify_windows_when_command_started: BooleanVar
    notification_enabled_notify_windows_when_command_ended: BooleanVar
    notification_enabled_notify_discord_when_command_started: BooleanVar
    notification_enabled_notify_discord_when_command_ended: BooleanVar

    # Other Settings
    other_output_size: DoubleVar
    other_output_stdout: IntVar
    other_widget_visible_output1: BooleanVar
    other_widget_visible_output2: BooleanVar
    other_widget_visible_software_controller: BooleanVar
    other_widget_software_controller_position: StringVar
    other_widget_dialogue_confirm_buttons_position: StringVar


def load_state() -> AppState:
    # FIXME: load from state file
    raw_state: dict[str, Any] = {}

    # Fill missing keys with default values
    for k in DEFAULT_STATE.keys():
        raw_state.setdefault(k, DEFAULT_STATE[k])

    kwargs: dict[str, Any] = {}
    for k, v in raw_state.items():
        if isinstance(v, bool):
            kwargs[k] = BooleanVar(value=v)
        elif isinstance(v, int):
            kwargs[k] = IntVar(value=v)
        elif isinstance(v, float):
            kwargs[k] = DoubleVar(value=v)
        elif isinstance(v, str):
            kwargs[k] = StringVar(value=v)
        elif isinstance(v, list):
            kwargs[k] = [StringVar(value=item) for item in v]

    return AppState(**kwargs)


def save_state(state: AppState) -> None:
    raw_state = {}
    for k in DEFAULT_STATE.keys():
        v = state.__dict__[k]
        if isinstance(v, list):
            raw_state[k] = [item.get() for item in v]
        elif isinstance(v, Variable):
            raw_state[k] = v.get()
        else:
            raise ValueError(f"Unsupported variable type: {type(v)}")

    # FIXME: save to state file
    print(raw_state)
