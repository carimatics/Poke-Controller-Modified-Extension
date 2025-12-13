import configparser
import logging
import os
import tkinter as tk

logger = logging.getLogger(__name__)

DEFAULT_SETTING: dict[str, dict[str, str]] = {
    "General Setting": {
        "camera_id": "0",
        "com_port": "0",
        "com_port_name": "0",
        "baud_rate": "9600",
        "fps": "45",
        "show_size": "640x360",
        "is_show_realtime": "True",
        "is_show_value": "False",
        "is_show_guide": "False",
        "is_show_serial": "False",
        "is_use_keyboard": "True",
        "serial_data_format_name": "Default",
        "touchscreen_start_x": "1",
        "touchscreen_start_y": "1",
        "touchscreen_end_x": "320",
        "touchscreen_end_y": "240",
    },
    "Pokemon Home": {
        "Season": "1",
        "Single or Double": "シングル",
    },
    "KeyMap-Button": {
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
    },
    "KeyMap-Direction": {
        "Direction.UP": "Key.up",
        "Direction.RIGHT": "Key.right",
        "Direction.DOWN": "Key.down",
        "Direction.LEFT": "Key.left",
        "Direction.UP_RIGHT": "20001",
        "Direction.DOWN_RIGHT": "20002",
        "Direction.DOWN_LEFT": "20010",
        "Direction.UP_LEFT": "20011",
    },
    "KeyMap-Hat": {
        "Hat.TOP": "10000",
        "Hat.TOP_RIGHT": "10001",
        "Hat.RIGHT": "10010",
        "Hat.BTM_RIGHT": "10011",
        "Hat.BTM": "10100",
        "Hat.BTM_LEFT": "10101",
        "Hat.LEFT": "10110",
        "Hat.TOP_LEFT": "10111",
        "Hat.CENTER": "11000",
    },
    "Shortcut": {
        "command_class_1": "None",
        "command_name_1": "(empty)",
        "command_class_2": "None",
        "command_name_2": "(empty)",
        "command_class_3": "None",
        "command_name_3": "(empty)",
        "command_class_4": "None",
        "command_name_4": "(empty)",
        "command_class_5": "None",
        "command_name_5": "(empty)",
        "command_class_6": "None",
        "command_name_6": "(empty)",
        "command_class_7": "None",
        "command_name_7": "(empty)",
        "command_class_8": "None",
        "command_name_8": "(empty)",
        "command_class_9": "None",
        "command_name_9": "(empty)",
        "command_class_10": "None",
        "command_name_10": "(empty)",
    },
    "Notification": {
        "is_win_notification_start": "False",
        "is_win_notification_end": "False",
        "is_line_notification_start": "False",
        "is_line_notification_end": "False",
        "is_discord_notification_start": "False",
        "is_discord_notification_end": "False",
    },
    "Output": {
        "area_size": "20",
        "stdout_destination": "1",
        "widget_mode": "ALL (default)",
        "software_controller_position": "2",
        "dialogue_buttons_position": "2",
    },
}


