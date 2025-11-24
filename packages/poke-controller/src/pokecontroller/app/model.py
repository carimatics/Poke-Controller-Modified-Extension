from abc import ABC

from .state import PokeControllerAppState


class PokeControllerAppModel(ABC):
    def __init__(self, state: PokeControllerAppState):
        self._state = state

    @property
    def state(self) -> PokeControllerAppState:
        return self._state

    # Command Functionalities
    def load_commands(self):
        pass

    def start_command(self):
        pass

    def stop_command(self):
        pass

    def pause_command(self):
        pass

    # FIXME: 必要か検証する
    def set_command_shortcut_number(self):
        pass

    def register_command_shortcut(self):
        pass

    def start_shortcut_command(self, shortcut_number: int):
        pass

    def apply_python_commands_filter(self):
        pass

    # FIXME: 必要か検証する
    def set_python_command(self):
        pass

    def apply_mcu_commands_filter(self):
        pass

    # FIXME: 必要か検証する
    def set_mcu_command(self):
        pass

    def load_python_command_list(self) -> list[str]:
        return ["Command 1", "Command 2", "Command 3"]

    def load_python_commands_filter_list(self) -> list[str]:
        return ["-"]

    def load_mcu_command_list(self) -> list[str]:
        return ["Command 1", "Command 2", "Command 3"]

    def load_mcu_commands_filter_list(self) -> list[str]:
        return ["-"]

    def open_commands_directory_window(self):
        pass

    # Camera Functionalities
    def load_camera_list(self) -> list[str]:
        return ["Camera 1", "Camera 2", "Camera 3"]

    def load_camera_size_list(self) -> list[str]:
        return [f"{320 * i}x{180 * i}" for i in range(1, 7)]

    def connect_camera(self):
        pass

    # FIXME: 必要か検証する
    def apply_camera_name(self):
        pass

    # FIXME: 必要か検証する
    def apply_camera_fps(self):
        pass

    # FIXME: 必要か検証する
    def apply_camera_size(self):
        pass

    # FIXME: 必要か検証する(多分いらない)
    def apply_camera_show_realtime(self):
        pass

    def apply_camera_show_matched(self):
        pass

    def apply_camera_show_guide(self):
        pass

    def save_screencapture(self):
        pass

    def open_screencapture_directory_window(self):
        pass

    # Serial Functionalities
    def load_serial_port_list(self) -> list[str]:
        return ["COM1", "COM2", "COM3"]

    def load_serial_baud_rate_list(self) -> list[int]:
        return [4800, 9600, 115200]

    def load_serial_data_format_list(self) -> list[str]:
        return ["Default", "Qingpi", "3DS Controller"]

    def connect_serial_port(self):
        pass

    def disconnect_serial_port(self):
        pass

    # Controller Functionalities
    def push_controller_button(self, button: str):
        pass

    def release_controller_button(self, button: str):
        pass

    def open_controller_window(self):
        pass

    def apply_controller_data_format(self):
        pass

    def open_software_controller_window(self):
        pass

    def apply_enabled_keyboard(self):
        pass

    def apply_enabled_lstick_mouse(self):
        pass

    def apply_enabled_rstick_mouse(self):
        pass

    def apply_enabled_pro_controller(self):
        pass

    def apply_enabled_record_pro_controller(self):
        pass

    # Logging Functionalities
    def clear_log_outputs(self):
        self.clear_log_output(output_id=1)
        self.clear_log_output(output_id=2)

    def clear_log_output(self, output_id: int):
        pass

    def apply_change_log_stdout(self):
        pass

    def adjust_log_outputs_size(self):
        pass

    # Notification Functionalities
    def notify_windows(self):
        pass

    def notify_discord(self):
        pass

    def notify_windows_force(self):
        pass

    def notify_discord_force(self):
        pass

    def apply_enabled_notify_windows_when_command_started(self):
        pass

    def apply_enabled_notify_windows_when_command_ended(self):
        pass

    def apply_enabled_notify_discord_when_command_started(self):
        pass

    def apply_enabled_notify_discord_when_command_ended(self):
        pass

    # Widget Layout Functionalities
    def apply_widget_layout(self):
        pass

    def apply_outputs_visibility(self):
        pass

    def apply_software_controller_visibility(self):
        pass

    def apply_software_controller_position(self):
        pass

    def apply_confirm_buttons_position(self):
        pass
