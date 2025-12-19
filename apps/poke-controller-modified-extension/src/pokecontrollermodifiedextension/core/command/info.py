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


_current_command_info: CommandInfo | None = None


def get_current_command_info() -> CommandInfo | None:
    global _current_command_info
    return _current_command_info


def set_current_command_info(command_info: CommandInfo) -> None:
    global _current_command_info
    _current_command_info = command_info


def clear_current_command_info() -> None:
    global _current_command_info
    _current_command_info = None
