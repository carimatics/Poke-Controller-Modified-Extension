import tkinter as tk
import tkinter.ttk as ttk


class ManualControlSettings(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.build_ui()

    def build_ui(self):
        # Create Labelframes
        software_settings = self.build_software_settings()
        hardware_settings = self.build_hardware_settings()

        # Layout
        software_settings.pack(expand=False, fill=tk.X, anchor=tk.N, pady=4)
        hardware_settings.pack(expand=False, fill=tk.X, anchor=tk.N, pady=4)

    def build_software_settings(self) -> ttk.Labelframe:
        labelframe = ttk.Labelframe(self, text="Software")

        upper_frame = ttk.Frame(labelframe)
        lower_frame = ttk.Frame(labelframe)

        # Controller Button
        controller_button = ttk.Button(upper_frame,
                                       width=15,
                                       text="Controller",
                                       command=self.open_software_controller_window)

        # Use Keyboard

        is_use_keyboard = tk.BooleanVar()
        use_keyboard_checkbutton = ttk.Checkbutton(lower_frame,
                                                   text="Use Keyboard",
                                                   variable=is_use_keyboard,
                                                   command=self.set_is_use_keyboard)

        # Use LStick Mouse
        is_use_lstick_mouse = tk.BooleanVar()
        use_lstick_mouse_checkbutton = ttk.Checkbutton(lower_frame,
                                                       text="Use LStick Mouse",
                                                       variable=is_use_lstick_mouse,
                                                       command=self.set_is_use_lstick_mouse)

        # Use RStick Mouse
        is_use_rstick_mouse = tk.BooleanVar()
        use_rstick_mouse_checkbutton = ttk.Checkbutton(lower_frame,
                                                       text="Use RStick Mouse",
                                                       variable=is_use_rstick_mouse,
                                                       command=self.set_is_use_rstick_mouse)

        # Layout
        controller_button.pack(expand=False, fill=tk.NONE, side=tk.LEFT, padx=4, pady=4)
        use_keyboard_checkbutton.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4)
        use_lstick_mouse_checkbutton.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=8)
        use_rstick_mouse_checkbutton.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4)
        upper_frame.pack(expand=False, fill=tk.X, anchor=tk.N)
        lower_frame.pack(expand=False, fill=tk.X, anchor=tk.N, pady=4)

        return labelframe

    def build_hardware_settings(self) -> ttk.Labelframe:
        labelframe = ttk.Labelframe(self, text="Hardware")

        # Use Pro Controller
        is_use_pro_controller = tk.BooleanVar()
        use_pro_controller_checkbutton = ttk.Checkbutton(labelframe,
                                                         text="Use Pro Controller",
                                                         variable=is_use_pro_controller,
                                                         command=self.set_is_use_pro_controller)

        # Record Pro Controller
        is_record_pro_controller = tk.BooleanVar()
        record_pro_controller_checkbutton = ttk.Checkbutton(labelframe,
                                                            text="Record Pro Controller",
                                                            variable=is_record_pro_controller,
                                                            command=self.set_is_record_pro_controller)

        # Layout
        use_pro_controller_checkbutton.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4, pady=4)
        record_pro_controller_checkbutton.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=8, pady=4)

        return labelframe

    def open_software_controller_window(self):
        pass

    def set_is_use_keyboard(self):
        pass

    def set_is_use_lstick_mouse(self):
        pass

    def set_is_use_rstick_mouse(self):
        pass

    def set_is_use_pro_controller(self):
        pass

    def set_is_record_pro_controller(self):
        pass
