from dataclasses import dataclass
from tkinter import BooleanVar, DoubleVar, IntVar, StringVar, Variable
from typing import Any

DEFAULT_GUI_STATE: dict[str, Any] = {
    "general": {
        "theme": "default",
    },
    "capture": {
        "camera_id": "0",
        "camera_name": "0",
        "fps": "45",
        "size": "640x360",
        "show_realtime": "True",
        "show_matched": "False",
        "show_guide": "False",
    },
    "serial": {
        "port": "",
        "baud_rate": "9600",
        "data_format": "Default",
        "show_data": "False",
    },
    "device_input": {
        "enabled_keyboard": "True",
        "enabled_lstick_mouse": "True",
        "enabled_rstick_mouse": "True",
        "enabled_pro_controller": "True",
        "enabled_record_pro_controller": "True",
    },
    "command": {
        "python_commands_filter": "-",
        "python_command": "",
        "mcu_commands_filter": "-",
        "mcu_command": "",
        "shortcut": {
            "number": "1",
            "registered_commands": {
                "1": {"name": "(empty)", "klass": "None"},
                "2": {"name": "(empty)", "klass": "None"},
                "3": {"name": "(empty)", "klass": "None"},
                "4": {"name": "(empty)", "klass": "None"},
                "5": {"name": "(empty)", "klass": "None"},
                "6": {"name": "(empty)", "klass": "None"},
                "7": {"name": "(empty)", "klass": "None"},
                "8": {"name": "(empty)", "klass": "None"},
                "9": {"name": "(empty)", "klass": "None"},
                "10": {"name": "(empty)", "klass": "None"},
            },
        },
    },
    "notification": {
        "line": {
            "enabled_started": "False",
            "enabled_ended": "False",
        },
        "discord": {
            "enabled_started": "False",
            "enabled_ended": "False",
        },
    },
    "widget": {
        "outputs": {
            "size_balance": "50.0",
            "stdout": "1",
            "visible_output1": "True",
            "visible_output2": "True",
        },
        "software_controller": {
            "position": "bottom",
            "visible": "True",
        },
        "dialog": {
            "confirm_buttons_position": "bottom",
        },
    },
}


@dataclass
class AppGuiGeneralSettings:
    theme: StringVar


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
    baud_rate: IntVar
    data_format: StringVar
    show_data: BooleanVar


@dataclass
class AppGuiDeviceInputSettings:
    enabled_keyboard: BooleanVar
    enabled_lstick_mouse: BooleanVar
    enabled_rstick_mouse: BooleanVar
    enabled_pro_controller: BooleanVar
    enabled_record_pro_controller: BooleanVar


@dataclass
class AppGuiCommandShortcut:
    name: StringVar
    klass: StringVar


@dataclass
class AppGuiCommandShortcutSettings:
    number: IntVar
    registered_commands: dict[str, AppGuiCommandShortcut]


@dataclass
class AppGuiCommandSettings:
    python_commands_filter: StringVar
    python_command: StringVar
    mcu_commands_filter: StringVar
    mcu_command: StringVar
    shortcut: AppGuiCommandShortcutSettings


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


@dataclass
class AppGuiState:
    general: AppGuiGeneralSettings
    capture: AppGuiCaptureSettings
    serial: AppGuiSerialSettings
    device_input: AppGuiDeviceInputSettings
    command: AppGuiCommandSettings
    notification: AppGuiNotificationSettings
    widget: AppGuiWidgetSettings


