import tkinter as tk
import tkinter.ttk as ttk



class OthersSettings(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.build_ui()

    def build_ui(self):
        upper_frame = ttk.Labelframe(self, text="Output Settings")
        size_adjuster = self.build_size_adjuster(upper_frame)
        standard_output_destination_settings = self.build_standard_output_destination_settings(upper_frame)
        clear_outputs = self.build_clear_outputs(upper_frame)

        lower_frame = ttk.Labelframe(self, text="Widget Settings")
        widget_mode = self.build_widget_mode(lower_frame)
        software_controller_position_settings = self.build_software_controller_position_settings(lower_frame)
        dialogue_confirm_buttons_position_settings = self.build_dialogue_confirm_buttons_position_settings(lower_frame)

        # Layout
        size_adjuster.pack(expand=True, fill=tk.X, side=tk.LEFT, padx=4, pady=4)
        standard_output_destination_settings.pack(expand=False, fill=tk.BOTH, side=tk.LEFT, padx=7, pady=4)
        clear_outputs.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4, pady=4)
        upper_frame.pack(expand=False, fill=tk.X, side=tk.TOP, padx=4, pady=4)

        widget_mode.pack(expand=False, fill=tk.X, side=tk.LEFT, anchor=tk.CENTER, padx=4, pady=4)
        software_controller_position_settings.pack(expand=False, fill=tk.NONE, side=tk.LEFT, anchor=tk.CENTER, padx=7,
                                                   pady=4)
        dialogue_confirm_buttons_position_settings.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4, pady=4)
        lower_frame.pack(expand=False, fill=tk.X, side=tk.TOP, padx=4, pady=4)

    def build_size_adjuster(self, master) -> ttk.Labelframe:
        labelframe = ttk.Labelframe(master, text="Size Adjuster")

        # Size
        size = tk.IntVar(value=50)
        size_scale = ttk.Scale(labelframe,
                               length=200,
                               orient=tk.HORIZONTAL,
                               from_=0,
                               to=100,
                               variable=size,
                               command=self.set_outputs_size)

        # Layout
        size_scale.pack(expand=True, fill=tk.X, side=tk.LEFT, anchor=tk.CENTER, padx=4)

        return labelframe

    def build_standard_output_destination_settings(self, master) -> ttk.Labelframe:
        labelframe = ttk.Labelframe(master, text="Standard Output")

        # Destination
        destination = tk.StringVar(value="1")
        destination_radiobuttons = [
            ttk.Radiobutton(labelframe,
                            text="Output#1",
                            value="1",
                            variable=destination,
                            command=self.set_output_destination),
            ttk.Radiobutton(labelframe,
                            text="Output#2",
                            value="2",
                            variable=destination,
                            command=self.set_output_destination),
        ]

        # Layout
        for radiobutton in destination_radiobuttons:
            radiobutton.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4)

        return labelframe

    def build_clear_outputs(self, master) -> ttk.Labelframe:
        labelframe = ttk.Labelframe(master, text="Clear")

        # Clear Outputs Buttons
        buttons = [
            ttk.Button(labelframe,
                       text="Clear(#1)",
                       command=lambda: self.clear_output(id=1)),
            ttk.Button(labelframe,
                       text="Clear(#2)",
                       command=lambda: self.clear_output(id=2)),
        ]

        # Layout
        for button in buttons:
            button.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4)

        return labelframe

    def build_widget_mode(self, master) -> ttk.Labelframe:
        labelframe = ttk.Labelframe(master, text="Display")

        # Widget Mode Checkbuttons
        variables = [
            tk.BooleanVar(),
            tk.BooleanVar(),
            tk.BooleanVar(),
        ]
        checkbuttons = [
            ttk.Checkbutton(labelframe,
                            text="Output#1",
                            variable=variables[0],
                            command=self.set_widget_mode),
            ttk.Checkbutton(labelframe,
                            text="Output#2",
                            variable=variables[1],
                            command=self.set_widget_mode),
            ttk.Checkbutton(labelframe,
                            text="Software-Controller",
                            variable=variables[2],
                            command=self.set_widget_mode),
        ]

        # Layout
        for checkbutton in checkbuttons:
            checkbutton.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4, pady=4)

        return labelframe

    def build_software_controller_position_settings(self, master) -> ttk.Labelframe:
        labelframe = ttk.Labelframe(master, text="Software-Controller Position")

        # Position
        position = tk.StringVar(value="top")
        position_radiobuttons = [
            ttk.Radiobutton(labelframe,
                            text="Top",
                            value="top",
                            variable=position,
                            command=self.set_software_controller_position),
            ttk.Radiobutton(labelframe,
                            text="Bottom",
                            value="bottom",
                            variable=position,
                            command=self.set_software_controller_position),
        ]

        # Layout
        for radiobutton in position_radiobuttons:
            radiobutton.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4, pady=4)

        return labelframe

    def build_dialogue_confirm_buttons_position_settings(self, master) -> ttk.Labelframe:
        labelframe = ttk.Labelframe(master, text="Dialogue OK/Cancel Position")

        # Position
        position = tk.StringVar(value="top")
        position_radiobuttons = [
            ttk.Radiobutton(labelframe,
                            text="Top",
                            value="top",
                            variable=position,
                            command=self.set_confirm_buttons_position),
            ttk.Radiobutton(labelframe,
                            text="Bottom",
                            value="bottom",
                            variable=position,
                            command=self.set_confirm_buttons_position),
            ttk.Radiobutton(labelframe,
                            text="Both",
                            value="both",
                            variable=position,
                            command=self.set_confirm_buttons_position),
        ]

        # Layout
        for radiobutton in position_radiobuttons:
            radiobutton.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4, pady=4)

        return labelframe

    def set_outputs_size(self, size: int):
        pass

    def set_output_destination(self):
        pass

    def clear_output(self, id: int):
        pass

    def set_widget_mode(self):
        pass

    def set_software_controller_position(self):
        pass

    def set_confirm_buttons_position(self):
        pass
