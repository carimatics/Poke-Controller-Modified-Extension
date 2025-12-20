import tkinter as tk
import tkinter.ttk as ttk
from typing import Any, Literal

from .... import widgets
from ....core.command import get_app_command_state
from ....core.command.info import (
    get_selected_command_info,
    set_selected_command_info,
)
from ....model import get_app_model
from ....settings import get_app_settings
from ....translation import t
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
    _notebook: ttk.Notebook

    _python_commands_filter_list: list[str]
    _python_command_list: list[str]
    _python_commands_filter_combobox: widgets.Combobox
    _python_command_combobox: widgets.Combobox
    _mcu_commands_filter_list: list[str]
    _mcu_command_list: list[str]
    _mcu_commands_filter_combobox: widgets.Combobox
    _mcu_command_combobox: widgets.Combobox

    _shortcut_buttons: list[widgets.Button]

    _start_button: widgets.Button
    _pause_button: widgets.Button

    def __init__(self, master: tk.Misc, *args: Any, **kwargs: Any) -> None:
        super().__init__(master, *args, **kwargs)

        self._app_settings = get_app_settings()
        self._app_model = get_app_model()
        self._app_command_state = get_app_command_state()

        self._open_dir_button_image: tk.PhotoImage = tk.PhotoImage(
            file="../assets/icons8-OpenDir-16.png"
        )

        self._python_commands_filter = self._app_settings.command.python_commands_filter
        self._python_command = self._app_settings.command.python_command
        self._mcu_commands_filter = self._app_settings.command.mcu_commands_filter
        self._mcu_command = self._app_settings.command.mcu_command
        self._shortcut_number = self._app_settings.command.shortcut.number
        self._registered_commands = (
            self._app_settings.command.shortcut.registered_commands
        )

        self._load_commands()
        set_selected_command_info(self._commands[0])

        self._register_traces()

        self.build_ui()

    def build_ui(self) -> None:
        upper_frame = widgets.Frame(self)
        lower_frame = widgets.Frame(self)

        # Notebook
        self._notebook = self._build_commands_notebook(upper_frame)

        # Open Commands Directory
        open_dir_button = widgets.Button(
            upper_frame,
            tooltip=t("main.settings.commands.open_dir.tooltip"),
            width=5,
            image=self._open_dir_button_image,
            command=self._on_open_dir_pushed,
        )

        shortcut_label = widgets.Label(
            lower_frame,
            text=t("main.settings.commands.shortcut.label"),
            tooltip=t("main.settings.commands.shortcut.label.tooltip"),
        )
        shortcut_spinbox = widgets.Spinbox(
            lower_frame,
            tooltip=t("main.settings.commands.shortcut.spinbox.tooltip"),
            width=7,
            from_=1,
            to=10,
            increment=1,
            textvariable=self._shortcut_number,
        )
        shortcut_set_button = widgets.Button(
            lower_frame,
            text=t("main.settings.commands.set"),
            tooltip=t("main.settings.commands.set.tooltip"),
            command=self._on_set_pushed,
        )
        command_reload_button = widgets.Button(
            lower_frame,
            text=t("main.settings.commands.reload"),
            tooltip=t("main.settings.commands.reload.tooltip"),
            command=self._on_reload_pushed,
        )
        self._start_button = widgets.Button(
            lower_frame,
            text=t("main.settings.commands.start"),
            tooltip=t("main.settings.commands.start.tooltip"),
            command=self._on_start_pushed,
        )
        self._pause_button = widgets.Button(
            lower_frame,
            text=t("main.settings.commands.pause"),
            tooltip=t("main.settings.commands.pause.tooltip"),
            command=self._on_pause_pushed,
            state=tk.DISABLED,
        )

        # Layout
        self._notebook.pack(expand=True, fill=tk.X, side=tk.LEFT)
        open_dir_button.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=(8, 0))
        upper_frame.pack(expand=True, fill=tk.X, side=tk.TOP, padx=4)

        shortcut_label.pack(expand=False, fill=tk.X, side=tk.LEFT)
        shortcut_spinbox.pack(expand=False, fill=tk.X, side=tk.LEFT)
        shortcut_set_button.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4)
        widgets.Separator(master=lower_frame, orient=tk.VERTICAL).pack(
            expand=False, fill=tk.Y, side=tk.LEFT, padx=5, pady=8
        )
        command_reload_button.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4)
        self._start_button.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4)
        self._pause_button.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4)
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
            kind="python",
            filter_list=self._python_commands_filter_list,
            filter_var=self._python_commands_filter,
            command_list=self._python_command_list,
            command_var=self._python_command,
        )

    def _build_mcu_commands_frame(self, notebook: ttk.Notebook) -> widgets.Frame:
        return self._build_commands_frame(
            notebook=notebook,
            kind="mcu",
            filter_list=self._mcu_commands_filter_list,
            filter_var=self._mcu_commands_filter,
            command_list=self._mcu_command_list,
            command_var=self._mcu_command,
        )

    # noinspection PyMethodMayBeStatic
    def _build_commands_frame(
        self,
        notebook: ttk.Notebook,
        kind: Literal["python", "mcu"],
        filter_list: list[str],
        filter_var: tk.StringVar,
        command_list: list[str],
        command_var: tk.StringVar,
    ) -> widgets.Frame:
        frame = widgets.Frame(notebook)

        def _combobox_frame(
            master: widgets.Frame,
            component: str,
            var: tk.StringVar,
            values: list[str],
        ) -> tuple[widgets.Frame, widgets.Combobox]:
            combobox_frame = widgets.Frame(master=master)
            label = widgets.Label(
                combobox_frame,
                text=t(f"main.settings.commands.notebook.{kind}.{component}.label"),
                tooltip=t(
                    f"main.settings.commands.notebook.{kind}.{component}.label.tooltip"
                ),
                width=8,
            )
            combobox = widgets.Combobox(
                combobox_frame,
                tooltip=t(
                    f"main.settings.commands.notebook.{kind}.{component}.combobox.tooltip"
                ),
                textvariable=var,
                values=values,
            )
            if var.get() == "":
                combobox.current(0)

            # Layout
            label.pack(expand=False, fill=tk.X, side=tk.LEFT)
            combobox.pack(expand=True, fill=tk.X, side=tk.LEFT)

            return combobox_frame, combobox

        filter_frame, filter_combobox = _combobox_frame(
            frame,
            "filter",
            filter_var,
            filter_list,
        )
        if kind == "python":
            self._python_commands_filter_combobox = filter_combobox
        if kind == "mcu":
            self._mcu_commands_filter_combobox = filter_combobox
        command_frame, command_combobox = _combobox_frame(
            frame,
            "command",
            command_var,
            command_list,
        )
        if kind == "python":
            self._python_command_combobox = command_combobox
        if kind == "mcu":
            self._mcu_command_combobox = command_combobox

        # Layout
        filter_frame.pack(expand=False, fill=tk.X, side=tk.TOP, padx=4, pady=4)
        command_frame.pack(expand=False, fill=tk.X, side=tk.TOP, padx=4, pady=4)

        return frame

    def _build_shortcut_commands_frame(self, notebook: ttk.Notebook) -> widgets.Frame:
        frame = widgets.Frame(notebook)

        shortcut_commands = [
            lambda num=i: self._on_shortcut_pushed(num) for i in range(1, 11)
        ]

        upper_frame = widgets.Frame(frame)
        lower_frame = widgets.Frame(frame)
        self._shortcut_buttons = [
            widgets.Button(
                upper_frame if i < 5 else lower_frame,
                width=7,
                text=(self._registered_commands[str(i + 1)]).name.get()[:8],
                tooltip=(self._registered_commands[str(i + 1)]).name.get(),
                command=shortcut_commands[i],
            )
            for i in range(10)
        ]

        # Layout
        for b in self._shortcut_buttons:
            b.pack(expand=True, fill=tk.X, side=tk.LEFT, padx=4, pady=2)
        upper_frame.pack(expand=False, fill=tk.X, side=tk.TOP, padx=4)
        lower_frame.pack(expand=False, fill=tk.X, side=tk.TOP, padx=4)

        return frame

    def _load_commands(self) -> None:
        self._commands = self._app_model.load_commands()

        def load_lists(
            kind: Literal["python", "mcu"],
            filter_var: tk.StringVar,
        ) -> tuple[list[str], list[str]]:
            filter_value = filter_var.get()
            use_filter = filter_value != "-"
            tags = set([t for c in self._commands if c.kind == kind for t in c.tags])
            filters = (
                ["-"]
                + sorted([t for t in tags if not t.startswith("@")])
                + sorted([t for t in tags if t.startswith("@")])
            )
            commands = [
                c.display_name
                for c in self._commands
                if c.kind == kind and (not use_filter or filter_value in c.tags)
            ]

            return filters, commands

        filter_list, command_list = load_lists("python", self._python_commands_filter)
        self._python_commands_filter_list = filter_list
        self._python_command_list = command_list

        filter_list, command_list = load_lists("mcu", self._mcu_commands_filter)
        self._mcu_commands_filter_list = filter_list
        self._mcu_command_list = command_list

    def _filter_commands(self) -> None:
        def filter_commands(
            kind: Literal["python", "mcu"],
            filter_var: tk.StringVar,
        ) -> list[str]:
            filter_value = filter_var.get()
            use_filter = filter_value != "-"
            commands = [
                c.display_name
                for c in self._commands
                if c.kind == kind and (not use_filter or filter_value in c.tags)
            ]

            return commands

        self._python_command_list = filter_commands(
            "python",
            self._python_commands_filter,
        )
        self._mcu_command_list = filter_commands(
            "mcu",
            self._mcu_commands_filter,
        )

    def _update_commands(self) -> None:
        def update_combobox(
            combobox: widgets.Combobox,
            items: list[str],
        ) -> None:
            combobox.configure(values=items)

            if not items:
                return

            hit = False
            for i, item in enumerate(items):
                if item == combobox.get():
                    hit = True
                    combobox.current(i)
                    break
            if not hit:
                combobox.current(0)

        update_combobox(
            self._python_commands_filter_combobox,
            self._python_commands_filter_list,
        )
        update_combobox(
            self._mcu_commands_filter_combobox,
            self._mcu_commands_filter_list,
        )
        update_combobox(
            self._python_command_combobox,
            self._python_command_list,
        )
        update_combobox(
            self._mcu_command_combobox,
            self._mcu_command_list,
        )

    def _on_open_dir_pushed(self) -> None:
        self._app_model.open_commands_directory_window()

    def _on_set_pushed(self) -> None:
        shortcut_number = self._shortcut_number.get()
        if self._notebook.index(self._notebook.select()) == 0:
            klass = "Python"
        elif self._notebook.index(self._notebook.select()) == 1:
            klass = "Mcu"
        else:
            return

        if klass == "Python":
            name = self._python_command.get()
        elif klass == "Mcu":
            name = self._mcu_command.get()
        else:
            return

        shortcut = self._registered_commands[str(shortcut_number)]
        shortcut.klass.set(klass)
        shortcut.name.set(name)
        button = self._shortcut_buttons[shortcut_number - 1]
        button.configure(text=name[:8])
        button.set_tooltip(text=name)

    def _start_command(self) -> None:
        if (command := get_selected_command_info()) is not None:
            self._app_model.start_command(command)

    def _start_shortcut_command(self, num: int) -> None:
        shortcut_number = str(num)
        klass = self._registered_commands[shortcut_number].klass.get()
        name = self._registered_commands[shortcut_number].name.get()

        if klass == "Python":
            for c in [c for c in self._commands if c.kind == PYTHON]:
                if c.display_name == name:
                    self._app_model.start_command(c)
                    return
        elif klass == "Mcu":
            for c in [c for c in self._commands if c.kind == MCU]:
                if c.display_name == name:
                    self._app_model.start_command(c)
                    return

    def _stop_command(self) -> None:
        self._app_model.stop_command()

    def _configure_start_button(self) -> None:
        self._start_button.configure(text="Start", command=self._on_start_pushed)

    def _configure_stop_button(self) -> None:
        self._start_button.configure(text="Stop", command=self._on_stop_pushed)

    def _enable_shortcut_buttons(self) -> None:
        for i in range(10):
            button = self._shortcut_buttons[i]
            button.configure(state=tk.NORMAL)

    def _disable_shortcut_buttons(self) -> None:
        for i in range(10):
            button = self._shortcut_buttons[i]
            button.configure(state=tk.DISABLED)

    def _enable_pause_button(self) -> None:
        self._pause_button.configure(state=tk.NORMAL)

    def _disable_pause_button(self) -> None:
        self._pause_button.configure(state=tk.DISABLED)

    def _on_running_changed(self, *_: str) -> None:
        if self._app_command_state.is_running.get():
            self._disable_shortcut_buttons()
            self._configure_stop_button()

    def _on_stopped_changed(self, *_: str) -> None:
        if self._app_command_state.is_stopped.get():
            self._enable_shortcut_buttons()
            self._configure_start_button()

    def _on_paused_changed(self, *_: str) -> None:
        is_running = self._app_command_state.is_running.get()
        is_paused = self._app_command_state.is_paused.get()
        if not is_running:
            self._disable_pause_button()
        elif is_running and not is_paused:
            self._disable_pause_button()
        else:
            self._enable_pause_button()

    def _on_reload_pushed(self) -> None:
        self._load_commands()
        self._update_commands()

    def _on_start_pushed(self) -> None:
        self._start_command()

    def _on_stop_pushed(self) -> None:
        self._stop_command()

    def _on_pause_pushed(self) -> None:
        self._app_model.pause_command()

    def _on_shortcut_pushed(self, shortcut_number: int) -> None:
        self._start_shortcut_command(shortcut_number)

    def _on_filter_changed(self, *_: str) -> None:
        self._filter_commands()
        self._update_commands()

    def _on_python_command_changed(self, *_: str) -> None:
        for command in [
            command for command in self._commands if command.kind == PYTHON
        ]:
            if command.display_name == self._python_command.get():
                set_selected_command_info(command)
                return

    def _on_mcu_command_changed(self, *_: str) -> None:
        for command in [command for command in self._commands if command.kind == MCU]:
            if command.display_name == self._mcu_command.get():
                set_selected_command_info(command)
                return

    def _register_traces(self) -> None:
        self.register_trace(
            "write",
            self._python_commands_filter,
            self._on_filter_changed,
        )
        self.register_trace(
            "write",
            self._mcu_commands_filter,
            self._on_filter_changed,
        )
        self.register_trace(
            "write",
            self._python_command,
            self._on_python_command_changed,
        )
        self.register_trace(
            "write",
            self._mcu_command,
            self._on_mcu_command_changed,
        )
        self.register_trace(
            "write",
            self._app_command_state.is_running,
            self._on_running_changed,
        )
        self.register_trace(
            "write",
            self._app_command_state.is_stopped,
            self._on_stopped_changed,
        )
        self.register_trace(
            "write",
            self._app_command_state.is_paused,
            self._on_paused_changed,
        )
