from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class CommandState:
    is_running: bool
    is_paused: bool
    is_alive: bool
    is_cancelled: bool
    is_stopped: bool
