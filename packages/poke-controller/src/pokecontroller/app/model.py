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
    def load_commands(self) -> list[str]: ...

    @abstractmethod
    def start_command(self) -> None: ...

    @abstractmethod
    def stop_command(self) -> None: ...

    @abstractmethod
    def pause_command(self) -> None: ...

    # FIXME: 必要か検証する
    @abstractmethod
    def set_command_shortcut_number(self) -> None: ...

    @abstractmethod
    def register_command_shortcut(self) -> None: ...

    @abstractmethod
    def start_shortcut_command(self, shortcut_number: int) -> None: ...

    @abstractmethod
    def apply_python_commands_filter(self) -> None: ...

    # FIXME: 必要か検証する
    @abstractmethod
    def set_python_command(self) -> None: ...

    @abstractmethod
    def apply_mcu_commands_filter(self) -> None: ...

    # FIXME: 必要か検証する
    @abstractmethod
    def set_mcu_command(self) -> None: ...

    @abstractmethod
    def load_python_command_list(self) -> list[str]: ...

    @abstractmethod
    def load_python_commands_filter_list(self) -> list[str]: ...

    @abstractmethod
    def load_mcu_command_list(self) -> list[str]: ...

    @abstractmethod
    def load_mcu_commands_filter_list(self) -> list[str]: ...

    @abstractmethod
    def open_commands_directory_window(self) -> None: ...

    # Camera Functionalities
    @abstractmethod
    def load_camera_list(self) -> list[str]: ...

    @abstractmethod
    def load_camera_size_list(self) -> list[str]: ...

    @abstractmethod
    def connect_camera(self) -> None: ...

    # FIXME: 必要か検証する
    @abstractmethod
    def apply_camera_name(self) -> None: ...

    # FIXME: 必要か検証する
    @abstractmethod
    def apply_camera_fps(self) -> None: ...

    # FIXME: 必要か検証する
    @abstractmethod
    def apply_camera_size(self) -> None: ...

    # FIXME: 必要か検証する(多分いらない)
    @abstractmethod
    def apply_camera_show_realtime(self) -> None: ...

    @abstractmethod
    def apply_camera_show_matched(self) -> None: ...

    @abstractmethod
    def apply_camera_show_guide(self) -> None: ...

    @abstractmethod
    def save_screencapture(self) -> None: ...

    @abstractmethod
    def open_screencapture_directory_window(self) -> None: ...

    # Serial Functionalities
    @abstractmethod
    def load_serial_port_list(self) -> list[str]: ...

    @abstractmethod
    def load_serial_baud_rate_list(self) -> list[int]: ...

    @abstractmethod
    def load_serial_data_format_list(self) -> list[str]: ...

    @abstractmethod
    def connect_serial_port(self) -> None: ...

    @abstractmethod
    def disconnect_serial_port(self) -> None: ...

    # Controller Functionalities
    @abstractmethod
    def push_controller_button(self, button: str) -> None: ...

    @abstractmethod
    def release_controller_button(self, button: str) -> None: ...

    @abstractmethod
    def apply_controller_data_format(self) -> None: ...

    @abstractmethod
    def open_software_controller_window(self) -> None: ...

    @abstractmethod
    def apply_enabled_keyboard(self) -> None: ...

    @abstractmethod
    def apply_enabled_lstick_mouse(self) -> None: ...

    @abstractmethod
    def apply_enabled_rstick_mouse(self) -> None: ...

    @abstractmethod
    def apply_enabled_pro_controller(self) -> None: ...

    @abstractmethod
    def apply_enabled_record_pro_controller(self) -> None: ...

    # Logging Functionalities
    @abstractmethod
    def clear_log_outputs(self) -> None: ...

    @abstractmethod
    def clear_log_output(self, output_id: int) -> None: ...

    @abstractmethod
    def apply_change_log_stdout(self) -> None: ...

    @abstractmethod
    def adjust_log_outputs_size(self) -> None: ...

    # Notification Functionalities
    @abstractmethod
    def notify_windows(self) -> None: ...

    @abstractmethod
    def notify_discord(self) -> None: ...

    @abstractmethod
    def notify_windows_force(self) -> None: ...

    @abstractmethod
    def notify_discord_force(self) -> None: ...

    @abstractmethod
    def apply_enabled_notify_windows_when_command_started(self) -> None: ...

    @abstractmethod
    def apply_enabled_notify_windows_when_command_ended(self) -> None: ...

    @abstractmethod
    def apply_enabled_notify_discord_when_command_started(self) -> None: ...

    @abstractmethod
    def apply_enabled_notify_discord_when_command_ended(self) -> None: ...

    # Widget Layout Functionalities
    @abstractmethod
    def apply_widget_layout(self) -> None: ...

    @abstractmethod
    def apply_outputs_visibility(self) -> None: ...

    @abstractmethod
    def apply_software_controller_visibility(self) -> None: ...

    @abstractmethod
    def apply_software_controller_position(self) -> None: ...

    @abstractmethod
    def apply_confirm_buttons_position(self) -> None: ...
