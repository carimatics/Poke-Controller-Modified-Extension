from typing import Callable
import tkinter as tk
import tkinter.ttk as ttk

from ....components import AppFrame
from ....utils import (
    separator,
)

PYTHON = 'python'
MCU = 'mcu'
SHORTCUT = 'shortcut'

COMMANDS = [
    (PYTHON, 'Python Commands'),
    (MCU, 'MCU Commands'),
    (SHORTCUT, 'Shortcut'),
]


class CommandsSettings(AppFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self._open_dir_button_image: tk.PhotoImage = tk.PhotoImage(file="../assets/icons8-OpenDir-16.png")
        self.python_commands_filter_list: list[str] = self.app_model.load_python_commands_filter_list()
        self.python_command_list: list[str] = self.app_model.load_python_command_list()
        self.mcu_commands_filter_list: list[str] = self.app_model.load_mcu_commands_filter_list()
        self.mcu_command_list: list[str] = self.app_model.load_mcu_command_list()
        self.shortcut_button_texts: list[tk.StringVar] = []
        self.shortcut_commands: list[Callable[[], None]] = []
        self.shortcut_buttons: list[ttk.Button] = []

        self.python_commands_filter = self.app_state.command_python_commands_filter
        self.python_command = self.app_state.command_python_command
        self.mcu_commands_filter = self.app_state.command_mcu_commands_filter
        self.mcu_command = self.app_state.command_mcu_command
        self.shortcut_number = self.app_state.command_shortcut_number
        self.shortcuts = self.app_state.command_shortcuts

        self.build_ui()

    def build_ui(self):
        upper_frame = ttk.Frame(self)
        lower_frame = ttk.Frame(self)

        # Notebook
        notebook = self.build_commands_notebook(upper_frame)

        # Open Commands Directory
        open_dir_button = ttk.Button(upper_frame,
                                     width=5,
                                     image=self._open_dir_button_image,
                                     command=self.app_model.open_commands_directory)

        # Settings
        shortcut_label = ttk.Label(lower_frame,
                                   text="Shortcut: ")
        shortcut_spinbox = ttk.Spinbox(lower_frame,
                                       width=7,
                                       from_=1,
                                       to=10,
                                       increment=1,
                                       textvariable=self.shortcut_number,
                                       command=self.app_model.set_shortcut_number)
        shortcut_set_button = ttk.Button(lower_frame,
                                         text="Set",
                                         command=self.app_model.set_command_to_shortcut)
        command_reload_button = ttk.Button(lower_frame,
                                           text="Reload",
                                           command=self.app_model.load_commands)
        start_button = ttk.Button(lower_frame,
                                  text="Start",
                                  command=self.app_model.start_command)
        pause_button = ttk.Button(lower_frame,
                                  text="Pause",
                                  command=self.app_model.pause_command)

        # Layout
        notebook.pack(expand=True, fill=tk.X, side=tk.LEFT)
        open_dir_button.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=(8, 0))
        upper_frame.pack(expand=True, fill=tk.X, side=tk.TOP, padx=4)

        shortcut_label.pack(expand=False, fill=tk.X, side=tk.LEFT)
        shortcut_spinbox.pack(expand=False, fill=tk.X, side=tk.LEFT)
        shortcut_set_button.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4)
        separator(lower_frame).pack(expand=False, fill=tk.Y, side=tk.LEFT, padx=5, pady=8)
        command_reload_button.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4)
        start_button.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4)
        pause_button.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4)
        lower_frame.pack(expand=False, fill=tk.BOTH, side=tk.TOP, padx=4, pady=4)

    def build_commands_notebook(self, master) -> ttk.Notebook:
        notebook = ttk.Notebook(master)

        commands_frame_builders = [
            self.build_python_commands_frame,
            self.build_mcu_commands_frame,
            self.build_shortcut_commands_frame,
        ]
        commands_builders: tuple[str, Callable[ttk.Widget, ttk.Frame], str] = map(
            lambda f: (f[0][0], f[1], f[0][1]),
            zip(COMMANDS, commands_frame_builders),
        )
        commands: dict[str, ttk.Frame] = {}
        for name, builder, tag_text in commands_builders:
            commands[name] = builder(notebook)
            notebook.add(commands[name], text=tag_text, padding=5, sticky=tk.NSEW)

        return notebook

    def build_python_commands_frame(self, notebook) -> ttk.Frame:
        frame = ttk.Frame(notebook)

        upper_frame = ttk.Frame(frame)
        lower_frame = ttk.Frame(frame)

        # Filter
        filter = tk.StringVar(value="-")
        filter_label = ttk.Label(upper_frame,
                                 text="Filter: ",
                                 width=8)
        filter_combobox = ttk.Combobox(upper_frame,
                                       state="readonly",
                                       textvariable=self.python_commands_filter,
                                       values=self.python_commands_filter_list)
        filter_combobox.bind("<<ComboboxSelected>>", self.app_model.set_python_commands_filter)

        # Command
        command_label = ttk.Label(lower_frame,
                                  text="Command: ",
                                  width=8)
        command_combobox = ttk.Combobox(lower_frame,
                                        state="readonly",
                                        textvariable=self.python_command,
                                        values=self.python_command_list)
        command_combobox.bind("<<ComboboxSelected>>", self.app_model.set_python_command)
        command_combobox.current(0)

        # Layout
        filter_label.pack(expand=False, fill=tk.X, side=tk.LEFT)
        filter_combobox.pack(expand=True, fill=tk.X, side=tk.LEFT)
        upper_frame.pack(expand=False, fill=tk.X, side=tk.TOP, padx=4, pady=4)

        command_label.pack(expand=False, fill=tk.X, side=tk.LEFT)
        command_combobox.pack(expand=True, fill=tk.X, side=tk.LEFT)
        lower_frame.pack(expand=False, fill=tk.X, side=tk.TOP, padx=4, pady=4)

        return frame

    def build_mcu_commands_frame(self, notebook) -> ttk.Frame:
        frame = ttk.Frame(notebook)

        upper_frame = ttk.Frame(frame)
        lower_frame = ttk.Frame(frame)

        # Filter
        filter_label = ttk.Label(upper_frame,
                                 text="Filter: ",
                                 width=8)
        filter_combobox = ttk.Combobox(upper_frame,
                                       state="readonly",
                                       textvariable=self.mcu_commands_filter,
                                       values=self.mcu_commands_filter_list)
        filter_combobox.bind("<<ComboboxSelected>>", self.app_model.set_mcu_commands_filter)

        # Command
        command_label = ttk.Label(lower_frame,
                                  text="Command: ",
                                  width=8)
        command_combobox = ttk.Combobox(lower_frame,
                                        state="readonly",
                                        textvariable=self.mcu_command,
                                        values=self.mcu_command_list)
        command_combobox.bind("<<ComboboxSelected>>", self.app_model.set_mcu_command)
        command_combobox.current(0)

        # Layout
        filter_label.pack(expand=False, fill=tk.X, side=tk.LEFT)
        filter_combobox.pack(expand=True, fill=tk.X, side=tk.LEFT)
        upper_frame.pack(expand=False, fill=tk.X, side=tk.TOP, padx=4, pady=4)

        command_label.pack(expand=False, fill=tk.X, side=tk.LEFT)
        command_combobox.pack(expand=True, fill=tk.X, side=tk.LEFT)
        lower_frame.pack(expand=False, fill=tk.X, side=tk.TOP, padx=4, pady=4)

        return frame

    def build_shortcut_commands_frame(self, notebook) -> ttk.Frame:
        frame = ttk.Frame(notebook)

        upper_frame = ttk.Frame(frame)
        lower_frame = ttk.Frame(frame)

        self.shortcut_button_texts = [
            tk.StringVar(value=f"({i})")
            for i in range(1, 11)
        ]
        self.shortcut_commands = [
            lambda: self.app_model.start_shortcut_command(id=1),
            lambda: self.app_model.start_shortcut_command(id=2),
            lambda: self.app_model.start_shortcut_command(id=3),
            lambda: self.app_model.start_shortcut_command(id=4),
            lambda: self.app_model.start_shortcut_command(id=5),
            lambda: self.app_model.start_shortcut_command(id=6),
            lambda: self.app_model.start_shortcut_command(id=7),
            lambda: self.app_model.start_shortcut_command(id=8),
            lambda: self.app_model.start_shortcut_command(id=9),
            lambda: self.app_model.start_shortcut_command(id=10),
        ]
        self.shortcut_buttons = [
                                    ttk.Button(upper_frame,
                                               width=7,
                                               textvariable=self.shortcut_button_texts[i],
                                               command=self.shortcut_commands[i])
                                    for i in range(5)
                                ] + [
                                    ttk.Button(lower_frame,
                                               width=7,
                                               textvariable=self.shortcut_button_texts[i],
                                               command=self.shortcut_commands[i])
                                    for i in range(5, 10)
                                ]

        # Layout
        for b in self.shortcut_buttons:
            b.pack(expand=True, fill=tk.X, side=tk.LEFT, padx=4, pady=2)
        upper_frame.pack(expand=False, fill=tk.X, side=tk.TOP, padx=4)
        lower_frame.pack(expand=False, fill=tk.X, side=tk.TOP, padx=4)

        return frame
