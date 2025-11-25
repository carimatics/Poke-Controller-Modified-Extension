from typing import Callable, Literal
import tkinter as tk

from ...state import (
    PokeControllerAppState,
    Variable as StateVariable,
)


class Variable[T](StateVariable[T]):
    def __init__(self, value: T, *, with_none: bool = False):
        StateVariable.__init__(self)
        self._container = self._gen_container(value, with_none)

    @property
    def container(self) -> tk.Variable:
        return self._container

    def get(self) -> T | None:
        return self._container.get()

    def set(self, value: T | None) -> None:
        self._container.set(value)

    def register_hook(self, mode: Literal["read", "write"], callback: Callable[[], None]) -> str:
        return self._container.trace_add(mode, lambda _n, _i, _m: callback())

    def unregister_hook(self, mode: Literal["read", "write"], callback_id: str):
        self._container.trace_remove(mode, callback_id)

    # noinspection PyMethodMayBeStatic
    def _gen_container(self, value: T, with_none: bool) -> tk.Variable:
        v = None if with_none else value
        if isinstance(value, int):
            return tk.IntVar(value=v)
        elif isinstance(value, float):
            return tk.DoubleVar(value=v)
        elif isinstance(value, bool):
            return tk.BooleanVar(value=v)
        elif isinstance(value, str):
            return tk.StringVar(value=v)
        else:
            raise ValueError(f"Unsupported value: {value}")


def load_state() -> PokeControllerAppState:
    return PokeControllerAppState(
        theme=Variable[str](value="default"),

        # Camera Settings
        camera_id=Variable[str](value=""),
        camera_name=Variable[str](value=""),
        camera_fps=Variable[int](value=45),
        camera_size=Variable[str](value="640x360"),
        camera_show_realtime=Variable[bool](value=True),
        camera_show_matched=Variable[bool](value=False),
        camera_show_guide=Variable[bool](value=False),

        # Serial Settings
        serial_port=Variable[str](value="COM 1"),
        serial_baud_rate=Variable[int](value=9600),
        serial_data_format=Variable[str](value="Default"),
        serial_show_data=Variable[bool](value=False),

        # Manual Control Settings
        manual_control_enabled_keyboard=Variable[bool](value=False),
        manual_control_enabled_lstick_mouse=Variable[bool](value=False),
        manual_control_enabled_rstick_mouse=Variable[bool](value=False),
        manual_control_enabled_pro_controller=Variable[bool](value=False),
        manual_control_enabled_record_pro_controller=Variable[bool](value=False),

        # Command Settings
        command_python_commands_filter=Variable[str](value="-"),
        command_python_command=Variable[str](value=""),
        command_mcu_commands_filter=Variable[str](value="-"),
        command_mcu_command=Variable[str](value=""),
        command_shortcut_number=Variable[int](value=1),
        command_shortcuts=[
            Variable[str](value="", with_none=True),
            Variable[str](value="", with_none=True),
            Variable[str](value="", with_none=True),
            Variable[str](value="", with_none=True),
            Variable[str](value="", with_none=True),
            Variable[str](value="", with_none=True),
            Variable[str](value="", with_none=True),
            Variable[str](value="", with_none=True),
            Variable[str](value="", with_none=True),
            Variable[str](value="", with_none=True),
        ],

        # Notification Settings
        notification_enabled_notify_windows_when_command_started=Variable[bool](value=False),
        notification_enabled_notify_windows_when_command_ended=Variable[bool](value=False),
        notification_enabled_notify_discord_when_command_started=Variable[bool](value=False),
        notification_enabled_notify_discord_when_command_ended=Variable[bool](value=False),

        # Other Settings
        other_output_size=Variable[int](value=50),
        other_output_stdout=Variable[int](value=1),
        other_widget_visible_output1=Variable[bool](value=True),
        other_widget_visible_output2=Variable[bool](value=True),
        other_widget_visible_software_controller=Variable[bool](value=True),
        other_widget_software_controller_position=Variable[str](value="bottom"),
        other_widget_dialogue_confirm_buttons_position=Variable[str](value="bottom"),
    )


def save_state(state: PokeControllerAppState):
    pass
