from configparser import ConfigParser

from ......state import AppGuiState


def to_state(config: ConfigParser) -> AppGuiState:
    widget_mode = config["Output"]["widget_mode"]
    visible_output1 = "ALL" in widget_mode or "Output#1" in widget_mode
    visible_output2 = "ALL" in widget_mode or "Output#2" in widget_mode
    visible_software_controller = (
        "ALL" in widget_mode or "Software-Controller" in widget_mode
    )
    software_controller_position = config["Output"]["software_controller_position"]
    dialogue_buttons_position = config["Output"]["dialogue_buttons_position"]
    if dialogue_buttons_position == "1":
        dialog_buttons_position = "top"
    elif dialogue_buttons_position == "2":
        dialog_buttons_position = "bottom"
    else:
        dialog_buttons_position = "both"
    state_dict = {
        "general": {
            "theme": config["General Setting"]["theme"],
            "version": config["General Setting"]["version"],
        },
        "capture": {
            "camera_id": config["General Setting"].getint("camera_id"),
            "camera_name": config["General Setting"]["camera_name"],
            "fps": config["General Setting"].getint("fps"),
            "size": config["General Setting"]["show_size"],
            "show_realtime": config["General Setting"].getboolean("is_show_realtime"),
            "show_matched": config["General Setting"].getboolean("is_show_value"),
            "show_guide": config["General Setting"].getboolean("is_show_guide"),
        },
        "serial": {
            "port": config["General Setting"]["com_port"],
            "port_name": config["General Setting"]["com_port_name"],
            "baud_rate": config["General Setting"].getint("baud_rate"),
            "data_format": config["General Setting"]["serial_data_format_name"],
            "show_data": config["General Setting"].getboolean("is_show_serial"),
        },
        "device_input": {
            "touchscreen": {
                "sx": config["General Setting"].getint("touchscreen_start_x"),
                "sy": config["General Setting"].getint("touchscreen_start_y"),
                "ex": config["General Setting"].getint("touchscreen_end_x"),
                "ey": config["General Setting"].getint("touchscreen_end_y"),
            },
            "enabled_keyboard": config["General Setting"].getboolean("is_use_keyboard"),
            "enabled_lstick_mouse": config["General Setting"].getboolean(
                "is_use_lstick_mouse"
            ),
            "enabled_rstick_mouse": config["General Setting"].getboolean(
                "is_use_rstick_mouse"
            ),
            "enabled_pro_controller": config["General Setting"].getboolean(
                "is_use_pro_controller"
            ),
            "enabled_record_pro_controller": config["General Setting"].getboolean(
                "is_use_record_pro_controller"
            ),
        },
        "command": {
            "python_commands_filter": "-",
            "python_command": "",
            "mcu_commands_filter": "-",
            "mcu_command": "",
            "shortcut": {
                "number": 1,
                "registered_commands": {
                    str(i): {
                        "klass": config["Shortcut"][f"command_class_{i}"],
                        "name": config["Shortcut"][f"command_name_{i}"],
                    }
                    for i in range(1, 11)
                },
            },
        },
        "notification": {
            "line": {
                "enabled_started": config["Notification"].getboolean(
                    "is_line_notification_start"
                ),
                "enabled_ended": config["Notification"].getboolean(
                    "is_line_notification_end"
                ),
            },
            "windows": {
                "enabled_started": config["Notification"].getboolean(
                    "is_win_notification_start"
                ),
                "enabled_ended": config["Notification"].getboolean(
                    "is_win_notification_end"
                ),
            },
            "discord": {
                "enabled_started": config["Notification"].getboolean(
                    "is_discord_notification_start"
                ),
                "enabled_ended": config["Notification"].getboolean(
                    "is_discord_notification_end"
                ),
            },
        },
        "widget": {
            "outputs": {
                "size_balance": config["Output"].getfloat("area_size"),
                "stdout": config["Output"].getint("stdout_destination"),
                "visible_output1": visible_output1,
                "visible_output2": visible_output2,
            },
            "software_controller": {
                "position": "top" if software_controller_position == "1" else "bottom",
                "visible": visible_software_controller,
            },
            "dialog": {
                "confirm_buttons_position": dialog_buttons_position,
            },
        },
    }

    return AppGuiState.from_dict(state_dict)


