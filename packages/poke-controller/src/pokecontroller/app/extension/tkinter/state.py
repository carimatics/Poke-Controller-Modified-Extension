import tkinter as tk
from ...state import PokeControllerAppState


def load_state() -> PokeControllerAppState:
    return PokeControllerAppState(
        theme=tk.StringVar(value="default"),

        # Camera Settings
        camera_id = tk.StringVar(value=""),
        camera_name = tk.StringVar(value=""),
        camera_fps = tk.IntVar(value=45),
        camera_size = tk.StringVar(value="640x360"),
        camera_show_realtime = tk.BooleanVar(value=True),
        camera_show_value = tk.BooleanVar(value=False),
        camera_show_guide = tk.BooleanVar(value=False),

        # Serial Settings
        serial_port = tk.StringVar(value="COM 1"),
        serial_baud_rate = tk.IntVar(value=9600),
        serial_data_format = tk.StringVar(value="Default"),
        serial_show_data = tk.BooleanVar(value=False),

        # Manual Control Settings
        manual_control_enabled_keyboard = tk.BooleanVar(value=False),
        manual_control_enabled_lstick_mouse = tk.BooleanVar(value=False),
        manual_control_enabled_rstick_mouse = tk.BooleanVar(value=False),
        manual_control_enabled_pro_controller = tk.BooleanVar(value=False),
        manual_control_enabled_record_pro_controller = tk.BooleanVar(value=False),

        # Command Settings
        command_python_commands_filter = tk.StringVar(value="-"),
        command_python_command = tk.StringVar(value=""),
        command_mcu_commands_filter = tk.StringVar(value="-"),
        command_mcu_command = tk.StringVar(value=""),
        command_shortcut_number = tk.IntVar(value=1),
        command_shortcuts = [
            tk.StringVar(value=None),
            tk.StringVar(value=None),
            tk.StringVar(value=None),
            tk.StringVar(value=None),
            tk.StringVar(value=None),
            tk.StringVar(value=None),
            tk.StringVar(value=None),
            tk.StringVar(value=None),
            tk.StringVar(value=None),
            tk.StringVar(value=None),
        ],

        # Notification Settings
        notification_enabled_windows_start = tk.BooleanVar(value=False),
        notification_enabled_windows_end = tk.BooleanVar(value=False),
        notification_enabled_discord_start = tk.BooleanVar(value=False),
        notification_enabled_discord_end = tk.BooleanVar(value=False),

        # Other Settings
        other_output_size = tk.IntVar(value=50),
        other_output_standard = tk.IntVar(value=1),
        other_widget_visibled_output1 = tk.BooleanVar(value=True),
        other_widget_visibled_output2 = tk.BooleanVar(value=True),
        other_widget_visibled_software_controller = tk.BooleanVar(value=True),
        other_software_controller_position = tk.StringVar(value="bottom"),
        other_dialogue_confirm_buttons_position = tk.StringVar(value="bottom"),
    )
