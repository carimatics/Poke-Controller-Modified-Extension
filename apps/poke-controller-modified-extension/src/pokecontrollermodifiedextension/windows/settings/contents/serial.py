import logging
import tkinter as tk
from typing import Any

from .... import widgets
from ....widgets.app import AppFrame
from ....widgets.components import ComponentPackBuilder

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
        label_width = 16
        frame = (
            ComponentPackBuilder(self)
            .add_frame_row()
            .add_label(text="Port:", width=label_width)
            .add_combobox(
                variable=self._port, values=[s.path for s in self._serial_ports]
            )
            .add_button(text="Reload", command=self._on_port_reload_pushed)
            .end()
            .add_frame_row()
            .add_label(text="Port Name:", width=label_width)
            .add_label(variable=self._port_name)
            .end()
            .add_frame_row()
            .add_label(text="Baud Rate:", width=label_width)
            .add_combobox(
                variable=self._baud_rate,
                values=[
                    str(i) for i in self.app.app_model.load_serial_baud_rate_list()
                ],
            )
            .end()
            .add_frame_row()
            .add_label(text="Data Format:", width=label_width)
            .add_combobox(
                variable=self._data_format,
                values=self.app.app_model.load_serial_data_format_list(),
            )
            .end()
            .add_frame_row()
            .add_label(text="Show Data:", width=label_width)
            .add_checkbutton(self._show_data, "")
            .end()
            .build()
        )

        frame.pack(expand=False, fill=tk.BOTH, anchor=tk.CENTER)

    def _on_port_reload_pushed(self) -> None:
        serial_ports = [s.path for s in self.app.app_model.load_serial_ports()]
        self._port_combobox.configure(values=serial_ports)
