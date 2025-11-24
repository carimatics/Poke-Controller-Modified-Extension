import platform
import tkinter as tk
import tkinter.ttk as ttk

from ....components import AppFrame
from ....utils import (
    separator,
)


class SerialSettings(AppFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.port_list: list[str] = self.app_model.load_serial_port_list()
        self.baud_rate_list: list[int] = self.app_model.load_serial_baud_rate_list()
        self.data_format_list: list[str] = self.app_model.load_serial_data_format_list()
        self.port: tk.StringVar = self.app_state.serial_port
        self.baud_rate: tk.IntVar = self.app_state.serial_baud_rate
        self.data_format: tk.StringVar = self.app_state.serial_data_format
        self.show_data: tk.BooleanVar = self.app_state.serial_show_data

        self.build_ui()

    def build_ui(self):
        # Create Labelframes
        serial_settings = self.build_serial_settings()
        data_settings = self.build_data_settings()

        # Layout
        serial_settings.pack(expand=False, fill=tk.X, anchor=tk.N, pady=4)
        data_settings.pack(expand=False, fill=tk.X, anchor=tk.N, pady=4)

    def build_serial_settings(self) -> ttk.Labelframe:
        labelframe = ttk.Labelframe(self, text="Port Settings")

        # Port
        port_label = ttk.Label(labelframe,
                               text="COM Port: " if platform.system() == "Windows" else "Port: ")
        port_entry = ttk.Combobox(labelframe,
                                  width=5,
                                  state="readonly",
                                  textvariable=self.port,
                                  values=self.port_list)

        # Baud Rate
        baud_rate_label = ttk.Label(labelframe, text="Baud Rate: ")
        baud_rate_combobox = ttk.Combobox(labelframe,
                                          width=6,
                                          justify=tk.RIGHT,
                                          state="readonly",
                                          textvariable=self.baud_rate,
                                          values=[str(i) for i in self.baud_rate_list])

        # Reconnect Button
        reconnect_button = ttk.Button(labelframe,
                                      text="Reconnect",
                                      command=self.app_model.connect_serial_port)

        # Disconnect Button
        disconnect_button = ttk.Button(labelframe,
                                       text="Disconnect",
                                       command=self.app_model.disconnect_serial_port)

        # Layout
        port_label.pack(expand=False, side=tk.LEFT, padx=4)
        port_entry.pack(expand=True, fill=tk.X, side=tk.LEFT)
        separator(labelframe).pack(expand=False, fill=tk.Y, side=tk.LEFT, padx=5, pady=8)
        baud_rate_label.pack(expand=False, side=tk.LEFT)
        baud_rate_combobox.pack(expand=False, fill=tk.X, side=tk.LEFT)
        separator(labelframe).pack(expand=False, fill=tk.Y, side=tk.LEFT, padx=5, pady=8)
        reconnect_button.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4, pady=4)
        disconnect_button.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4, pady=4)

        return labelframe

    def build_data_settings(self) -> ttk.Labelframe:
        labelframe = ttk.Labelframe(self, text="Data")

        # Data Format
        data_format_label = ttk.Label(labelframe,
                                      text="Data Format: ",
                                      anchor=tk.CENTER)
        data_format_combobox = ttk.Combobox(labelframe,
                                            state=tk.NORMAL,
                                            textvariable=self.data_format,
                                            values=self.data_format_list)
        data_format_combobox.bind("<<ComboboxSelected>>", self.app_model.apply_controller_data_format)

        # Show Serial
        show_serial_checkbutton = ttk.Checkbutton(labelframe,
                                                  text="Show Serial",
                                                  variable=self.show_data)

        # Layout
        data_format_label.pack(expand=False, side=tk.LEFT, padx=4, pady=(0, 4))
        data_format_combobox.pack(expand=False, side=tk.LEFT, padx=4, pady=(0, 4))
        show_serial_checkbutton.pack(expand=False, side=tk.LEFT, padx=4, pady=(0, 4))

        return labelframe
