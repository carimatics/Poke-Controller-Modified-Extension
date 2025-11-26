from dataclasses import dataclass


@dataclass(frozen=True)
class PokeControllerAppInfo:
    name: str
