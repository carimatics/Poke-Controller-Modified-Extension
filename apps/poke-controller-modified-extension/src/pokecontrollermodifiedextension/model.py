from .state import AppState
from .info import AppInfo


class AppModel:
    def __init__(self, info: AppInfo, state: AppState):
        self._info = info
        self._state = state

    @property
    def info(self) -> AppInfo:
        return self._info

    @property
    def state(self) -> AppState:
        return self._state

    def load_commands(self) -> list[str]:
        return []

    def start_command(self) -> None:
        pass

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
        return ["Camera 1", "Camera 2", "Camera 3"]

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

    def load_serial_port_list(self) -> list[str]:
        return ["COM1", "COM2", "COM3"]

    def load_serial_baud_rate_list(self) -> list[int]:
        return [4800, 9600, 115200]

    def load_serial_data_format_list(self) -> list[str]:
        return ["Default", "Qingpi", "3DS Controller"]

    def connect_serial_port(self) -> None:
        pass

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
