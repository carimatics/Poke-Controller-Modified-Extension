import tkinter as tk
import tkinter.ttk as ttk

from ....components import AppFrame

START = 'start'
CONTROLLER = 'controller'
CLEAR_OUTPUTS = 'clear_outputs'
CAPTURE = 'capture'
OPEN_CAPTURE_DIR = 'open_capture_dir'
NOTIFY_DISCORD = 'notify_discord'

BUTTONS = [
    START,
    CONTROLLER,
    CLEAR_OUTPUTS,
    CAPTURE,
    OPEN_CAPTURE_DIR,
    NOTIFY_DISCORD,
]


class Buttons(AppFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._open_dir_button_image: tk.PhotoImage = tk.PhotoImage(file="../assets/icons8-OpenDir-16.png")
        self.build_ui()

    def build_ui(self):
        # Create Buttons
        buttons: dict[str, ttk.Button] = {}
        buttons[START] = ttk.Button(self,
                                    text="Start",
                                    command=self.app_model.start_command)
        buttons[CONTROLLER] = ttk.Button(self,
                                         text="Controller",
                                         command=self.app_model.open_controller_window)
        buttons[CLEAR_OUTPUTS] = ttk.Button(self,
                                            text="Clear Outputs",
                                            command=self.app_model.clear_log_outputs)
        buttons[CAPTURE] = ttk.Button(self,
                                      text="Capture",
                                      command=self.app_model.save_screencapture)
        buttons[OPEN_CAPTURE_DIR] = ttk.Button(self,
                                               padding=1,
                                               image=self._open_dir_button_image,
                                               command=self.app_model.open_screencapture_directory_window)
        buttons[NOTIFY_DISCORD] = ttk.Button(self,
                                             text="Discord",
                                             command=self.app_model.notify_discord)

        # Layout
        for button in BUTTONS:
            buttons[button].pack(expand=True, anchor=tk.CENTER, side=tk.LEFT, padx=4)
