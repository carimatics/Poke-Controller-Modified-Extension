import tkinter as tk
import tkinter.ttk as ttk

from ....components import AppFrame


class OthersSettings(AppFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.output_size = self.app_state.other_output_size
        self.output_standard = self.app_state.other_output_standard
        self.visibled_output1 = self.app_state.other_widget_visibled_output1
        self.visibled_output2 = self.app_state.other_widget_visibled_output2
        self.visibled_software_controller = self.app_state.other_widget_visibled_software_controller
        self.software_controller_position = self.app_state.other_software_controller_position
        self.confirm_dialogue_buttons_position = self.app_state.other_dialogue_confirm_buttons_position

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
        size_scale = ttk.Scale(labelframe,
                               length=200,
                               orient=tk.HORIZONTAL,
                               from_=0,
                               to=100,
                               variable=self.output_size,
                               command=self.app_model.set_outputs_size)

        # Layout
        size_scale.pack(expand=True, fill=tk.X, side=tk.LEFT, anchor=tk.CENTER, padx=4, pady=(5, 12))

        return labelframe

    def build_standard_output_destination_settings(self, master) -> ttk.Labelframe:
        labelframe = ttk.Labelframe(master, text="Standard Output")

        # Destination
        destination_radiobuttons = [
            ttk.Radiobutton(labelframe,
                            text="Output#1",
                            value=1,
                            variable=self.output_standard,
                            command=self.app_model.set_output_destination),
            ttk.Radiobutton(labelframe,
                            text="Output#2",
                            value=2,
                            variable=self.output_standard,
                            command=self.app_model.set_output_destination),
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
                       command=lambda: self.app_model.clear_output(id=1)),
            ttk.Button(labelframe,
                       text="Clear(#2)",
                       command=lambda: self.app_model.clear_output(id=2)),
        ]

        # Layout
        for button in buttons:
            button.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4, pady=(3, 5))

        return labelframe

    def build_widget_mode(self, master) -> ttk.Labelframe:
        labelframe = ttk.Labelframe(master, text="Display")

        # Widget Mode Checkbuttons
        checkbuttons = [
            ttk.Checkbutton(labelframe,
                            text="Output#1",
                            variable=self.visibled_output1,
                            command=self.app_model.set_visibled_output1),
            ttk.Checkbutton(labelframe,
                            text="Output#2",
                            variable=self.visibled_output2,
                            command=self.app_model.set_visibled_output2),
            ttk.Checkbutton(labelframe,
                            text="Software-Controller",
                            variable=self.visibled_software_controller,
                            command=self.app_model.set_visibled_software_controller),
        ]

        # Layout
        for checkbutton in checkbuttons:
            checkbutton.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4, pady=4)

        return labelframe

    def build_software_controller_position_settings(self, master) -> ttk.Labelframe:
        labelframe = ttk.Labelframe(master, text="Software-Controller Position")

        # Position
        position_radiobuttons = [
            ttk.Radiobutton(labelframe,
                            text="Top",
                            value="top",
                            variable=self.software_controller_position,
                            command=self.app_model.set_software_controller_position),
            ttk.Radiobutton(labelframe,
                            text="Bottom",
                            value="bottom",
                            variable=self.software_controller_position,
                            command=self.app_model.set_software_controller_position),
        ]

        # Layout
        for radiobutton in position_radiobuttons:
            radiobutton.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4, pady=4)

        return labelframe

    def build_dialogue_confirm_buttons_position_settings(self, master) -> ttk.Labelframe:
        labelframe = ttk.Labelframe(master, text="Dialogue OK/Cancel Position")

        # Position
        position_radiobuttons = [
            ttk.Radiobutton(labelframe,
                            text="Top",
                            value="top",
                            variable=self.confirm_dialogue_buttons_position,
                            command=self.app_model.set_confirm_buttons_position),
            ttk.Radiobutton(labelframe,
                            text="Bottom",
                            value="bottom",
                            variable=self.confirm_dialogue_buttons_position,
                            command=self.app_model.set_confirm_buttons_position),
            ttk.Radiobutton(labelframe,
                            text="Both",
                            value="both",
                            variable=self.confirm_dialogue_buttons_position,
                            command=self.app_model.set_confirm_buttons_position),
        ]

        # Layout
        for radiobutton in position_radiobuttons:
            radiobutton.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4, pady=4)

        return labelframe
