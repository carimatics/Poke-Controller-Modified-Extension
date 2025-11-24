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

        self._python_commands_filter_list: list[str] = self._load_python_commands_filter_list()
        self._python_command_list: list[str] = self._load_python_command_list()
        self._mcu_commands_filter_list: list[str] = self._load_mcu_commands_filter_list()
        self._mcu_command_list: list[str] = self._load_mcu_command_list()
        self._shortcut_button_texts: list[tk.StringVar] = []
        self._shortcut_commands: list[Callable[[], None]] = []
        self._shortcut_buttons: list[ttk.Button] = []

        # noinspection PyTypeChecker
        self._python_commands_filter: tk.StringVar = self.app_state.command_python_commands_filter
        # noinspection PyTypeChecker
        self._python_command: tk.StringVar = self.app_state.command_python_command
        # noinspection PyTypeChecker
        self._mcu_commands_filter: tk.StringVar = self.app_state.command_mcu_commands_filter
        # noinspection PyTypeChecker
        self._mcu_command: tk.StringVar = self.app_state.command_mcu_command
        # noinspection PyTypeChecker
        self._shortcut_number: tk.StringVar = self.app_state.command_shortcut_number
        # noinspection PyTypeChecker
        self._shortcuts: tk.StringVar = self.app_state.command_shortcuts

        self.build_ui()

    def build_ui(self):
        upper_frame = ttk.Frame(self)
        lower_frame = ttk.Frame(self)

        # Notebook
        notebook = self._build_commands_notebook(upper_frame)

        # Open Commands Directory
        open_dir_button = ttk.Button(upper_frame,
                                     width=5,
                                     image=self._open_dir_button_image,
                                     command=self._on_open_dir_pushed)

        # Settings
        shortcut_label = ttk.Label(lower_frame,
                                   text="Shortcut: ")
        shortcut_spinbox = ttk.Spinbox(lower_frame,
                                       width=7,
                                       from_=1,
                                       to=10,
                                       increment=1,
                                       textvariable=self._shortcut_number,
                                       command=self._on_shortcut_number_changed)
        shortcut_set_button = ttk.Button(lower_frame,
                                         text="Set",
                                         command=self._on_set_pushed)
        command_reload_button = ttk.Button(lower_frame,
                                           text="Reload",
                                           command=self._on_reload_pushed)
        start_button = ttk.Button(lower_frame,
                                  text="Start",
                                  command=self._on_start_pushed)
        pause_button = ttk.Button(lower_frame,
                                  text="Pause",
                                  command=self._on_pause_pushed)

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

    def _build_commands_notebook(self, master) -> ttk.Notebook:
        notebook = ttk.Notebook(master)

        commands_frame_builders = [
            self._build_python_commands_frame,
            self._build_mcu_commands_frame,
            self._build_shortcut_commands_frame,
        ]
        commands_builders: tuple[str, Callable[[ttk.Widget], ttk.Frame], str] = map(
            lambda f: (f[0][0], f[1], f[0][1]),
            zip(COMMANDS, commands_frame_builders),
        )
        commands: dict[str, ttk.Frame] = {}
        for name, builder, tag_text in commands_builders:
            commands[name] = builder(notebook)
            notebook.add(commands[name], text=tag_text, padding=5, sticky=tk.NSEW)

        return notebook

    def _build_python_commands_frame(self, notebook) -> ttk.Frame:
        frame = ttk.Frame(notebook)

        upper_frame = ttk.Frame(frame)
        lower_frame = ttk.Frame(frame)

        # Filter
        filter_label = ttk.Label(upper_frame,
                                 text="Filter: ",
                                 width=8)
        filter_combobox = ttk.Combobox(upper_frame,
                                       state="readonly",
                                       textvariable=self._python_commands_filter,
                                       values=self._python_commands_filter_list)
        filter_combobox.bind("<<ComboboxSelected>>", self._on_python_commands_filter_selected, add="")

        # Command
        command_label = ttk.Label(lower_frame,
                                  text="Command: ",
                                  width=8)
        command_combobox = ttk.Combobox(lower_frame,
                                        state="readonly",
                                        textvariable=self._python_command,
                                        values=self._python_command_list)
        command_combobox.bind("<<ComboboxSelected>>", self._on_python_command_selected, add="")
        command_combobox.current(0)

        # Layout
        filter_label.pack(expand=False, fill=tk.X, side=tk.LEFT)
        filter_combobox.pack(expand=True, fill=tk.X, side=tk.LEFT)
        upper_frame.pack(expand=False, fill=tk.X, side=tk.TOP, padx=4, pady=4)

        command_label.pack(expand=False, fill=tk.X, side=tk.LEFT)
        command_combobox.pack(expand=True, fill=tk.X, side=tk.LEFT)
        lower_frame.pack(expand=False, fill=tk.X, side=tk.TOP, padx=4, pady=4)

        return frame

    def _build_mcu_commands_frame(self, notebook) -> ttk.Frame:
        frame = ttk.Frame(notebook)

        upper_frame = ttk.Frame(frame)
        lower_frame = ttk.Frame(frame)

        # Filter
        filter_label = ttk.Label(upper_frame,
                                 text="Filter: ",
                                 width=8)
        filter_combobox = ttk.Combobox(upper_frame,
                                       state="readonly",
                                       textvariable=self._mcu_commands_filter,
                                       values=self._mcu_commands_filter_list)
        filter_combobox.bind("<<ComboboxSelected>>", self._on_mcu_commands_filter_selected, add="")

        # Command
        command_label = ttk.Label(lower_frame,
                                  text="Command: ",
                                  width=8)
        command_combobox = ttk.Combobox(lower_frame,
                                        state="readonly",
                                        textvariable=self._mcu_command,
                                        values=self._mcu_command_list)
        command_combobox.bind("<<ComboboxSelected>>", self._on_mcu_command_selected, add="")
        command_combobox.current(0)

        # Layout
        filter_label.pack(expand=False, fill=tk.X, side=tk.LEFT)
        filter_combobox.pack(expand=True, fill=tk.X, side=tk.LEFT)
        upper_frame.pack(expand=False, fill=tk.X, side=tk.TOP, padx=4, pady=4)

        command_label.pack(expand=False, fill=tk.X, side=tk.LEFT)
        command_combobox.pack(expand=True, fill=tk.X, side=tk.LEFT)
        lower_frame.pack(expand=False, fill=tk.X, side=tk.TOP, padx=4, pady=4)

        return frame

    def _build_shortcut_commands_frame(self, notebook) -> ttk.Frame:
        frame = ttk.Frame(notebook)

        upper_frame = ttk.Frame(frame)
        lower_frame = ttk.Frame(frame)

        self._shortcut_button_texts = [
            tk.StringVar(value=f"({i})")
            for i in range(1, 11)
        ]
        self._shortcut_commands = [lambda i=num: self._on_shortcut_pushed(i) for num in range(1, 11)]
        self._shortcut_buttons = [
            ttk.Button(upper_frame if i < 5 else lower_frame,
                       width=7,
                       textvariable=self._shortcut_button_texts[i],
                       command=self._shortcut_commands[i])
            for i in range(10)
        ]

        # Layout
        for b in self._shortcut_buttons:
            b.pack(expand=True, fill=tk.X, side=tk.LEFT, padx=4, pady=2)
        upper_frame.pack(expand=False, fill=tk.X, side=tk.TOP, padx=4)
        lower_frame.pack(expand=False, fill=tk.X, side=tk.TOP, padx=4)

        return frame

    def _load_python_commands_filter_list(self) -> list[str]:
        return self.app_model.load_python_commands_filter_list()

    def _load_python_command_list(self) -> list[str]:
        return self.app_model.load_python_command_list()

    def _load_mcu_commands_filter_list(self) -> list[str]:
        return self.app_model.load_mcu_commands_filter_list()

    def _load_mcu_command_list(self) -> list[str]:
        return self.app_model.load_mcu_command_list()

    def _on_open_dir_pushed(self):
        self.app_model.open_commands_directory_window()

    def _on_shortcut_number_changed(self):
        self.app_model.set_command_shortcut_number()

    def _on_set_pushed(self):
        self.app_model.register_command_shortcut()

    def _on_reload_pushed(self):
        self.app_model.load_commands()

    def _on_start_pushed(self):
        self.app_model.start_command()

    def _on_pause_pushed(self):
        self.app_model.pause_command()

    def _on_python_commands_filter_selected(self, _event):
        self.app_model.apply_python_commands_filter()

    def _on_python_command_selected(self, _event):
        self.app_model.set_python_command()

    def _on_mcu_commands_filter_selected(self, _event):
        self.app_model.apply_mcu_commands_filter()

    def _on_mcu_command_selected(self, _event):
        self.app_model.set_mcu_command()

    def _on_shortcut_pushed(self, shortcut_number: int):
        self.app_model.start_shortcut_command(shortcut_number)
