from dataclasses import dataclass, fields, is_dataclass
from tkinter import BooleanVar, DoubleVar, IntVar, StringVar
from typing import Any, Self

# @formatter:off (for PyCharm)
# fmt: off
# language=toml
DEFAULT_GUI_STATE: str = """
[general]
theme = "default"
version = "0.1.8"

[capture]
camera_id = 0
camera_name = "0"
fps = 45
size = "640x360"
show_realtime = true
show_matched = false
show_guide = false

[serial]
port = ""
port_name = ""
baud_rate = 9600
data_format = "Default"
show_data = false

[device_input]
touchscreen.sx = 1
touchscreen.sy = 1
touchscreen.ex = 320
touchscreen.ey = 240
enabled_keyboard = true
enabled_lstick_mouse = true
enabled_rstick_mouse = true
enabled_pro_controller = false
enabled_record_pro_controller = false

[command]
python_commands_filter = "-"
python_command = ""
mcu_commands_filter = "-"
mcu_command = ""

[command.shortcut]
number = 1

[command.shortcut.registered_commands]
"1".name = "(empty)"
"1".klass = "None"
"2".name = "(empty)"
"2".klass = "None"
"3".name = "(empty)"
"3".klass = "None"
"4".name = "(empty)"
"4".klass = "None"
"5".name = "(empty)"
"5".klass = "None"
"6".name = "(empty)"
"6".klass = "None"
"7".name = "(empty)"
"7".klass = "None"
"8".name = "(empty)"
"8".klass = "None"
"9".name = "(empty)"
"9".klass = "None"
"10".name = "(empty)"
"10".klass = "None"

[notification]
line.enabled_started = false
line.enabled_ended = false
discord.enabled_started = false
discord.enabled_ended = false

[widget]
outputs.size_balance = 50.0
outputs.stdout = 1
outputs.visible_output1 = true
outputs.visible_output2 = true
software_controller.position = "bottom"
software_controller.visible = true
dialog.confirm_buttons_position = "bottom"
"""
# fmt: on
# @formatter:on (for PyCharm)


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
class AppGuiNotificationSettings:
    line: AppGuiLineNotificationSettings
    discord: AppGuiDiscordNotificationSettings

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Self:
        return cls(
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
        match v:
            case dict(d):
                result[k] = _convert_to_state_dict(d)
            case int(i):
                result[k] = IntVar(value=i)
            case float(f):
                result[k] = DoubleVar(value=f)
            case str(s):
                result[k] = StringVar(value=s)
            case bool(b):
                result[k] = BooleanVar(value=b)
            case _:
                raise ValueError(f"unsupported type: {type(v)}")
    return result


def convert_from_state(state: Any) -> dict[str, Any]:
    if isinstance(state, dict):
        return {k: convert_from_state(v) for k, v in state.items()}

    if not is_dataclass(state):
        raise ValueError(f"unsupported type: {type(state)}")

    result: dict[str, Any] = {}
    for field in fields(state):
        k, v = field.name, getattr(state, field.name)
        if isinstance(v, (StringVar, BooleanVar, IntVar, DoubleVar)):
            result[k] = v.get()
        else:
            result[k] = convert_from_state(v)
    return result
