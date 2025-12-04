import platform
import tkinter as tk
import tkinter.ttk as ttk
from typing import Any

from ....model import AppModel
from ....state import AppGuiState
from ....values import literals as l
from ....widgets import AppFrame


class SerialSettings(AppFrame):
    def __init__(self, master: tk.Misc, *args: Any, **kwargs: Any) -> None:
        super().__init__(master, *args, **kwargs)

        self._port_list: list[str] = self._load_serial_port_list()
        self._baud_rate_list: list[int] = self._load_serial_baud_rate_list()
        self._data_format_list: list[str] = self._load_serial_data_format_list()

        self._port = self.app_state.serial.port
        self._baud_rate = self.app_state.serial.baud_rate
        self._data_format = self.app_state.serial.data_format
        self._show_data = self.app_state.serial.show_data

        self.build_ui()

    @property
    def app_state(self) -> AppGuiState:
        return self.app.app_state

    @property
    def app_model(self) -> AppModel:
        return self.app.app_model

    def build_ui(self) -> None:
        # Create Labelframes
        serial_settings = self._build_serial_settings()
        data_settings = self._build_data_settings()

        # Layout
        serial_settings.pack(expand=False, fill=l.X, anchor=l.N, pady=4)
        data_settings.pack(expand=False, fill=l.X, anchor=l.N, pady=4)

    def _build_serial_settings(self) -> ttk.Labelframe:
        labelframe = ttk.Labelframe(self, text="Port Settings")

        # Port
        port_label = ttk.Label(
            labelframe,
            text="COM Port: " if platform.system() == "Windows" else "Port: ",
        )
        port_entry = ttk.Combobox(
            labelframe,
            width=5,
            state=l.READONLY,
            textvariable=self._port,
            values=self._port_list,
        )
        port_entry.current(0)

        # Baud Rate
        baud_rate_label = ttk.Label(labelframe, text="Baud Rate: ")
        baud_rate_combobox = ttk.Combobox(
            labelframe,
            width=6,
            justify=l.RIGHT,
            state=l.READONLY,
            textvariable=self._baud_rate,
            values=[str(i) for i in self._baud_rate_list],
        )

        # Reconnect Button
        reconnect_button = ttk.Button(
            labelframe,
            text="Reconnect",
            command=self._on_reconnect_pushed,
        )

        # Disconnect Button
        disconnect_button = ttk.Button(
            labelframe,
            text="Disconnect",
            command=self._on_disconnect_pushed,
        )

        # Layout
        port_label.pack(expand=False, side=l.LEFT, padx=4)
        port_entry.pack(expand=True, fill=l.X, side=l.LEFT)
        ttk.Separator(master=labelframe, orient=l.VERTICAL).pack(
            expand=False, fill=l.Y, side=l.LEFT, padx=5, pady=8
        )
        baud_rate_label.pack(expand=False, side=l.LEFT)
        baud_rate_combobox.pack(expand=False, fill=l.X, side=l.LEFT)
        ttk.Separator(master=labelframe, orient=l.VERTICAL).pack(
            expand=False, fill=l.Y, side=l.LEFT, padx=5, pady=8
        )
        reconnect_button.pack(expand=False, fill=l.X, side=l.LEFT, padx=4, pady=4)
        disconnect_button.pack(expand=False, fill=l.X, side=l.LEFT, padx=4, pady=4)

        return labelframe

    def _build_data_settings(self) -> ttk.Labelframe:
        labelframe = ttk.Labelframe(self, text="Data")

        # Data Format
        data_format_label = ttk.Label(labelframe, text="Data Format: ", anchor=l.CENTER)
        data_format_combobox = ttk.Combobox(
            labelframe,
            state=l.NORMAL,
            textvariable=self._data_format,
            values=self._data_format_list,
        )
        data_format_combobox.bind(
            "<<ComboboxSelected>>",
            self._on_data_format_selected,
            add="",
        )

        # Show Serial
        show_serial_checkbutton = ttk.Checkbutton(
            labelframe,
            text="Show Serial",
            variable=self._show_data,
        )

        # Layout
        data_format_label.pack(expand=False, side=l.LEFT, padx=4, pady=(0, 4))
        data_format_combobox.pack(expand=False, side=l.LEFT, padx=4, pady=(0, 4))
        show_serial_checkbutton.pack(expand=False, side=l.LEFT, padx=4, pady=(0, 4))

        return labelframe

    def _load_serial_port_list(self) -> list[str]:
        return self.app_model.load_serial_port_list()

    def _load_serial_baud_rate_list(self) -> list[int]:
        return self.app_model.load_serial_baud_rate_list()

    def _load_serial_data_format_list(self) -> list[str]:
        return self.app_model.load_serial_data_format_list()

    def _on_reconnect_pushed(self) -> None:
        self.app_model.connect_serial_port()

    def _on_disconnect_pushed(self) -> None:
        self.app_model.disconnect_serial_port()

    def _on_data_format_selected(self, _event: tk.Event) -> None:
        self.app_model.apply_controller_data_format()
