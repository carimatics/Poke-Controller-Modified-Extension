from dataclasses import dataclass
from types import ModuleType
from typing import Literal


@dataclass(kw_only=True, frozen=True)
class CommandInfo[T]:
    name: str
    display_name: str
    tags: list[str]
    module: ModuleType
    klass: type[T]
    api_version: str
    kind: Literal["python", "mcu"]


_running_command_info: CommandInfo | None = None
_selected_command_info: CommandInfo | None = None


def get_running_command_info() -> CommandInfo | None:
    global _running_command_info
    return _running_command_info


def set_running_command_info(command_info: CommandInfo) -> None:
    global _running_command_info
    _running_command_info = command_info


def clear_running_command_info() -> None:
    global _running_command_info
    _running_command_info = None


def get_selected_command_info() -> CommandInfo | None:
    global _selected_command_info
    return _selected_command_info


def set_selected_command_info(command_info: CommandInfo) -> None:
    global _selected_command_info
    _selected_command_info = command_info
