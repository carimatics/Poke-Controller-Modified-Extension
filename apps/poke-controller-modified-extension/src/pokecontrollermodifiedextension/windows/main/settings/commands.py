import tkinter as tk
import tkinter.ttk as ttk
from typing import Any, Callable

from ....model import AppModel
from ....settings import AppSettings
from ....values import literals as l
from ....widgets import AppFrame

PYTHON = "python"
MCU = "mcu"
SHORTCUT = "shortcut"

COMMANDS = [
    (PYTHON, "Python Commands"),
    (MCU, "MCU Commands"),
    (SHORTCUT, "Shortcut"),
]


class CommandsSettings(AppFrame):
    def __init__(self, master: tk.Misc, *args: Any, **kwargs: Any) -> None:
        super().__init__(master, *args, **kwargs)

        self._open_dir_button_image: tk.PhotoImage = tk.PhotoImage(
            file="../assets/icons8-OpenDir-16.png"
        )

        self._python_commands_filter_list: list[str] = (
            self._load_python_commands_filter_list()
        )
        self._python_command_list: list[str] = self._load_python_command_list()
        self._mcu_commands_filter_list: list[str] = (
            self._load_mcu_commands_filter_list()
        )
        self._mcu_command_list: list[str] = self._load_mcu_command_list()
        self._shortcut_button_texts: list[tk.StringVar] = []

        self._python_commands_filter = self.app_state.command.python_commands_filter
        self._python_command = self.app_state.command.python_command
        self._mcu_commands_filter = self.app_state.command.mcu_commands_filter
        self._mcu_command = self.app_state.command.mcu_command
        self._shortcut_number = self.app_state.command.shortcut.number
        self._registered_commands = self.app_state.command.shortcut.registered_commands

        self.build_ui()

    @property
    def app_state(self) -> AppSettings:
        return self.app.settings

    @property
    def app_model(self) -> AppModel:
        return self.app.app_model

    def build_ui(self) -> None:
        upper_frame = ttk.Frame(self)
        lower_frame = ttk.Frame(self)

        # Notebook
        notebook = self._build_commands_notebook(upper_frame)

        # Open Commands Directory
        open_dir_button = ttk.Button(
            upper_frame,
            width=5,
            image=self._open_dir_button_image,
            command=self._on_open_dir_pushed,
        )

        # Settings
        shortcut_label = ttk.Label(lower_frame, text="Shortcut: ")
        shortcut_spinbox = ttk.Spinbox(
            lower_frame,
            width=7,
            from_=1,
            to=10,
            increment=1,
            textvariable=self._shortcut_number,
            command=self._on_shortcut_number_changed,
        )
        shortcut_set_button = ttk.Button(
            lower_frame,
            text="Set",
            command=self._on_set_pushed,
        )
        command_reload_button = ttk.Button(
            lower_frame,
            text="Reload",
            command=self._on_reload_pushed,
        )
        start_button = ttk.Button(
            lower_frame,
            text="Start",
            command=self._on_start_pushed,
        )
        pause_button = ttk.Button(
            lower_frame,
            text="Pause",
            command=self._on_pause_pushed,
        )

        # Layout
        notebook.pack(expand=True, fill=l.X, side=l.LEFT)
        open_dir_button.pack(expand=False, fill=l.X, side=l.LEFT, padx=(8, 0))
        upper_frame.pack(expand=True, fill=l.X, side=l.TOP, padx=4)

        shortcut_label.pack(expand=False, fill=l.X, side=l.LEFT)
        shortcut_spinbox.pack(expand=False, fill=l.X, side=l.LEFT)
        shortcut_set_button.pack(expand=False, fill=l.X, side=l.LEFT, padx=4)
        ttk.Separator(master=lower_frame, orient=l.VERTICAL).pack(
            expand=False, fill=l.Y, side=l.LEFT, padx=5, pady=8
        )
        command_reload_button.pack(expand=False, fill=l.X, side=l.LEFT, padx=4)
        start_button.pack(expand=False, fill=l.X, side=l.LEFT, padx=4)
        pause_button.pack(expand=False, fill=l.X, side=l.LEFT, padx=4)
        lower_frame.pack(expand=False, fill=l.BOTH, side=l.TOP, padx=4, pady=4)

    def _build_commands_notebook(self, master: ttk.Frame) -> ttk.Notebook:
        notebook = ttk.Notebook(master)

        command_frames: list[ttk.Frame] = [
            self._build_python_commands_frame(notebook),
            self._build_mcu_commands_frame(notebook),
            self._build_shortcut_commands_frame(notebook),
        ]

        commands: dict[str, ttk.Frame] = {}
        for (name, tag_text), frame in zip(COMMANDS, command_frames):
            commands[name] = frame
            notebook.add(frame, text=tag_text, padding=5, sticky=l.NSEW)

        return notebook

    def _build_python_commands_frame(self, notebook: ttk.Notebook) -> ttk.Frame:
        return self._build_commands_frame(
            notebook=notebook,
            filter_list=self._python_commands_filter_list,
            filter_var=self._python_commands_filter,
            on_filter_selected=self._on_python_commands_filter_selected,
            command_list=self._python_command_list,
            command_var=self._python_command,
            on_command_selected=self._on_python_command_selected,
        )

    def _build_mcu_commands_frame(self, notebook: ttk.Notebook) -> ttk.Frame:
        return self._build_commands_frame(
            notebook=notebook,
            filter_list=self._mcu_commands_filter_list,
            filter_var=self._mcu_commands_filter,
            on_filter_selected=self._on_mcu_commands_filter_selected,
            command_list=self._mcu_command_list,
            command_var=self._mcu_command,
            on_command_selected=self._on_mcu_command_selected,
        )

    # noinspection PyMethodMayBeStatic
    def _build_commands_frame(
        self,
        notebook: ttk.Notebook,
        filter_list: list[str],
        filter_var: tk.StringVar,
        on_filter_selected: Callable[[tk.Event], None],
        command_list: list[str],
        command_var: tk.StringVar,
        on_command_selected: Callable[[tk.Event], None],
    ) -> ttk.Frame:
        frame = ttk.Frame(notebook)

        def _combobox_frame(
            master: ttk.Frame,
            text: str,
            var: tk.StringVar,
            values: list[str],
            on_changed: Callable[[tk.Event], None],
        ) -> ttk.Frame:
            combobox_frame = ttk.Frame(master=master)
            label = ttk.Label(combobox_frame, text=text, width=8)
            combobox = ttk.Combobox(
                combobox_frame,
                state=l.READONLY,
                textvariable=var,
                values=values,
            )
            combobox.bind("<<ComboboxSelected>>", func=on_changed, add="")

            # Layout
            label.pack(expand=False, fill=l.X, side=l.LEFT)
            combobox.pack(expand=True, fill=l.X, side=l.LEFT)

            return combobox_frame

        # Filter
        upper_frame = _combobox_frame(
            frame,
            "Filter:",
            filter_var,
            filter_list,
            on_filter_selected,
        )
        lower_frame = _combobox_frame(
            frame,
            "Command:",
            command_var,
            command_list,
            on_command_selected,
        )

        # Layout
        upper_frame.pack(expand=False, fill=l.X, side=l.TOP, padx=4, pady=4)
        lower_frame.pack(expand=False, fill=l.X, side=l.TOP, padx=4, pady=4)

        return frame

    def _build_shortcut_commands_frame(self, notebook: ttk.Notebook) -> ttk.Frame:
        frame = ttk.Frame(notebook)

        self._shortcut_button_texts = [
            tk.StringVar(value=f"({i})") for i in range(1, 11)
        ]
        shortcut_commands = [
            lambda num=i: self._on_shortcut_pushed(num) for i in range(1, 11)
        ]

        upper_frame = ttk.Frame(frame)
        lower_frame = ttk.Frame(frame)
        shortcut_buttons = [
            ttk.Button(
                upper_frame if i < 5 else lower_frame,
                width=7,
                textvariable=self._shortcut_button_texts[i],
                command=shortcut_commands[i],
            )
            for i in range(10)
        ]

        # Layout
        for b in shortcut_buttons:
            b.pack(expand=True, fill=l.X, side=l.LEFT, padx=4, pady=2)
        upper_frame.pack(expand=False, fill=l.X, side=l.TOP, padx=4)
        lower_frame.pack(expand=False, fill=l.X, side=l.TOP, padx=4)

        return frame

    def _load_python_commands_filter_list(self) -> list[str]:
        return self.app_model.load_python_commands_filter_list()

    def _load_python_command_list(self) -> list[str]:
        return self.app_model.load_python_command_list()

    def _load_mcu_commands_filter_list(self) -> list[str]:
        return self.app_model.load_mcu_commands_filter_list()

    def _load_mcu_command_list(self) -> list[str]:
        return self.app_model.load_mcu_command_list()

    def _on_open_dir_pushed(self) -> None:
        self.app_model.open_commands_directory_window()

    def _on_shortcut_number_changed(self) -> None:
        self.app_model.set_command_shortcut_number()

    def _on_set_pushed(self) -> None:
        self.app_model.register_command_shortcut()

    def _on_reload_pushed(self) -> None:
        self.app_model.load_commands()

    def _on_start_pushed(self) -> None:
        self.app_model.start_command()

    def _on_pause_pushed(self) -> None:
        self.app_model.pause_command()

    def _on_python_commands_filter_selected(self, _event: tk.Event) -> None:
        self.app_model.apply_python_commands_filter()

    def _on_python_command_selected(self, _event: tk.Event) -> None:
        self.app_model.set_python_command()

    def _on_mcu_commands_filter_selected(self, _event: tk.Event) -> None:
        self.app_model.apply_mcu_commands_filter()

    def _on_mcu_command_selected(self, _event: tk.Event) -> None:
        self.app_model.set_mcu_command()

    def _on_shortcut_pushed(self, shortcut_number: int) -> None:
        self.app_model.start_shortcut_command(shortcut_number)