def to_config(state: AppGuiState) -> ConfigParser:
    config = ConfigParser(allow_no_value=True)
    config.optionxform = str  # type: ignore[assignment]

    visible_output1 = state.widget.outputs.visible_output1.get()
    visible_output2 = state.widget.outputs.visible_output2.get()
    visible_software_controller = state.widget.software_controller.visible.get()
    widget_mode_list = []
    if all((visible_output1, visible_output2, visible_software_controller)):
        widget_mode = "ALL (default)"
    else:
        if visible_output1:
            widget_mode_list.append("Output#1")
        if visible_output2:
            widget_mode_list.append("Output#2")
        if visible_software_controller:
            widget_mode_list.append("Software-Controller")

        if len(widget_mode_list) == 1:
            widget_mode = f"{widget_mode_list[0]} Only"
        else:
            widget_mode = " + ".join(widget_mode_list)

    software_controller_position = state.widget.software_controller.position.get()
    if software_controller_position == "top":
        software_controller_position_num = "1"
    else:
        software_controller_position_num = "2"

    dialog_buttons_position = state.widget.dialog.confirm_buttons_position.get()
    if dialog_buttons_position == "top":
        dialogue_buttons_position_num = "1"
    elif dialog_buttons_position == "bottom":
        dialogue_buttons_position_num = "2"
    else:
        dialogue_buttons_position_num = "3"

    config["General Setting"] = {
        "theme": state.general.theme.get(),
        "version": state.general.version.get(),
        "camera_id": str(state.capture.camera_id.get()),
        "camera_name": state.capture.camera_name.get(),
        "com_port": str(state.serial.port.get()),
        "com_port_name": state.serial.port_name.get(),
        "baud_rate": str(state.serial.baud_rate.get()),
        "fps": str(state.capture.fps.get()),
        "show_size": str(state.capture.size.get()),
        "is_show_realtime": str(state.capture.show_realtime.get()),
        "is_show_value": str(state.capture.show_matched.get()),
        "is_show_guide": str(state.capture.show_guide.get()),
        "is_show_serial": str(state.serial.show_data.get()),
        "is_use_keyboard": str(state.device_input.enabled_keyboard.get()),
        "is_use_lstick_mouse": str(state.device_input.enabled_lstick_mouse.get()),
        "is_use_rstick_mouse": str(state.device_input.enabled_rstick_mouse.get()),
        "is_use_pro_controller": str(state.device_input.enabled_pro_controller.get()),
        "is_use_record_pro_controller": str(
            state.device_input.enabled_record_pro_controller.get()
        ),
        "serial_data_format_name": state.serial.data_format.get(),
        "touchscreen_start_x": str(state.device_input.touchscreen.sx.get()),
        "touchscreen_start_y": str(state.device_input.touchscreen.sy.get()),
        "touchscreen_end_x": str(state.device_input.touchscreen.ex.get()),
        "touchscreen_end_y": str(state.device_input.touchscreen.ey.get()),
    }
    # FIXME
    config["Pokemon Home"] = {
        "Season": "1",
        "Single or Double": "シングル",
    }
    # FIXME
    config["KeyMap-Button"] = {
        "Button.Y": "y",
        "Button.B": "b",
        "Button.X": "x",
        "Button.A": "a",
        "Button.L": "l",
        "Button.R": "r",
        "Button.ZL": "k",
        "Button.ZR": "e",
        "Button.MINUS": "m",
        "Button.PLUS": "p",
        "Button.LCLICK": "q",
        "Button.RCLICK": "w",
        "Button.HOME": "h",
        "Button.CAPTURE": "c",
    }
    # FIXME
    config["KeyMap-Direction"] = {
        "Direction.UP": "Key.up",
        "Direction.RIGHT": "Key.right",
        "Direction.DOWN": "Key.down",
        "Direction.LEFT": "Key.left",
        "Direction.UP_RIGHT": "20001",
        "Direction.DOWN_RIGHT": "20002",
        "Direction.DOWN_LEFT": "20010",
        "Direction.UP_LEFT": "20011",
    }
    config["KeyMap-Hat"] = {
        "Hat.TOP": "10000",
        "Hat.TOP_RIGHT": "10001",
        "Hat.RIGHT": "10010",
        "Hat.BTM_RIGHT": "10011",
        "Hat.BTM": "10100",
        "Hat.BTM_LEFT": "10101",
        "Hat.LEFT": "10110",
        "Hat.TOP_LEFT": "10111",
        "Hat.CENTER": "11000",
    }
    registered_commands = state.command.shortcut.registered_commands
    shortcuts = {}
    for i in range(1, 11):
        shortcuts[f"command_class_{i}"] = registered_commands[str(i)].klass.get()
        shortcuts[f"command_name_{i}"] = registered_commands[str(i)].name.get()
    config["Shortcut"] = shortcuts
    config["Notification"] = {
        "is_win_notification_start": str(
            state.notification.windows.enabled_started.get()
        ),
        "is_win_notification_end": str(state.notification.windows.enabled_ended.get()),
        "is_line_notification_start": str(
            state.notification.line.enabled_started.get()
        ),
        "is_line_notification_end": str(state.notification.line.enabled_ended.get()),
        "is_discord_notification_start": str(
            state.notification.discord.enabled_started.get()
        ),
        "is_discord_notification_end": str(
            state.notification.discord.enabled_ended.get()
        ),
    }
    config["Output"] = {
        "area_size": str(state.widget.outputs.size_balance.get()),
        "stdout_destination": str(state.widget.outputs.stdout.get()),
        "widget_mode": widget_mode,
        "software_controller_position": software_controller_position_num,
        "dialogue_buttons_position": dialogue_buttons_position_num,
    }

    return config
