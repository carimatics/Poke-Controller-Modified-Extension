from configparser import ConfigParser

from ......state import AppGuiState


def config_to_state(config: ConfigParser) -> AppGuiState:
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
                        "name": config["Shortcut"][f"command_class_{i}"],
                        "klass": config["Shortcut"][f"command_name_{i}"],
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
