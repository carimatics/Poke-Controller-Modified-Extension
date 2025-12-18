import tkinter as tk
import tkinter.ttk as ttk
from typing import Any, Callable

from .... import widgets
from ....model import get_app_model
from ....settings import get_app_settings
from ....widgets.app import AppFrame

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

        self._app_settings = get_app_settings()
        self._app_model = get_app_model()

        self._commands = self._app_model.load_commands()

        self._open_dir_button_image: tk.PhotoImage = tk.PhotoImage(
            file="../assets/icons8-OpenDir-16.png"
        )

        self._python_commands_filter_list: list[str] = [
            t
            for c in self._commands
            if c.kind == PYTHON and hasattr(c.klass, "TAGS")
            for t in c.klass.TAGS
        ]
        self._python_command_list: list[str] = [
            c.klass.NAME
            for c in self._commands
            if c.kind == PYTHON and c.klass.NAME != ""
        ]
        self._mcu_commands_filter_list: list[str] = [
            t
            for c in self._commands
            if c.kind == MCU and hasattr(c.klass, "TAGS")
            for t in c.klass.TAGS
        ]
        self._mcu_command_list: list[str] = [
            c.klass.NAME for c in self._commands if c.kind == MCU and c.klass.NAME != ""
        ]
        self._shortcut_button_texts: list[tk.StringVar] = []

        self._python_commands_filter = self._app_settings.command.python_commands_filter
        self._python_command = self._app_settings.command.python_command
        self._mcu_commands_filter = self._app_settings.command.mcu_commands_filter
        self._mcu_command = self._app_settings.command.mcu_command
        self._shortcut_number = self._app_settings.command.shortcut.number
        self._registered_commands = (
            self._app_settings.command.shortcut.registered_commands
        )

        self.build_ui()

    def build_ui(self) -> None:
        upper_frame = widgets.Frame(self)
        lower_frame = widgets.Frame(self)

        # Notebook
        notebook = self._build_commands_notebook(upper_frame)

        # Open Commands Directory
        open_dir_button = widgets.Button(
            upper_frame,
            width=5,
            image=self._open_dir_button_image,
            command=self._on_open_dir_pushed,
        )

        # Settings
        shortcut_label = widgets.Label(lower_frame, text="Shortcut: ")
        shortcut_spinbox = widgets.Spinbox(
            lower_frame,
            width=7,
            from_=1,
            to=10,
            increment=1,
            textvariable=self._shortcut_number,
            command=self._on_shortcut_number_changed,
        )
        shortcut_set_button = widgets.Button(
            lower_frame,
            text="Set",
            command=self._on_set_pushed,
        )
        command_reload_button = widgets.Button(
            lower_frame,
            text="Reload",
            command=self._on_reload_pushed,
        )
        start_button = widgets.Button(
            lower_frame,
            text="Start",
            command=self._on_start_pushed,
        )
        pause_button = widgets.Button(
            lower_frame,
            text="Pause",
            command=self._on_pause_pushed,
        )

        # Layout
        notebook.pack(expand=True, fill=tk.X, side=tk.LEFT)
        open_dir_button.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=(8, 0))
        upper_frame.pack(expand=True, fill=tk.X, side=tk.TOP, padx=4)

        shortcut_label.pack(expand=False, fill=tk.X, side=tk.LEFT)
        shortcut_spinbox.pack(expand=False, fill=tk.X, side=tk.LEFT)
        shortcut_set_button.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4)
        widgets.Separator(master=lower_frame, orient=tk.VERTICAL).pack(
            expand=False, fill=tk.Y, side=tk.LEFT, padx=5, pady=8
        )
        command_reload_button.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4)
        start_button.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4)
        pause_button.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4)
        lower_frame.pack(expand=False, fill=tk.BOTH, side=tk.TOP, padx=4, pady=4)

    def _build_commands_notebook(self, master: widgets.Frame) -> ttk.Notebook:
        notebook = ttk.Notebook(master)

        command_frames: list[widgets.Frame] = [
            self._build_python_commands_frame(notebook),
            self._build_mcu_commands_frame(notebook),
            self._build_shortcut_commands_frame(notebook),
        ]

        commands: dict[str, widgets.Frame] = {}
        for (name, tag_text), frame in zip(COMMANDS, command_frames):
            commands[name] = frame
            notebook.add(frame, text=tag_text, padding=5, sticky=tk.NSEW)

        return notebook

    def _build_python_commands_frame(self, notebook: ttk.Notebook) -> widgets.Frame:
        return self._build_commands_frame(
            notebook=notebook,
            filter_list=self._python_commands_filter_list,
            filter_var=self._python_commands_filter,
            on_filter_selected=self._on_python_commands_filter_selected,
            command_list=self._python_command_list,
            command_var=self._python_command,
            on_command_selected=self._on_python_command_selected,
        )

    def _build_mcu_commands_frame(self, notebook: ttk.Notebook) -> widgets.Frame:
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
    ) -> widgets.Frame:
        frame = widgets.Frame(notebook)

        def _combobox_frame(
            master: widgets.Frame,
            text: str,
            var: tk.StringVar,
            values: list[str],
            on_changed: Callable[[tk.Event], None],
        ) -> widgets.Frame:
            combobox_frame = widgets.Frame(master=master)
            label = widgets.Label(combobox_frame, text=text, width=8)
            combobox = widgets.Combobox(
                combobox_frame,
                state="readonly",
                textvariable=var,
                values=values,
            )
            combobox.bind("<<ComboboxSelected>>", func=on_changed, add="")

            # Layout
            label.pack(expand=False, fill=tk.X, side=tk.LEFT)
            combobox.pack(expand=True, fill=tk.X, side=tk.LEFT)

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
        upper_frame.pack(expand=False, fill=tk.X, side=tk.TOP, padx=4, pady=4)
        lower_frame.pack(expand=False, fill=tk.X, side=tk.TOP, padx=4, pady=4)

        return frame

    def _build_shortcut_commands_frame(self, notebook: ttk.Notebook) -> widgets.Frame:
        frame = widgets.Frame(notebook)

        self._shortcut_button_texts = [
            tk.StringVar(value=f"({i})") for i in range(1, 11)
        ]
        shortcut_commands = [
            lambda num=i: self._on_shortcut_pushed(num) for i in range(1, 11)
        ]

        upper_frame = widgets.Frame(frame)
        lower_frame = widgets.Frame(frame)
        shortcut_buttons = [
            widgets.Button(
                upper_frame if i < 5 else lower_frame,
                width=7,
                textvariable=self._shortcut_button_texts[i],
                command=shortcut_commands[i],
            )
            for i in range(10)
        ]

        # Layout
        for b in shortcut_buttons:
            b.pack(expand=True, fill=tk.X, side=tk.LEFT, padx=4, pady=2)
        upper_frame.pack(expand=False, fill=tk.X, side=tk.TOP, padx=4)
        lower_frame.pack(expand=False, fill=tk.X, side=tk.TOP, padx=4)

        return frame

    def _on_open_dir_pushed(self) -> None:
        self._app_model.open_commands_directory_window()

    def _on_shortcut_number_changed(self) -> None:
        self._app_model.set_command_shortcut_number()

    def _on_set_pushed(self) -> None:
        self._app_model.register_command_shortcut()

    def _on_reload_pushed(self) -> None:
        self._commands = self._app_model.load_commands()
        self._python_commands_filter_list = [
            t for c in self._commands if c.kind == PYTHON for t in c.klass.TAGS
        ]
        self._python_command_list = [
            c.klass.NAME for c in self._commands if c.kind == PYTHON
        ]
        self._mcu_commands_filter_list = [
            t for c in self._commands if c.kind == MCU for t in c.klass.TAGS
        ]
        self._mcu_command_list = [c.klass.NAME for c in self._commands if c.kind == MCU]

    def _on_start_pushed(self) -> None:
        pass

    def _on_pause_pushed(self) -> None:
        self._app_model.pause_command()

    def _on_python_commands_filter_selected(self, _event: tk.Event) -> None:
        self._app_model.apply_python_commands_filter()

    def _on_python_command_selected(self, _event: tk.Event) -> None:
        self._app_model.set_python_command()

    def _on_mcu_commands_filter_selected(self, _event: tk.Event) -> None:
        self._app_model.apply_mcu_commands_filter()

    def _on_mcu_command_selected(self, _event: tk.Event) -> None:
        self._app_model.set_mcu_command()

    def _on_shortcut_pushed(self, shortcut_number: int) -> None:
        self._app_model.start_shortcut_command(shortcut_number)
