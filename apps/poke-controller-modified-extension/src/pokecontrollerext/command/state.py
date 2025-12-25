import tkinter as tk

from pokecontrollerext.command.info import CommandInfo


class AppCommandState:
    def __init__(self) -> None:
        self._is_running = tk.BooleanVar(value=False)
        self._is_paused = tk.BooleanVar(value=False)
        self._is_alive = tk.BooleanVar(value=False)
        self._is_cancelled = tk.BooleanVar(value=False)
        self._is_stopped = tk.BooleanVar(value=True)
        self._running_command_info: CommandInfo | None = None
        self._selected_command_info: CommandInfo | None = None

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

    @property
    def running_command_info(self) -> CommandInfo | None:
        return self._running_command_info

    @property
    def selected_command_info(self) -> CommandInfo | None:
        return self._selected_command_info

    def select(self, info: CommandInfo) -> None:
        self._selected_command_info = info

    def start(self, info: CommandInfo | None = None) -> None:
        self._is_running.set(True)
        self._is_paused.set(False)
        self._is_alive.set(True)
        self._is_cancelled.set(False)
        self._is_stopped.set(False)

        if info is not None:
            self._running_command_info = info

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

        self._running_command_info = None
