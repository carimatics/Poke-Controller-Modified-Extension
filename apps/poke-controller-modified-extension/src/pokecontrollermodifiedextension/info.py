from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class AppInfo:
    name: str
    version: str
    latest_settings_version: str
    latest_api_version: str
