from typing import Callable
import tkinter as tk
import tkinter.ttk as ttk

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


class CommandsSettings(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._open_dir_button_image: tk.PhotoImage = tk.PhotoImage(file="../assets/icons8-OpenDir-16.png")
        self.shortcut_button_texts: list[tk.StringVar] = []
        self.shotcut_commands: list[Callable[[], None]] = []
        self.shortcut_buttons: list[ttk.Button] = []
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
                                     command=self.open_commands_directory)

        # Settings
        shotcut_number = tk.IntVar(value=1)
        shortcut_label = ttk.Label(lower_frame,
                                   text="Shortcut: ")
        shortcut_spinbox = ttk.Spinbox(lower_frame,
                                       width=7,
                                       from_=1,
                                       to=10,
                                       increment=1,
                                       textvariable=shotcut_number,
                                       command=self.set_shortcut_number)
        shortcut_set_button = ttk.Button(lower_frame,
                                         text="Set",
                                         command=self.set_command_to_shortcut)
        command_reload_button = ttk.Button(lower_frame,
                                           text="Reload",
                                           command=self.reload_commands)
        start_button = ttk.Button(lower_frame,
                                  text="Start",
                                  command=self.start_command)
        pause_button = ttk.Button(lower_frame,
                                  text="Pause",
                                  command=self.pause_command)

        # Layout
        notebook.pack(expand=True, fill=tk.X, side=tk.LEFT)
        open_dir_button.pack(expand=False, fill=tk.X, side=tk.LEFT)
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
        filter_list = [
            "-"
        ]
        filter = tk.StringVar(value="-")
        filter_label = ttk.Label(upper_frame,
                                 text="Filter:          ")
        filter_combobox = ttk.Combobox(upper_frame,
                                       state="readonly",
                                       textvariable=filter,
                                       values=filter_list)
        filter_combobox.bind("<<ComboboxSelected>>", self.set_python_commands_filter)

        # Command
        command_list = [
            "-"
        ]
        command = tk.StringVar(value="-")
        command_label = ttk.Label(lower_frame,
                                  text="Command: ")
        command_combobox = ttk.Combobox(lower_frame,
                                        state="readonly",
                                        textvariable=command,
                                        values=command_list)
        command_combobox.bind("<<ComboboxSelected>>", self.set_python_command)

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
        filter_list = [
            "-"
        ]
        filter = tk.StringVar(value="-")
        filter_label = ttk.Label(upper_frame,
                                 text="Filter:          ")
        filter_combobox = ttk.Combobox(upper_frame,
                                       state="readonly",
                                       textvariable=filter,
                                       values=filter_list)
        filter_combobox.bind("<<ComboboxSelected>>", self.set_mcu_commands_filter)

        # Command
        command_list = [
            "-"
        ]
        command = tk.StringVar(value="-")
        command_label = ttk.Label(lower_frame,
                                  text="Command: ")
        command_combobox = ttk.Combobox(lower_frame,
                                        state="readonly",
                                        textvariable=command,
                                        values=command_list)
        command_combobox.bind("<<ComboboxSelected>>", self.set_mcu_command)

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
            lambda: self.shortcut_command(id=1),
            lambda: self.shortcut_command(id=2),
            lambda: self.shortcut_command(id=3),
            lambda: self.shortcut_command(id=4),
            lambda: self.shortcut_command(id=5),
            lambda: self.shortcut_command(id=6),
            lambda: self.shortcut_command(id=7),
            lambda: self.shortcut_command(id=8),
            lambda: self.shortcut_command(id=9),
            lambda: self.shortcut_command(id=10),
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

    def set_python_commands_filter(self, event) -> None:
        pass

    def set_python_command(self, event) -> None:
        pass

    def set_mcu_commands_filter(self, event) -> None:
        pass

    def set_mcu_command(self, event) -> None:
        pass

    def shortcut_command(self, id: int) -> None:
        pass

    def open_commands_directory(self):
        pass

    def set_shortcut_number(self) -> None:
        pass

    def set_command_to_shortcut(self) -> None:
        pass

    def reload_commands(self) -> None:
        pass

    def start_command(self) -> None:
        pass

    def pause_command(self) -> None:
        pass
