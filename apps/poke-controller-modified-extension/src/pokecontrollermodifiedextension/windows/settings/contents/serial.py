import logging
import tkinter as tk
from typing import Any

from .... import widgets
from ....widgets.app import AppFrame
from .dynamic_input import DynamicInputsBuilder

logger = logging.getLogger(__name__)


class SerialSettingsPane(AppFrame):
    _port_combobox: widgets.Combobox

    def __init__(self, master: tk.Misc, *args: Any, **kwargs: Any) -> None:
        super().__init__(master, *args, **kwargs)

        self._serial_ports = self.app.app_model.load_serial_ports()

        self._port = self.app.settings.serial.port
        self._port_name = self.app.settings.serial.port_name
        self._baud_rate = self.app.settings.serial.baud_rate
        self._data_format = self.app.settings.serial.data_format
        self._show_data = self.app.settings.serial.show_data

        self.build_ui()

    def build_ui(self) -> None:
        frame = widgets.Frame(self)

        # port
        port_frame = widgets.Frame(frame, padding=(5, 5))
        port_label = widgets.Label(port_frame, width=16, text="Port:")
        self._port_combobox = widgets.Combobox(
            port_frame,
            textvariable=self._port,
            values=[s.path for s in self._serial_ports],
        )
        port_reload_button = widgets.Button(
            port_frame, text="Reload", command=self._on_port_reload_pushed
        )
        port_label.pack(expand=False, side=tk.LEFT, fill=tk.NONE)
        self._port_combobox.pack(expand=False, side=tk.LEFT, fill=tk.NONE)
        port_reload_button.pack(expand=False, side=tk.LEFT, fill=tk.NONE)
        port_frame.pack(expand=False, side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)

        dynamic_inputs = (
            DynamicInputsBuilder(frame, label_width=16)
            .add_label_row("Port Name:", self._port_name)
            .add_combobox_row(
                "Baud Rate:",
                self._baud_rate,
                values=[
                    str(i) for i in self.app.app_model.load_serial_baud_rate_list()
                ],
            )
            .add_combobox_row(
                "Data Format:",
                self._data_format,
                values=self.app.app_model.load_serial_data_format_list(),
            )
            .add_checkbutton_row("Show Data:", "", self._show_data)
            .build()
        )

        # Layout
        port_label.pack(side=tk.LEFT)
        self._port_combobox.pack(side=tk.LEFT)
        port_reload_button.pack(side=tk.LEFT)

        dynamic_inputs.pack(expand=True, fill=tk.BOTH)
        frame.pack(expand=True, fill=tk.BOTH, anchor=tk.CENTER)

    def _on_port_reload_pushed(self) -> None:
        serial_ports = [s.path for s in self.app.app_model.load_serial_ports()]
        self._port_combobox.configure(values=serial_ports)