class GuiSettings:
    SETTING_PATH = os.path.join(
        os.path.dirname(__file__), "profiles", "default", "settings.ini"
    )

    def __init__(self) -> None:
        self.setting = configparser.ConfigParser()
        self._initialize_setting()

        general_setting = self.setting["General Setting"]
        self.camera_id = tk.IntVar(
            value=general_setting.getint("camera_id"),
        )
        self.com_port = tk.IntVar(
            value=general_setting.getint("com_port"),
        )
        self.com_port_name = tk.StringVar(
            value=general_setting.get("com_port_name"),
        )
        self.baud_rate = tk.IntVar(
            value=general_setting.getint("baud_rate"),
        )
        self.fps = tk.StringVar(
            value=general_setting["fps"],
        )
        self.show_size = tk.StringVar(value=general_setting.get("show_size"))
        self.is_show_realtime = tk.BooleanVar(
            value=general_setting.getboolean("is_show_realtime")
        )
        self.is_show_value = tk.BooleanVar(
            value=general_setting.getboolean("is_show_value")
        )
        self.is_show_guide = tk.BooleanVar(
            value=general_setting.getboolean("is_show_guide")
        )
        self.is_show_serial = tk.BooleanVar(
            value=general_setting.getboolean("is_show_serial")
        )
        self.is_use_keyboard = tk.BooleanVar(
            value=general_setting.getboolean("is_use_keyboard")
        )
        self.serial_data_format_name = tk.StringVar(
            value=general_setting["serial_data_format_name"]
        )
        self.touchscreen_start_x = general_setting.getint("touchscreen_start_x")
        self.touchscreen_start_y = general_setting.getint("touchscreen_start_y")
        self.touchscreen_end_x = general_setting.getint("touchscreen_end_x")
        self.touchscreen_end_y = general_setting.getint("touchscreen_end_y")

        # Pokemon Home用の設定
        pokemon_home = self.setting["Pokemon Home"]
        self.season = tk.StringVar(value=pokemon_home.get("Season"))
        self.is_SingleBattle = tk.StringVar(value=pokemon_home.get("Single or Double"))

        # Shortcut用の設定
        shortcut = self.setting["Shortcut"]
        self.command_class_dict: dict[str, str] = {}
        self.command_name_dict: dict[str, tk.StringVar] = {}
        for i in range(1, 11):
            key = str(i)
            self.command_class_dict[key] = shortcut[f"command_class_{key}"]
            self.command_name_dict[key] = tk.StringVar(
                value=shortcut[f"command_name_{key}"]
            )

        # Notification用の設定
        notification = self.setting["Notification"]
        self.is_win_notification_start = tk.BooleanVar(
            value=notification.getboolean("is_win_notification_start")
        )
        self.is_win_notification_end = tk.BooleanVar(
            value=notification.getboolean("is_win_notification_end")
        )
        self.is_line_notification_start = tk.BooleanVar(
            value=notification.getboolean("is_line_notification_start")
        )
        self.is_line_notification_end = tk.BooleanVar(
            value=notification.getboolean("is_line_notification_end")
        )
        self.is_discord_notification_start = tk.BooleanVar(
            value=notification.getboolean("is_discord_notification_start")
        )
        self.is_discord_notification_end = tk.BooleanVar(
            value=notification.getboolean("is_discord_notification_end")
        )

        # Output Area用の設定
        output = self.setting["Output"]
        self.area_size = output["area_size"]
        self.stdout_destination = output["stdout_destination"]
        self.right_frame_widget_mode = output["widget_mode"]
        self.pos_software_controller = output["software_controller_position"]
        self.pos_dialogue_buttons = output["dialogue_buttons_position"]

    def load(self) -> None:
        if os.path.isfile(self.SETTING_PATH):
            self.setting.read(self.SETTING_PATH, encoding="utf-8")

    def generate(self) -> None:
        for section, options in DEFAULT_SETTING.items():
            self.setting[section] = dict(options)
        with open(self.SETTING_PATH, "w", encoding="utf-8") as file:
            self.setting.write(file)
        os.chmod(path=self.SETTING_PATH, mode=0o777)

    def save(self, path: str | None = None) -> None:
        # update setting values
        self._general_setting_to_config()
        self._pokemon_home_setting_to_config()
        self._shortcut_setting_to_config()
        self._notification_setting_to_config()
        self._output_setting_to_config()

        with open(self.SETTING_PATH, "w", encoding="utf-8") as file:
            self.setting.write(file)
        os.chmod(path=self.SETTING_PATH, mode=0o777)
        logger.debug("Settings file has been saved.")

    def _initialize_setting(self) -> None:
        self.setting.optionxform = str  # type: ignore[method-assign, assignment]

        # generate setting file
        if not os.path.exists(self.SETTING_PATH):
            logger.debug("Setting file does not exists.")
            self.generate()
            logger.debug("Settings file has been generated.")
        else:
            logger.debug("Setting file exists.")

        # load setting file
        self.load()
        logger.debug("Settings file has been loaded.")

        # fill by default values if not exist
        sections = self.setting.sections()
        for section, options in DEFAULT_SETTING.items():
            if section not in sections:
                self.setting[section] = {}
            for option, val in options.items():
                self.setting[section].setdefault(option, val)

    def _general_setting_to_config(self) -> None:
        self.setting["General Setting"] = {
            "camera_id": str(self.camera_id.get()),
            "com_port": str(self.com_port.get()),
            "com_port_name": self.com_port_name.get(),
            "baud_rate": str(self.baud_rate.get()),
            "fps": self.fps.get(),
            "show_size": self.show_size.get(),
            "is_show_realtime": str(self.is_show_realtime.get()),
            "is_show_value": str(self.is_show_value.get()),
            "is_show_guide": str(self.is_show_guide.get()),
            "is_show_serial": str(self.is_show_serial.get()),
            "is_use_keyboard": str(self.is_use_keyboard.get()),
            "serial_data_format_name": self.serial_data_format_name.get(),
            "touchscreen_start_x": str(self.touchscreen_start_x),
            "touchscreen_start_y": str(self.touchscreen_start_y),
            "touchscreen_end_x": str(self.touchscreen_end_x),
            "touchscreen_end_y": str(self.touchscreen_end_y),
        }

    def _pokemon_home_setting_to_config(self) -> None:
        self.setting["Pokemon Home"] = {
            "Season": self.season.get(),
            "Single or Double": self.is_SingleBattle.get(),
        }

    def _shortcut_setting_to_config(self) -> None:
        shortcut_setting = {}
        for i in range(1, 11):
            key = str(i)
            shortcut_setting[f"command_class_{i}"] = self.command_class_dict[key]
            shortcut_setting[f"command_name_{i}"] = self.command_name_dict[key].get()
        self.setting["Shortcut"] = shortcut_setting

    def _notification_setting_to_config(self) -> None:
        self.setting["Notification"] = {
            "is_win_notification_start": str(self.is_win_notification_start.get()),
            "is_win_notification_end": str(self.is_win_notification_end.get()),
            "is_line_notification_start": str(self.is_line_notification_start.get()),
            "is_line_notification_end": str(self.is_line_notification_end.get()),
            "is_discord_notification_start": str(
                self.is_discord_notification_start.get()
            ),
            "is_discord_notification_end": str(self.is_discord_notification_end.get()),
        }

    def _output_setting_to_config(self) -> None:
        self.setting["Output"] = {
            "area_size": self.area_size,
            "stdout_destination": self.stdout_destination,
            "widget_mode": self.right_frame_widget_mode,
            "software_controller_position": self.pos_software_controller,
            "dialogue_buttons_position": self.pos_dialogue_buttons,
        }
