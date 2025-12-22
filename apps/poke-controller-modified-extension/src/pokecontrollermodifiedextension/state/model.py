import logging

from pokecontroller.core.camera import CameraDetector, CameraInfo
from pokecontroller.core.image import RawImage
from pokecontroller.core.notification import DiscordConfig, DiscordNotifier
from pokecontroller.core.notification.desktop import DesktopNotifier
from pokecontroller.core.serial import SerialPort, get_serial_ports

from pokecontrollermodifiedextension.core.exception import AppRuntimeException
from pokecontrollermodifiedextension.papico import get_papico
from pokecontrollermodifiedextension.state.info import get_app_info
from pokecontrollermodifiedextension.state.resources import get_app_resources
from pokecontrollermodifiedextension.state.runtime_info import get_app_runtime_info
from pokecontrollermodifiedextension.state.settings import get_app_settings

logger = logging.getLogger(__name__)


class AppModel:
    def __init__(self) -> None:
        self._runtime_info = get_app_runtime_info()
        self._app_resources = get_app_resources()
        self._app_info = get_app_info()
        self._app_settings = get_app_settings()
        self._papico = get_papico()

        app_name = self._app_info.name
        app_version = self._app_info.version
        base_dir = self._runtime_info.base_dir
        profile = self._runtime_info.profile
        self._discord_notifier = DiscordNotifier(
            config=DiscordConfig(
                path=base_dir / "profiles" / profile / "discord_token.ini"
            )
        )
        self._desktop_notifier = DesktopNotifier(
            title=f"{app_name} ver. {app_version}(profile: {profile})"
        )

    def load_camera_list(self) -> list[CameraInfo]:
        return CameraDetector(max_cameras=20).detect()

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

    def notify_desktop(self, message: str) -> None:
        self._desktop_notifier.notify(message=message)

    def notify_discord(
        self,
        message: str | None = None,
        image: RawImage | None = None,
    ) -> None:
        self._discord_notifier.notify(message=message, image=image)

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
