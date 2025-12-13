import tkinter as tk
import tkinter.ttk as ttk
from typing import Any

from ....model import AppModel
from ....settings import AppSettings
from ....widgets.app import AppFrame


class OthersSettings(AppFrame):
    def __init__(self, master: tk.Misc, *args: Any, **kwargs: Any) -> None:
        super().__init__(master, *args, **kwargs)

        self._output_size = self.settings.widget.output.size_balance
        self._output_stdout = self.settings.widget.output.stdout
        self._output1_visibility = self.settings.widget.output.visible_output1
        self._output2_visibility = self.settings.widget.output.visible_output2
        self._software_controller_visibility = (
            self.settings.widget.software_controller.visible
        )
        self._software_controller_position = (
            self.settings.widget.software_controller.position
        )
        self._confirm_dialogue_buttons_position = (
            self.settings.widget.dialog.confirm_buttons_position
        )

        self.build_ui()

    @property
    def settings(self) -> AppSettings:
        return self.app.settings

    @property
    def app_model(self) -> AppModel:
        return self.app.app_model

    def build_ui(self) -> None:
        upper_frame = ttk.Labelframe(self, text="Output Settings")
        size_adjuster = self._build_size_adjuster(upper_frame)
        standard_output_destination_settings = self._build_stdout_settings(upper_frame)
        clear_outputs = self._build_clear_outputs(upper_frame)

        lower_frame = ttk.Labelframe(self, text="Widget Settings")
        widget_mode = self._build_widget_mode(lower_frame)
        software_controller_position_settings = (
            self._build_software_controller_position_settings(lower_frame)
        )
        dialogue_confirm_buttons_position_settings = (
            self._build_dialogue_confirm_buttons_position_settings(lower_frame)
        )

        # Layout
        size_adjuster.pack(expand=True, fill=tk.X, side=tk.LEFT, padx=4, pady=4)
        standard_output_destination_settings.pack(
            expand=False,
            fill=tk.BOTH,
            side=tk.LEFT,
            padx=7,
            pady=4,
        )
        clear_outputs.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4, pady=4)
        upper_frame.pack(expand=False, fill=tk.X, side=tk.TOP, padx=4, pady=4)

        widget_mode.pack(
            expand=False,
            fill=tk.X,
            side=tk.LEFT,
            anchor=tk.CENTER,
            padx=4,
            pady=4,
        )
        software_controller_position_settings.pack(
            expand=False,
            fill=tk.NONE,
            side=tk.LEFT,
            anchor=tk.CENTER,
            padx=7,
            pady=4,
        )
        dialogue_confirm_buttons_position_settings.pack(
            expand=False,
            fill=tk.X,
            side=tk.LEFT,
            padx=4,
            pady=4,
        )
        lower_frame.pack(expand=False, fill=tk.X, side=tk.TOP, padx=4, pady=4)

    def _build_size_adjuster(self, master: tk.Misc) -> ttk.Labelframe:
        labelframe = ttk.Labelframe(master, text="Size Adjuster")

        # Size
        size_scale = ttk.Scale(
            labelframe,
            length=200,
            orient=tk.HORIZONTAL,
            from_=0,
            to=100,
            variable=self._output_size,
            command=self._on_size_adjuster_changed,
        )

        # Layout
        size_scale.pack(
            expand=True,
            fill=tk.X,
            side=tk.LEFT,
            anchor=tk.CENTER,
            padx=4,
            pady=(5, 12),
        )

        return labelframe

    def _build_stdout_settings(self, master: tk.Misc) -> ttk.Labelframe:
        labelframe = ttk.Labelframe(master, text="Standard Output")

        # Destinations
        stdout_radiobuttons = [
            ttk.Radiobutton(
                labelframe,
                text=f"Output#{i}",
                value=i,
                variable=self._output_stdout,
                command=self._on_stdout_changed,
            )
            for i in range(1, 3)
        ]

        # Layout
        for radiobutton in stdout_radiobuttons:
            radiobutton.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4)

        return labelframe

    def _build_clear_outputs(self, master: tk.Misc) -> ttk.Labelframe:
        labelframe = ttk.Labelframe(master, text="Clear")

        # Outputs Clear Buttons
        buttons = [
            ttk.Button(
                labelframe,
                text=f"Clear(#{i})",
                command=lambda i=i: self._on_clear_pushed(output_id=i),  # type: ignore[misc]
            )
            for i in range(1, 3)
        ]

        # Layout
        for button in buttons:
            button.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4, pady=(3, 5))

        return labelframe

    def _build_widget_mode(self, master: tk.Misc) -> ttk.Labelframe:
        labelframe = ttk.Labelframe(master, text="Display")

        # Widget Mode Checkbuttons
        checkbuttons = [
            ttk.Checkbutton(
                labelframe,
                text=text,
                variable=var,
                command=command,
            )
            for text, var, command in [
                (
                    "Output#1",
                    self._output1_visibility,
                    self._on_output_visibility_changed,
                ),
                (
                    "Output#2",
                    self._output2_visibility,
                    self._on_output_visibility_changed,
                ),
                (
                    "Software-Controller",
                    self._software_controller_visibility,
                    self._on_software_controller_visibility_changed,
                ),
            ]
        ]

        # Layout
        for checkbutton in checkbuttons:
            checkbutton.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4, pady=4)

        return labelframe

    def _build_software_controller_position_settings(
        self,
        master: tk.Misc,
    ) -> ttk.Labelframe:
        labelframe = ttk.Labelframe(master, text="Software-Controller Position")

        # Positions
        position_radiobuttons = [
            ttk.Radiobutton(
                labelframe,
                text=value.capitalize(),
                value=value,
                variable=self._software_controller_position,
                command=self._on_software_controller_position_changed,
            )
            for value in ["top", "bottom"]
        ]

        # Layout
        for radiobutton in position_radiobuttons:
            radiobutton.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4, pady=4)

        return labelframe

    def _build_dialogue_confirm_buttons_position_settings(
        self,
        master: tk.Misc,
    ) -> ttk.Labelframe:
        labelframe = ttk.Labelframe(master, text="Dialogue OK/Cancel Position")

        # Positions
        position_radiobuttons = [
            ttk.Radiobutton(
                labelframe,
                text=value.capitalize(),
                value=value,
                variable=self._confirm_dialogue_buttons_position,
                command=self._on_confirm_buttons_position_changed,
            )
            for value in ["top", "bottom", "both"]
        ]

        # Layout
        for radiobutton in position_radiobuttons:
            radiobutton.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4, pady=4)

        return labelframe

    def _on_size_adjuster_changed(self, _value: str) -> None:
        self.app_model.adjust_log_outputs_size()

    def _on_stdout_changed(self) -> None:
        self.app_model.apply_change_log_stdout()

    def _on_clear_pushed(self, output_id: int) -> None:
        self.app_model.clear_log_output(output_id)

    def _on_output_visibility_changed(self) -> None:
        self.app_model.apply_outputs_visibility()

    def _on_software_controller_visibility_changed(self) -> None:
        self.app_model.apply_software_controller_visibility()

    def _on_software_controller_position_changed(self) -> None:
        self.app_model.apply_software_controller_position()

    def _on_confirm_buttons_position_changed(self) -> None:
        self.app_model.apply_confirm_buttons_position()
