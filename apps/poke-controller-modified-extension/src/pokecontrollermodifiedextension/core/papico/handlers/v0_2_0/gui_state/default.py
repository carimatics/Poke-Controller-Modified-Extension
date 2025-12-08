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
1.name = "(empty)"
1.klass = "None"
2.name = "(empty)"
2.klass = "None"
3.name = "(empty)"
3.klass = "None"
4.name = "(empty)"
4.klass = "None"
5.name = "(empty)"
5.klass = "None"
6.name = "(empty)"
6.klass = "None"
7.name = "(empty)"
7.klass = "None"
8.name = "(empty)"
8.klass = "None"
9.name = "(empty)"
9.klass = "None"
10.name = "(empty)"
10.klass = "None"

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
