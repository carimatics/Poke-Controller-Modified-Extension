from dataclasses import fields, is_dataclass
from tkinter import BooleanVar, DoubleVar, IntVar, StringVar
from typing import Any

# @formatter:off (for PyCharm)
# fmt: off
SETTINGS_TEMPLATE: str = """
[general]
theme = "${general.theme}"
version = "${general.version}"

[capture]
camera_id = ${capture.camera_id}
camera_name = "${capture.camera_name}"
fps = ${capture.fps}
size = "${capture.size}"
show_realtime = ${capture.show_realtime}
show_matched = ${capture.show_matched}
show_guide = ${capture.show_guide}

[serial]
port = "${serial.port}"
port_name = "${serial.port_name}"
baud_rate = ${serial.baud_rate}
data_format = "${serial.data_format}"
show_data = ${serial.show_data}

[device_input]
touchscreen.sx = ${device_input.touchscreen.sx}
touchscreen.sy = ${device_input.touchscreen.sy}
touchscreen.ex = ${device_input.touchscreen.ex}
touchscreen.ey = ${device_input.touchscreen.ey}
enabled_keyboard = ${device_input.enabled_keyboard}
enabled_lstick_mouse = ${device_input.enabled_lstick_mouse}
enabled_rstick_mouse = ${device_input.enabled_rstick_mouse}
enabled_pro_controller = ${device_input.enabled_pro_controller}
enabled_record_pro_controller = ${device_input.enabled_record_pro_controller}

[command]
python_commands_filter = "${command.python_commands_filter}"
python_command = "${command.python_command}"
mcu_commands_filter = "${command.mcu_commands_filter}"
mcu_command = "${command.mcu_command}"

[command.shortcut]
number = ${command.shortcut.number}

[command.shortcut.registered_commands]
1.name = "${command.shortcut.registered_commands.1.name}"
1.klass = "${command.shortcut.registered_commands.1.klass}"
2.name = "${command.shortcut.registered_commands.2.name}"
2.klass = "${command.shortcut.registered_commands.2.klass}"
3.name = "${command.shortcut.registered_commands.3.name}"
3.klass = "${command.shortcut.registered_commands.3.klass}"
4.name = "${command.shortcut.registered_commands.4.name}"
4.klass = "${command.shortcut.registered_commands.4.klass}"
5.name = "${command.shortcut.registered_commands.5.name}"
5.klass = "${command.shortcut.registered_commands.5.klass}"
6.name = "${command.shortcut.registered_commands.6.name}"
6.klass = "${command.shortcut.registered_commands.6.klass}"
7.name = "${command.shortcut.registered_commands.7.name}"
7.klass = "${command.shortcut.registered_commands.7.klass}"
8.name = "${command.shortcut.registered_commands.8.name}"
8.klass = "${command.shortcut.registered_commands.8.klass}"
9.name = "${command.shortcut.registered_commands.9.name}"
9.klass = "${command.shortcut.registered_commands.9.klass}"
10.name = "${command.shortcut.registered_commands.10.name}"
10.klass = "${command.shortcut.registered_commands.10.klass}"

[notification]
windows.enabled_started = ${notification.windows.enabled_started}
windows.enabled_ended = ${notification.windows.enabled_ended}
line.enabled_started = ${notification.line.enabled_started}
line.enabled_ended = ${notification.line.enabled_ended}
discord.enabled_started = ${notification.discord.enabled_started}
discord.enabled_ended = ${notification.discord.enabled_ended}

[widget]
outputs.size_balance = ${widget.outputs.size_balance}
outputs.stdout = ${widget.outputs.stdout}
outputs.visible_output1 = ${widget.outputs.visible_output1}
outputs.visible_output2 = ${widget.outputs.visible_output2}
software_controller.position = "${widget.software_controller.position}"
software_controller.visible = ${widget.software_controller.visible}
dialog.confirm_buttons_position = "${widget.dialog.confirm_buttons_position}"
""".strip()
# fmt: on
# @formatter:on


def to_dict(state: Any) -> dict[str, Any]:
    if isinstance(state, dict):
        return {k: to_dict(v) for k, v in state.items()}

    if not is_dataclass(state):
        raise ValueError(f"unsupported type: {type(state)}")

    result: dict[str, Any] = {}
    for field in fields(state):
        k, v = field.name, getattr(state, field.name)
        if isinstance(v, BooleanVar):
            result[k] = "true" if v.get() else "false"
        elif isinstance(v, (StringVar, IntVar, DoubleVar)):
            result[k] = v.get()
        else:
            result[k] = to_dict(v)
    return result
