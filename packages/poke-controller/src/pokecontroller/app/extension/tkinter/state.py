from typing import Callable, Literal
import tkinter as tk

from ...state import (
    DEFAULT_STATE,
    PokeControllerAppState,
    Variable as StateVariable,
)


class Variable[T](StateVariable[T]):
    def __init__(self, container: tk.Variable):
        super().__init__()
        self._container: tk.Variable = container

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


def load_state() -> PokeControllerAppState:
    # FIXME: load from state file
    raw_state = {}

    # Fill missing keys with default values
    for k in DEFAULT_STATE.keys():
        raw_state.setdefault(k, DEFAULT_STATE[k])

    kwargs = {}
    for k, v in raw_state.items():
        if v is None:
            kwargs[k] = Variable[str](tk.StringVar())
        elif isinstance(v, bool):
            kwargs[k] = Variable[bool](tk.BooleanVar(value=v))
        elif isinstance(v, int):
            kwargs[k] = Variable[int](tk.IntVar(value=v))
        elif isinstance(v, float):
            kwargs[k] = Variable[float](tk.DoubleVar(value=v))
        elif isinstance(v, str):
            kwargs[k] = Variable[str](tk.StringVar(value=v))
        elif isinstance(v, list):
            kwargs[k] = [Variable[str](tk.StringVar(value=item)) for item in v]

    return PokeControllerAppState(**kwargs)


def save_state(state: PokeControllerAppState):
    raw_state = {}
    for k in DEFAULT_STATE.keys():
        v = state.__dict__[k]
        if isinstance(v, Variable):
            raw_state[k] = v.get()
        elif isinstance(v, list):
            raw_state[k] = [item.get() for item in v]

    # FIXME: save to state file
    print(raw_state)
