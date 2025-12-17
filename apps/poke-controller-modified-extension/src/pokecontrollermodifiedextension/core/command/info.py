from dataclasses import dataclass
from typing import Literal


@dataclass(kw_only=True, frozen=True)
class CommandInfo[T]:
    name: str
    klass: type[T]
    api_version: str
    kind: Literal["python", "mcu"]
