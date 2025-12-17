import logging

from pokecontroller.core.dynamic import DynamicClassLoader
from pokecontroller.core.serial import SerialPort, get_serial_ports

from .api.v0_1_8.command.commands.base import Command
from .api.v0_1_8.command.commands.mcu.base import McuCommand
from .api.v0_1_8.command.commands.python.base import PythonCommand
from .api.v0_1_8.command.sender import Sender
from .exception import AppRuntimeException
from .info import get_app_info
from .resources import get_app_resources
from .runtime_info import get_app_runtime_info
from .settings import get_app_settings

logger = logging.getLogger(__name__)


class AppModel:
    def __init__(self) -> None:
        self._runtime_info = get_app_runtime_info()
        self._app_resources = get_app_resources()
        self._app_info = get_app_info()
        self._app_settings = get_app_settings()
        self._sender: Sender | None = None
        self._command: Command | None = None

    def load_commands(
        self,
    ) -> tuple[
        list[tuple[str, type[PythonCommand]]],
        list[tuple[str, type[McuCommand]]],
    ]:
        base_dir = self._runtime_info.base_dir / "Commands"

        python_commands = list(
            DynamicClassLoader(
                base_dir=base_dir / "PythonCommands",
                klass=PythonCommand,  # type: ignore[type-abstract]
            ).load()
        )
        mcu_commands = list(
            DynamicClassLoader(
                base_dir=base_dir / "McuCommands",
                klass=McuCommand,  # type: ignore[type-abstract]
            ).load()
        )
        return python_commands, mcu_commands

    def start_command(self, klass: type[Command]) -> None:
        logger.info("start_command")
        if self._command is not None:
            self._command.end(self._app_resources.sender_v0_1_8)
            self._command = None
        else:
            self._command = klass()
            sender = self._app_resources.sender_v0_1_8
            port = self._app_settings.serial.port.get()
            sender.openSerial(portNum=0, portName=port)
            klass().start(ser=sender)

    def stop_command(self) -> None:
        pass

    def pause_command(self) -> None:
        pass

    def set_command_shortcut_number(self) -> None:
        pass

    def register_command_shortcut(self) -> None:
        pass

    def start_shortcut_command(self, shortcut_number: int) -> None:
        pass

    def apply_python_commands_filter(self) -> None:
        pass

    def set_python_command(self) -> None:
        pass

    def apply_mcu_commands_filter(self) -> None:
        pass

    def set_mcu_command(self) -> None:
        pass

    def load_python_command_list(self) -> list[str]:
        return ["Python Command 1", "Python Command 2", "Python Command 3"]

    def load_python_commands_filter_list(self) -> list[str]:
        return ["-", "Python 1", "Python 2"]

    def load_mcu_command_list(self) -> list[str]:
        return ["MCU Command 1", "MCU Command 2", "MCU Command 3"]

    def load_mcu_commands_filter_list(self) -> list[str]:
        return ["-", "MCU 1", "MCU 2"]

    def open_commands_directory_window(self) -> None:
        pass

    def load_camera_list(self) -> list[str]:
        return ["0"]

    def load_camera_size_list(self) -> list[str]:
        return [f"{320 * i}x{180 * i}" for i in range(1, 7)]

    def connect_camera(self) -> None:
        pass

    def apply_camera_name(self) -> None:
        pass

    def apply_camera_fps(self) -> None:
        pass

    def apply_camera_size(self) -> None:
        pass

    def apply_camera_show_realtime(self) -> None:
        pass

    def apply_camera_show_matched(self) -> None:
        pass

    def apply_camera_show_guide(self) -> None:
        pass

    def save_screencapture(self) -> None:
        pass

    def open_screencapture_directory_window(self) -> None:
        pass

    def load_serial_ports(self) -> list[SerialPort]:
        return get_serial_ports()

    def load_serial_baud_rate_list(self) -> list[int]:
        return [4800, 9600, 115200]

    def load_serial_data_format_list(self) -> list[str]:
        return ["Default", "Qingpi", "3DS Controller"]

    def connect_serial_port(self) -> None:
        serial = get_app_resources().serial
        port = self._app_settings.serial.port.get()
        baud_rate = self._app_settings.serial.baud_rate.get()
        serial.open(port_path=port, baud_rate=baud_rate)

    def disconnect_serial_port(self) -> None:
        pass

    def push_controller_button(self, button: str) -> None:
        pass

    def release_controller_button(self, button: str) -> None:
        pass

    def apply_controller_data_format(self) -> None:
        pass

    def open_software_controller_window(self) -> None:
        pass

    def apply_enabled_keyboard(self) -> None:
        pass

    def apply_enabled_lstick_mouse(self) -> None:
        pass

    def apply_enabled_rstick_mouse(self) -> None:
        pass

    def apply_enabled_pro_controller(self) -> None:
        pass

    def apply_enabled_record_pro_controller(self) -> None:
        pass

    def clear_log_outputs(self) -> None:
        self.clear_log_output(output_id=1)
        self.clear_log_output(output_id=2)

    def clear_log_output(self, output_id: int) -> None:
        pass

    def apply_change_log_stdout(self) -> None:
        pass

    def adjust_log_outputs_size(self) -> None:
        pass

    def notify_windows(self) -> None:
        pass

    def notify_discord(self) -> None:
        pass

    def notify_windows_force(self) -> None:
        pass

    def notify_discord_force(self) -> None:
        pass

    def apply_enabled_notify_windows_when_command_started(self) -> None:
        pass

    def apply_enabled_notify_windows_when_command_ended(self) -> None:
        pass

    def apply_enabled_notify_discord_when_command_started(self) -> None:
        pass

    def apply_enabled_notify_discord_when_command_ended(self) -> None:
        pass

    def apply_widget_layout(self) -> None:
        pass

    def apply_outputs_visibility(self) -> None:
        pass

    def apply_software_controller_visibility(self) -> None:
        pass

    def apply_software_controller_position(self) -> None:
        pass

    def apply_confirm_buttons_position(self) -> None:
        pass


_app_model: AppModel | None = None


def get_app_model() -> AppModel:
    global _app_model
    if _app_model is None:
        raise AppRuntimeException("App model is not initialized.")
    return _app_model


def setup_app_model() -> AppModel:
    global _app_model
    _app_model = AppModel()
    return _app_model
