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
