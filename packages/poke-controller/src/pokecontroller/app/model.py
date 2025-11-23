from abc import ABC

from .state import PokeControllerAppState


class PokeControllerAppModel(ABC):
    def __init__(self, state: PokeControllerAppState):
        self._state = state

    @property
    def state(self) -> PokeControllerAppState:
        return self._state

    def start_command(self):
        pass

    def open_controller_window(self):
        pass

    def clear_outputs(self):
        pass

    def save_screen_capture(self):
        pass

    def open_capture_directory(self):
        pass

    def notify_discord(self):
        pass

    def load_camera_list(self) -> list[str]:
        return ["Camera 1", "Camera 2", "Camera 3"]

    def load_camera_size_list(self) -> list[str]:
        return [f"{320 * i}x{180 * i}" for i in range(1, 7)]

    def set_camera_name(self):
        pass

    def set_camera_fps(self):
        pass

    def set_camera_size(self):
        pass

    def load_camera(self):
        pass

    def set_show_realtime(self):
        pass

    def set_show_value(self):
        pass

    def set_show_guide(self):
        pass

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

    def set_serial_data_format(self):
        pass

    def open_software_controller_window(self):
        pass

    def set_enable_keyboard(self):
        pass

    def set_enable_lstick_mouse(self):
        pass

    def set_enable_rstick_mouse(self):
        pass

    def set_enable_pro_controller(self):
        pass

    def set_enable_record_pro_controller(self):
        pass

    def load_python_command_list(self) -> list[str]:
        return ["Command 1", "Command 2", "Command 3"]

    def load_python_commands_filter_list(self) -> list[str]:
        return ["-"]

    def load_mcu_command_list(self) -> list[str]:
        return ["Command 1", "Command 2", "Command 3"]

    def load_mcu_commands_filter_list(self) -> list[str]:
        return ["-"]

    def set_shortcut_number(self):
        pass

    def set_command_to_shortcut(self):
        pass

    def load_commands(self):
        pass

    def start_command(self):
        pass

    def pause_command(self):
        pass

    def set_python_commands_filter(self):
        pass

    def set_python_command(self):
        pass

    def set_mcu_commands_filter(self):
        pass

    def set_mcu_command(self):
        pass

    def start_shortcut_command(self, id: int):
        pass

    def open_commands_directory(self):
        pass

    def set_enabled_notify_windows_start(self):
        pass

    def set_enabled_notify_windows_end(self):
        pass

    def test_windows_notification(self):
        pass

    def set_enabled_notify_discord_start(self):
        pass

    def set_enabled_notify_discord_end(self):
        pass

    def test_discord_notification(self):
        pass

    def set_outputs_size(self, value: float):
        pass

    def set_output_destination(self):
        pass

    def clear_output(self, id: int):
        pass

    def set_visibled_output1(self):
        pass

    def set_visibled_output2(self):
        pass

    def set_visibled_software_controller(self):
        pass

    def set_software_controller_position(self):
        pass

    def set_confirm_buttons_position(self):
        pass

    def push_button(self, button: str):
        print(button)

    def release_button(self, button: str):
        print(button)
