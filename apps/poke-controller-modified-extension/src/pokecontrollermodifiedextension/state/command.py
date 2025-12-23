import tkinter as tk

from pokecontrollermodifiedextension.exception import AppRuntimeException


class AppCommandState:
    def __init__(self) -> None:
        self._is_running = tk.BooleanVar(value=False)
        self._is_paused = tk.BooleanVar(value=False)
        self._is_alive = tk.BooleanVar(value=False)
        self._is_cancelled = tk.BooleanVar(value=False)
        self._is_stopped = tk.BooleanVar(value=True)

    @property
    def is_running(self) -> tk.BooleanVar:
        return self._is_running

    @property
    def is_paused(self) -> tk.BooleanVar:
        return self._is_paused

    @property
    def is_alive(self) -> tk.BooleanVar:
        return self._is_alive

    @property
    def is_cancelled(self) -> tk.BooleanVar:
        return self._is_cancelled

    @property
    def is_stopped(self) -> tk.BooleanVar:
        return self._is_stopped

    def start(self) -> None:
        self._is_running.set(True)
        self._is_paused.set(False)
        self._is_alive.set(True)
        self._is_cancelled.set(False)
        self._is_stopped.set(False)

    def stop(self) -> None:
        self._is_alive.set(False)
        self._is_stopped.set(True)

    def pause(self) -> None:
        self._is_paused.set(True)

    def resume(self) -> None:
        self._is_paused.set(False)

    def cancel(self) -> None:
        self._is_alive.set(False)
        self._is_cancelled.set(True)

    def finish(self) -> None:
        self._is_running.set(False)
        self._is_paused.set(False)
        self._is_alive.set(False)
        self._is_cancelled.set(False)
        self._is_stopped.set(True)


_app_command_state: AppCommandState | None = None


def setup_app_command_state() -> AppCommandState:
    global _app_command_state
    _app_command_state = AppCommandState()
    return _app_command_state


def get_app_command_state() -> AppCommandState:
    global _app_command_state
    if _app_command_state is None:
        raise AppRuntimeException("App command state is not initialized.")
    return _app_command_state
