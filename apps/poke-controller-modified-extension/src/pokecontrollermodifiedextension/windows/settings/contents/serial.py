import logging
import tkinter as tk
import tkinter.ttk as ttk
from typing import Any

from ....widgets import AppFrame

logger = logging.getLogger(__name__)


class SerialSettingsPane(AppFrame):
    _port_combobox: ttk.Combobox

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
        frame = ttk.Frame(self)

        # port
        port_frame = ttk.Frame(frame)
        port_label = ttk.Label(port_frame, width=16, text="Port:")
        self._port_combobox = ttk.Combobox(
            port_frame,
            textvariable=self._port,
            values=[s.path for s in self._serial_ports],
        )
        port_reload_button = ttk.Button(
            port_frame, text="Reload", command=self._on_port_reload_pushed
        )

        # port_name
        port_name_frame = ttk.Frame(frame)
        port_name_label = ttk.Label(port_name_frame, width=16, text="Port Name:")
        port_name_value = ttk.Label(port_name_frame, textvariable=self._port_name)

        # baud_rate
        baud_rate_frame = ttk.Frame(frame)
        baud_rate_label = ttk.Label(baud_rate_frame, width=16, text="Baud Rate:")
        baud_rate_combobox = ttk.Combobox(
            baud_rate_frame,
            textvariable=self._baud_rate,
            values=[str(i) for i in self.app.app_model.load_serial_baud_rate_list()],
        )

        # data_format
        data_format_frame = ttk.Frame(frame)
        data_format_label = ttk.Label(data_format_frame, width=16, text="Data Format:")
        data_format_combobox = ttk.Combobox(
            data_format_frame,
            textvariable=self._data_format,
            values=self.app.app_model.load_serial_data_format_list(),
        )

        # show_data
        show_data_frame = ttk.Frame(frame)
        show_data_label = ttk.Label(show_data_frame, width=16, text="Show Data:")
        show_data_combobox = ttk.Checkbutton(
            show_data_frame,
            variable=self._show_data,
        )

        # Layout
        port_label.pack(side=tk.LEFT)
        self._port_combobox.pack(side=tk.LEFT, padx=4)
        port_reload_button.pack(side=tk.LEFT, padx=4)
        port_frame.pack(expand=False, fill=tk.X)

        port_name_label.pack(side=tk.LEFT)
        port_name_value.pack(side=tk.LEFT, padx=4)
        port_name_frame.pack(expand=False, fill=tk.X)

        baud_rate_label.pack(side=tk.LEFT)
        baud_rate_combobox.pack(side=tk.LEFT, padx=4)
        baud_rate_frame.pack(expand=False, fill=tk.X)

        data_format_label.pack(side=tk.LEFT)
        data_format_combobox.pack(side=tk.LEFT, padx=4)
        data_format_frame.pack(expand=False, fill=tk.X)

        show_data_label.pack(side=tk.LEFT)
        show_data_combobox.pack(side=tk.LEFT, padx=4)
        show_data_frame.pack(expand=False, fill=tk.X)

        frame.pack(expand=True, fill=tk.BOTH, anchor=tk.CENTER)

    def _on_port_reload_pushed(self) -> None:
        serial_ports = [s.path for s in self.app.app_model.load_serial_ports()]
        self._port_combobox.configure(values=serial_ports)