def load_state(
    *,
    base_dir: str,
    profile: str,
) -> AppGuiState:
    # FIXME: load from state file
    raw: dict[str, Any] = DEFAULT_GUI_STATE

    # general
    return AppGuiState(
        general=AppGuiGeneralSettings(
            theme=StringVar(value=raw["general"]["theme"]),
        ),
        capture=AppGuiCaptureSettings(
            camera_id=StringVar(value=raw["capture"]["camera_id"]),
            camera_name=StringVar(value=raw["capture"]["camera_name"]),
            fps=IntVar(value=int(raw["capture"]["fps"])),
            size=StringVar(value=raw["capture"]["size"]),
            show_realtime=BooleanVar(value=raw["capture"]["show_realtime"] == "True"),
            show_matched=BooleanVar(value=raw["capture"]["show_matched"] == "True"),
            show_guide=BooleanVar(value=raw["capture"]["show_guide"] == "True"),
        ),
        serial=AppGuiSerialSettings(
            port=StringVar(value=raw["serial"]["port"]),
            baud_rate=IntVar(value=int(raw["serial"]["baud_rate"])),
            data_format=StringVar(value=raw["serial"]["data_format"]),
            show_data=BooleanVar(value=raw["serial"]["show_data"] == "True"),
        ),
        device_input=AppGuiDeviceInputSettings(
            enabled_keyboard=BooleanVar(
                value=raw["device_input"]["enabled_keyboard"] == "True"
            ),
            enabled_lstick_mouse=BooleanVar(
                value=raw["device_input"]["enabled_lstick_mouse"] == "True"
            ),
            enabled_rstick_mouse=BooleanVar(
                value=raw["device_input"]["enabled_rstick_mouse"] == "True"
            ),
            enabled_pro_controller=BooleanVar(
                value=raw["device_input"]["enabled_pro_controller"] == "True"
            ),
            enabled_record_pro_controller=BooleanVar(
                value=raw["device_input"]["enabled_record_pro_controller"] == "True"
            ),
        ),
        command=AppGuiCommandSettings(
            python_commands_filter=StringVar(
                value=raw["command"]["python_commands_filter"]
            ),
            python_command=StringVar(value=raw["command"]["python_command"]),
            mcu_commands_filter=StringVar(value=raw["command"]["mcu_commands_filter"]),
            mcu_command=StringVar(value=raw["command"]["mcu_command"]),
            shortcut=AppGuiCommandShortcutSettings(
                number=IntVar(value=int(raw["command"]["shortcut"]["number"])),
                registered_commands={
                    "1": AppGuiCommandShortcut(
                        name=StringVar(
                            value=raw["command"]["shortcut"]["registered_commands"][
                                "1"
                            ]["name"]
                        ),
                        klass=StringVar(
                            value=raw["command"]["shortcut"]["registered_commands"][
                                "1"
                            ]["klass"]
                        ),
                    ),
                    "2": AppGuiCommandShortcut(
                        name=StringVar(
                            value=raw["command"]["shortcut"]["registered_commands"][
                                "2"
                            ]["name"]
                        ),
                        klass=StringVar(
                            value=raw["command"]["shortcut"]["registered_commands"][
                                "2"
                            ]["klass"]
                        ),
                    ),
                    "3": AppGuiCommandShortcut(
                        name=StringVar(
                            value=raw["command"]["shortcut"]["registered_commands"][
                                "3"
                            ]["name"]
                        ),
                        klass=StringVar(
                            value=raw["command"]["shortcut"]["registered_commands"][
                                "3"
                            ]["klass"]
                        ),
                    ),
                    "4": AppGuiCommandShortcut(
                        name=StringVar(
                            value=raw["command"]["shortcut"]["registered_commands"][
                                "4"
                            ]["name"]
                        ),
                        klass=StringVar(
                            value=raw["command"]["shortcut"]["registered_commands"][
                                "4"
                            ]["klass"]
                        ),
                    ),
                    "5": AppGuiCommandShortcut(
                        name=StringVar(
                            value=raw["command"]["shortcut"]["registered_commands"][
                                "5"
                            ]["name"]
                        ),
                        klass=StringVar(
                            value=raw["command"]["shortcut"]["registered_commands"][
                                "5"
                            ]["klass"]
                        ),
                    ),
                    "6": AppGuiCommandShortcut(
                        name=StringVar(
                            value=raw["command"]["shortcut"]["registered_commands"][
                                "6"
                            ]["name"]
                        ),
                        klass=StringVar(
                            value=raw["command"]["shortcut"]["registered_commands"][
                                "6"
                            ]["klass"]
                        ),
                    ),
                    "7": AppGuiCommandShortcut(
                        name=StringVar(
                            value=raw["command"]["shortcut"]["registered_commands"][
                                "7"
                            ]["name"]
                        ),
                        klass=StringVar(
                            value=raw["command"]["shortcut"]["registered_commands"][
                                "7"
                            ]["klass"]
                        ),
                    ),
                    "8": AppGuiCommandShortcut(
                        name=StringVar(
                            value=raw["command"]["shortcut"]["registered_commands"][
                                "8"
                            ]["name"]
                        ),
                        klass=StringVar(
                            value=raw["command"]["shortcut"]["registered_commands"][
                                "8"
                            ]["klass"]
                        ),
                    ),
                    "9": AppGuiCommandShortcut(
                        name=StringVar(
                            value=raw["command"]["shortcut"]["registered_commands"][
                                "9"
                            ]["name"]
                        ),
                        klass=StringVar(
                            value=raw["command"]["shortcut"]["registered_commands"][
                                "9"
                            ]["klass"]
                        ),
                    ),
                    "10": AppGuiCommandShortcut(
                        name=StringVar(
                            value=raw["command"]["shortcut"]["registered_commands"][
                                "10"
                            ]["name"]
                        ),
                        klass=StringVar(
                            value=raw["command"]["shortcut"]["registered_commands"][
                                "10"
                            ]["klass"]
                        ),
                    ),
                },
            ),
        ),
        notification=AppGuiNotificationSettings(
            line=AppGuiLineNotificationSettings(
                enabled_started=BooleanVar(
                    value=raw["notification"]["line"]["enabled_started"] == "True"
                ),
                enabled_ended=BooleanVar(
                    value=raw["notification"]["line"]["enabled_ended"] == "True"
                ),
            ),
            discord=AppGuiDiscordNotificationSettings(
                enabled_started=BooleanVar(
                    value=raw["notification"]["discord"]["enabled_started"] == "True"
                ),
                enabled_ended=BooleanVar(
                    value=raw["notification"]["discord"]["enabled_ended"] == "True"
                ),
            ),
        ),
        widget=AppGuiWidgetSettings(
            outputs=AppGuiOutputsWidgetSettings(
                size_balance=DoubleVar(
                    value=float(raw["widget"]["outputs"]["size_balance"])
                ),
                stdout=IntVar(value=int(raw["widget"]["outputs"]["stdout"])),
                visible_output1=BooleanVar(
                    value=raw["widget"]["outputs"]["visible_output1"] == "True"
                ),
                visible_output2=BooleanVar(
                    value=raw["widget"]["outputs"]["visible_output2"] == "True"
                ),
            ),
            software_controller=AppGuiSoftwareControllerWidgetSettings(
                position=StringVar(
                    value=raw["widget"]["software_controller"]["position"]
                ),
                visible=BooleanVar(
                    value=raw["widget"]["software_controller"]["visible"] == "True"
                ),
            ),
            dialog=AppGuiDialogWidgetSettings(
                confirm_buttons_position=StringVar(
                    value=raw["widget"]["dialog"]["confirm_buttons_position"]
                ),
            ),
        ),
    )


def save_state(
    state: AppGuiState,
    *,
    base_dir: str,
    profile: str,
) -> None:
    raw_state = {}
    for k in DEFAULT_GUI_STATE.keys():
        v = state.__dict__[k]
        if isinstance(v, list):
            raw_state[k] = [item.get() for item in v]
        elif isinstance(v, Variable):
            raw_state[k] = v.get()
        else:
            raise ValueError(f"Unsupported variable type: {type(v)}")

    # FIXME: save to state file
    print(raw_state)
