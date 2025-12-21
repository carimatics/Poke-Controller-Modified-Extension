from dataclasses import dataclass
from pathlib import Path


@dataclass(kw_only=True, frozen=True)
class AppInfo:
    name: str
    version: str
    latest_settings_version: str
    latest_api_version: str
    application_root: Path


_app_info = AppInfo(
    name="Poke-Controller Modified Extension",
    version="0.2.0",
    latest_settings_version="0.2.0",
    latest_api_version="0.2.0",
    application_root=Path(__file__).parent.parent.parent.parent,
)


def get_app_info() -> AppInfo:
    global _app_info
    return _app_info
