import platform
import tkinter as tk
import tkinter.ttk as ttk

from ....utils import (
    separator,
)


class SerialSettings(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
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
        port = tk.StringVar()
        port_label = ttk.Label(labelframe,
                               text="COM Port: " if platform.system() == "Windows" else "Port: ")
        port_entry = ttk.Entry(labelframe,
                               width=5,
                               state="readonly",
                               textvariable=port)

        # Baud Rate
        baud_rate_list = [
            4800,
            9600,
            115200,
        ]
        baud_rate = tk.StringVar(value=str(baud_rate_list[1]))
        baud_rate_label = ttk.Label(labelframe, text="Baud Rate: ")
        baud_rate_combobox = ttk.Combobox(labelframe,
                                          width=6,
                                          justify=tk.RIGHT,
                                          state="readonly",
                                          textvariable=baud_rate,
                                          values=[str(i) for i in baud_rate_list])

        # Reconnect Button
        reconnect_button = ttk.Button(labelframe,
                                      text="Reconnect",
                                      command=self.reconnect_port)

        # Disconnect Button
        disconnect_button = ttk.Button(labelframe,
                                       text="Disconnect",
                                       command=self.disconnect_port)

        # Layout
        port_label.pack(expand=False, side=tk.LEFT, padx=4)
        port_entry.pack(expand=True, fill=tk.X, side=tk.LEFT)
        separator(labelframe).pack(expand=False, fill=tk.Y, side=tk.LEFT, padx=5, pady=8)
        baud_rate_label.pack(expand=False, side=tk.LEFT)
        baud_rate_combobox.pack(expand=False, fill=tk.X, side=tk.LEFT)
        separator(labelframe).pack(expand=False, fill=tk.Y, side=tk.LEFT, padx=5, pady=8)
        reconnect_button.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4)
        disconnect_button.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4)

        return labelframe

    def build_data_settings(self) -> ttk.Labelframe:
        labelframe = ttk.Labelframe(self, text="Data")

        # Data Format
        data_format_list = [
            "Default",
            "Qingpi",
            "3DS Controller",
        ]
        data_format = tk.StringVar(value=data_format_list[0])
        data_format_label = ttk.Label(labelframe,
                                      text="Data Format: ",
                                      anchor=tk.CENTER)
        data_format_combobox = ttk.Combobox(labelframe,
                                            state=tk.NORMAL,
                                            textvariable=data_format,
                                            values=data_format_list)
        data_format_combobox.bind("<<ComboboxSelected>>", self.set_data_format)

        # Show Serial
        is_show_serial = tk.BooleanVar(value=False)
        show_serial_checkbutton = ttk.Checkbutton(labelframe,
                                                  text="Show Serial",
                                                  variable=is_show_serial)

        # Layout
        data_format_label.pack(expand=False, side=tk.LEFT, padx=4)
        data_format_combobox.pack(expand=False, side=tk.LEFT, padx=4)
        show_serial_checkbutton.pack(expand=False, side=tk.LEFT, padx=4)

        return labelframe

    def reconnect_port(self) -> None:
        pass

    def disconnect_port(self) -> None:
        pass

    def set_data_format(self, event) -> None:
        pass
