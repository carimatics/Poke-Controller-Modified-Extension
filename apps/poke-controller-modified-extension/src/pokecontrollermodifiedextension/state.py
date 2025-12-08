from dataclasses import dataclass
from tkinter import BooleanVar, DoubleVar, IntVar, StringVar
from typing import Any, Self


@dataclass
class AppGuiGeneralSettings:
    theme: StringVar
    version: StringVar


@dataclass
class AppGuiCaptureSettings:
    camera_id: StringVar
    camera_name: StringVar
    fps: IntVar
    size: StringVar
    show_realtime: BooleanVar
    show_matched: BooleanVar
    show_guide: BooleanVar


@dataclass
class AppGuiSerialSettings:
    port: StringVar
    port_name: StringVar
    baud_rate: IntVar
    data_format: StringVar
    show_data: BooleanVar


@dataclass
class AppGuiTouchscreenSettings:
    sx: IntVar
    sy: IntVar
    ex: IntVar
    ey: IntVar


@dataclass
class AppGuiDeviceInputSettings:
    touchscreen: AppGuiTouchscreenSettings
    enabled_keyboard: BooleanVar
    enabled_lstick_mouse: BooleanVar
    enabled_rstick_mouse: BooleanVar
    enabled_pro_controller: BooleanVar
    enabled_record_pro_controller: BooleanVar

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Self:
        return cls(
            touchscreen=AppGuiTouchscreenSettings(**d["touchscreen"]),
            enabled_keyboard=d["enabled_keyboard"],
            enabled_lstick_mouse=d["enabled_lstick_mouse"],
            enabled_rstick_mouse=d["enabled_rstick_mouse"],
            enabled_pro_controller=d["enabled_pro_controller"],
            enabled_record_pro_controller=d["enabled_record_pro_controller"],
        )


@dataclass
class AppGuiCommandShortcut:
    name: StringVar
    klass: StringVar


@dataclass
class AppGuiCommandShortcutSettings:
    number: IntVar
    registered_commands: dict[str, AppGuiCommandShortcut]

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Self:
        return cls(
            number=d["number"],
            registered_commands={
                k: AppGuiCommandShortcut(**v)
                for k, v in d["registered_commands"].items()
            },
        )


@dataclass
class AppGuiCommandSettings:
    python_commands_filter: StringVar
    python_command: StringVar
    mcu_commands_filter: StringVar
    mcu_command: StringVar
    shortcut: AppGuiCommandShortcutSettings

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Self:
        return cls(
            python_commands_filter=d["python_commands_filter"],
            python_command=d["python_command"],
            mcu_commands_filter=d["mcu_commands_filter"],
            mcu_command=d["mcu_command"],
            shortcut=AppGuiCommandShortcutSettings.from_dict(d["shortcut"]),
        )


@dataclass
class AppGuiLineNotificationSettings:
    enabled_started: BooleanVar
    enabled_ended: BooleanVar


@dataclass
class AppGuiDiscordNotificationSettings:
    enabled_started: BooleanVar
    enabled_ended: BooleanVar


@dataclass
class AppGuiWindowsNotificationSettings:
    enabled_started: BooleanVar
    enabled_ended: BooleanVar


@dataclass
class AppGuiNotificationSettings:
    windows: AppGuiWindowsNotificationSettings
    line: AppGuiLineNotificationSettings
    discord: AppGuiDiscordNotificationSettings

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Self:
        return cls(
            windows=AppGuiWindowsNotificationSettings(**d["windows"]),
            line=AppGuiLineNotificationSettings(**d["line"]),
            discord=AppGuiDiscordNotificationSettings(**d["discord"]),
        )


@dataclass
class AppGuiOutputsWidgetSettings:
    size_balance: DoubleVar
    stdout: IntVar
    visible_output1: BooleanVar
    visible_output2: BooleanVar


@dataclass
class AppGuiSoftwareControllerWidgetSettings:
    position: StringVar
    visible: BooleanVar


@dataclass
class AppGuiDialogWidgetSettings:
    confirm_buttons_position: StringVar


@dataclass
class AppGuiWidgetSettings:
    outputs: AppGuiOutputsWidgetSettings
    software_controller: AppGuiSoftwareControllerWidgetSettings
    dialog: AppGuiDialogWidgetSettings

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Self:
        return cls(
            outputs=AppGuiOutputsWidgetSettings(**d["outputs"]),
            software_controller=AppGuiSoftwareControllerWidgetSettings(
                **d["software_controller"]
            ),
            dialog=AppGuiDialogWidgetSettings(**d["dialog"]),
        )


@dataclass
class AppGuiState:
    general: AppGuiGeneralSettings
    capture: AppGuiCaptureSettings
    serial: AppGuiSerialSettings
    device_input: AppGuiDeviceInputSettings
    command: AppGuiCommandSettings
    notification: AppGuiNotificationSettings
    widget: AppGuiWidgetSettings

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Self:
        sd = _convert_to_state_dict(d)
        return cls(
            general=AppGuiGeneralSettings(**sd["general"]),
            capture=AppGuiCaptureSettings(**sd["capture"]),
            serial=AppGuiSerialSettings(**sd["serial"]),
            device_input=AppGuiDeviceInputSettings.from_dict(sd["device_input"]),
            command=AppGuiCommandSettings.from_dict(sd["command"]),
            notification=AppGuiNotificationSettings.from_dict(sd["notification"]),
            widget=AppGuiWidgetSettings.from_dict(sd["widget"]),
        )


def _convert_to_state_dict(data: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for k, v in data.items():
        if isinstance(v, dict):
            result[k] = _convert_to_state_dict(v)
        elif v is True or v is False:
            result[k] = BooleanVar(value=v)
        elif isinstance(v, int):
            result[k] = IntVar(value=v)
        elif isinstance(v, float):
            result[k] = DoubleVar(value=v)
        elif isinstance(v, str):
            result[k] = StringVar(value=v)
        else:
            raise ValueError(f"unsupported type: {type(v)}")
    return result
