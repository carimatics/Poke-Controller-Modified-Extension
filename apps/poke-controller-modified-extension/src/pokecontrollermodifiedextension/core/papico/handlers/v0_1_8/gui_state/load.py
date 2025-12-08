from configparser import ConfigParser
from pathlib import Path

from ......state import AppGuiState
from ....context import PapicoExecContext, PapicoResult
from ....exception import PapicoGuiStateLoadHandlerException
from ....handlers.handler import PapicoHandler

# @formatter:off (for PyCharm)
# fmt: off
DEFAULT_SETTINGS = """
[General Setting]
theme = Default
version = 0.1.8
camera_id = 0
camera_name =
com_port = 0
com_port_name = 
baud_rate = 9600
fps = 45
show_size = 640x360
is_show_realtime = True
is_show_value = False
is_show_guide = False
is_show_serial = False
is_use_keyboard = True
is_use_lstick_mouse = True
is_use_rstick_mouse = True
is_use_pro_controller = False
is_use_record_pro_controller = False
serial_data_format_name = Default
touchscreen_start_x = 1
touchscreen_start_y = 1
touchscreen_end_x = 320
touchscreen_end_y = 240

[Pokemon Home]
Season = 1
Single or Double = シングル

[KeyMap-Button]
Button.Y = y
Button.B = b
Button.X = x
Button.A = a
Button.L = l
Button.R = r
Button.ZL = k
Button.ZR = e
Button.MINUS = m
Button.PLUS = p
Button.LCLICK = q
Button.RCLICK = w
Button.HOME = h
Button.CAPTURE = c

[KeyMap-Direction]
Direction.UP = Key.up
Direction.RIGHT = Key.right
Direction.DOWN = Key.down
Direction.LEFT = Key.left
Direction.UP_RIGHT = 20001
Direction.DOWN_RIGHT = 20002
Direction.DOWN_LEFT = 20010
Direction.UP_LEFT = 20011

[KeyMap-Hat]
Hat.TOP = 10000
Hat.TOP_RIGHT = 10001
Hat.RIGHT = 10010
Hat.BTM_RIGHT = 10011
Hat.BTM = 10100
Hat.BTM_LEFT = 10101
Hat.LEFT = 10110
Hat.TOP_LEFT = 10111
Hat.CENTER = 11000

[Shortcut]
command_class_1 = None
command_name_1 = (empty)
command_class_2 = None
command_name_2 = (empty)
command_class_3 = None
command_name_3 = (empty)
command_class_4 = None
command_name_4 = (empty)
command_class_5 = None
command_name_5 = (empty)
command_class_6 = None
command_name_6 = (empty)
command_class_7 = None
command_name_7 = (empty)
command_class_8 = None
command_name_8 = (empty)
command_class_9 = None
command_name_9 = (empty)
command_class_10 = None
command_name_10 = (empty)

[Notification]
is_win_notification_start = False
is_win_notification_end = False
is_line_notification_start = False
is_line_notification_end = False
is_discord_notification_start = False
is_discord_notification_end = False

[Output]
area_size = 20
stdout_destination = 1
widget_mode = ALL (default)
software_controller_position = 2
dialogue_buttons_position = 2
""".strip()
# fmt: on
# @formatter:on


class PapicoGuiStateLoadHandler(PapicoHandler):
    def handle(self, ctx: PapicoExecContext) -> PapicoResult[AppGuiState]:
        try:
            path: str = ctx.params["path"]
            config = self._read_config(path)
            self._fill_by_default(config)
            return PapicoResult(
                success=True,
                ctx=ctx,
                data=self._config_to_state(config),
            )
        except Exception as e:
            default = ConfigParser(allow_no_value=True)
            default.read_string(DEFAULT_SETTINGS)
            return PapicoResult(
                success=False,
                ctx=ctx,
                data=self._config_to_state(default),
                error=PapicoGuiStateLoadHandlerException(
                    f"{e}",
                ),
            )

    def _read_config(self, path: str) -> ConfigParser:
        p = Path(path)
        config = ConfigParser(
            allow_no_value=True,
            comment_prefixes=("#", ";"),
        )
        config.optionxform = str  # type: ignore[assignment]

        if not p.exists() or not p.is_file():
            return config

        try:
            config.read(path, encoding="utf-8")
        except Exception as e:
            raise PapicoGuiStateLoadHandlerException(
                f"Config could not read: {e}",
            ) from e

        return config

    def _fill_by_default(self, config: ConfigParser) -> None:
        default = ConfigParser(allow_no_value=True)
        default.read_string(DEFAULT_SETTINGS)

        # General Setting
        sections = default.sections()
        for section in sections:
            if not config.has_section(section):
                config.add_section(section)
            for key, value in default.items(section):
                config[section].setdefault(key, value)

    def _config_to_state(self, config: ConfigParser) -> AppGuiState:
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
                "show_realtime": config["General Setting"].getboolean(
                    "is_show_realtime"
                ),
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
                "enabled_keyboard": config["General Setting"].getboolean(
                    "is_use_keyboard"
                ),
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
                    "position": "top"
                    if software_controller_position == "1"
                    else "bottom",
                    "visible": visible_software_controller,
                },
                "dialog": {
                    "confirm_buttons_position": dialog_buttons_position,
                },
            },
        }

        return AppGuiState.from_dict(state_dict)
