from abc import ABC, abstractmethod

from .state import PokeControllerAppState


class PokeControllerAppModel(ABC):
    def __init__(self, state: PokeControllerAppState):
        self._state = state

    @property
    def state(self) -> PokeControllerAppState:
        return self._state

    # Command Functionalities
    @abstractmethod
    def load_commands(self):
        pass

    @abstractmethod
    def start_command(self):
        pass

    @abstractmethod
    def stop_command(self):
        pass

    @abstractmethod
    def pause_command(self):
        pass

    # FIXME: 必要か検証する
    @abstractmethod
    def set_command_shortcut_number(self):
        pass

    @abstractmethod
    def register_command_shortcut(self):
        pass

    @abstractmethod
    def start_shortcut_command(self, shortcut_number: int):
        pass

    @abstractmethod
    def apply_python_commands_filter(self):
        pass

    # FIXME: 必要か検証する
    @abstractmethod
    def set_python_command(self):
        pass

    @abstractmethod
    def apply_mcu_commands_filter(self):
        pass

    # FIXME: 必要か検証する
    @abstractmethod
    def set_mcu_command(self):
        pass

    @abstractmethod
    def load_python_command_list(self) -> list[str]:
        pass

    @abstractmethod
    def load_python_commands_filter_list(self) -> list[str]:
        return ["-"]

    @abstractmethod
    def load_mcu_command_list(self) -> list[str]:
        pass

    @abstractmethod
    def load_mcu_commands_filter_list(self) -> list[str]:
        pass

    @abstractmethod
    def open_commands_directory_window(self):
        pass

    # Camera Functionalities
    @abstractmethod
    def load_camera_list(self) -> list[str]:
        pass

    @abstractmethod
    def load_camera_size_list(self) -> list[str]:
        pass

    @abstractmethod
    def connect_camera(self):
        pass

    # FIXME: 必要か検証する
    @abstractmethod
    def apply_camera_name(self):
        pass

    # FIXME: 必要か検証する
    @abstractmethod
    def apply_camera_fps(self):
        pass

    # FIXME: 必要か検証する
    @abstractmethod
    def apply_camera_size(self):
        pass

    # FIXME: 必要か検証する(多分いらない)
    @abstractmethod
    def apply_camera_show_realtime(self):
        pass

    @abstractmethod
    def apply_camera_show_matched(self):
        pass

    @abstractmethod
    def apply_camera_show_guide(self):
        pass

    @abstractmethod
    def save_screencapture(self):
        pass

    @abstractmethod
    def open_screencapture_directory_window(self):
        pass

    # Serial Functionalities
    @abstractmethod
    def load_serial_port_list(self) -> list[str]:
        pass

    @abstractmethod
    def load_serial_baud_rate_list(self) -> list[int]:
        pass

    @abstractmethod
    def load_serial_data_format_list(self) -> list[str]:
        pass

    @abstractmethod
    def connect_serial_port(self):
        pass

    @abstractmethod
    def disconnect_serial_port(self):
        pass

    # Controller Functionalities
    @abstractmethod
    def push_controller_button(self, button: str):
        pass

    @abstractmethod
    def release_controller_button(self, button: str):
        pass

    @abstractmethod
    def open_controller_window(self):
        pass

    @abstractmethod
    def apply_controller_data_format(self):
        pass

    @abstractmethod
    def open_software_controller_window(self):
        pass

    @abstractmethod
    def apply_enabled_keyboard(self):
        pass

    @abstractmethod
    def apply_enabled_lstick_mouse(self):
        pass

    @abstractmethod
    def apply_enabled_rstick_mouse(self):
        pass

    @abstractmethod
    def apply_enabled_pro_controller(self):
        pass

    @abstractmethod
    def apply_enabled_record_pro_controller(self):
        pass

    # Logging Functionalities
    @abstractmethod
    def clear_log_outputs(self):
        pass

    @abstractmethod
    def clear_log_output(self, output_id: int):
        pass

    @abstractmethod
    def apply_change_log_stdout(self):
        pass

    @abstractmethod
    def adjust_log_outputs_size(self):
        pass

    # Notification Functionalities
    @abstractmethod
    def notify_windows(self):
        pass

    @abstractmethod
    def notify_discord(self):
        pass

    @abstractmethod
    def notify_windows_force(self):
        pass

    @abstractmethod
    def notify_discord_force(self):
        pass

    @abstractmethod
    def apply_enabled_notify_windows_when_command_started(self):
        pass

    @abstractmethod
    def apply_enabled_notify_windows_when_command_ended(self):
        pass

    @abstractmethod
    def apply_enabled_notify_discord_when_command_started(self):
        pass

    @abstractmethod
    def apply_enabled_notify_discord_when_command_ended(self):
        pass

    # Widget Layout Functionalities
    @abstractmethod
    def apply_widget_layout(self):
        pass

    @abstractmethod
    def apply_outputs_visibility(self):
        pass

    @abstractmethod
    def apply_software_controller_visibility(self):
        pass

    @abstractmethod
    def apply_software_controller_position(self):
        pass

    @abstractmethod
    def apply_confirm_buttons_position(self):
        pass
