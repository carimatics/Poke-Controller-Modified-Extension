from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class AppInfo:
    name: str
    version: str
