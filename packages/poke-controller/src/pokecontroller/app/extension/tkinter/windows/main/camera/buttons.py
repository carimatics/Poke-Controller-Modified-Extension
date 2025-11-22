import tkinter as tk
import tkinter.ttk as ttk

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


class Buttons(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._open_dir_button_image: tk.PhotoImage = tk.PhotoImage(file="../assets/icons8-OpenDir-16.png")
        self.build_ui()

    def build_ui(self):
        # Create Buttons
        buttons: dict[str, ttk.Button] = {}
        buttons[START] = ttk.Button(self,
                                    text="Start",
                                    command=self.start_command)
        buttons[CONTROLLER] = ttk.Button(self,
                                         text="Controller",
                                         command=self.open_controller_window)
        buttons[CLEAR_OUTPUTS] = ttk.Button(self,
                                            text="Clear Outputs",
                                            command=self.clear_outputs)
        buttons[CAPTURE] = ttk.Button(self,
                                      text="Capture",
                                      command=self.save_screen_capture)
        buttons[OPEN_CAPTURE_DIR] = ttk.Button(self,
                                               padding=1,
                                               image=self._open_dir_button_image,
                                               command=self.open_capture_directory)
        buttons[NOTIFY_DISCORD] = ttk.Button(self,
                                             text="Discord",
                                             command=self.notify_discord)

        # Layout
        for button in BUTTONS:
            buttons[button].pack(expand=True, anchor=tk.CENTER, side=tk.LEFT, padx=4)

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
