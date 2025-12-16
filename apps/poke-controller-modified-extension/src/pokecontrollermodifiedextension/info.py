from dataclasses import dataclass
from pathlib import Path

from .exception import AppRuntimeException


@dataclass(kw_only=True, frozen=True)
class AppInfo:
    name: str
    version: str
    latest_settings_version: str
    latest_api_version: str
    application_root: Path


@dataclass(kw_only=True, frozen=True)
class AppRuntimeInfo:
    base_dir: Path
    profile: str


APP_INFO_SINGLETON = AppInfo(
    name="Poke-Controller Modified Extension",
    version="0.2.0",
    latest_settings_version="0.2.0",
    latest_api_version="0.2.0",
    application_root=Path(__file__).parent.parent.parent,
)

RUNTIME_INFO_SINGLETON: AppRuntimeInfo | None = None


def get_app_info() -> AppInfo:
    global APP_INFO_SINGLETON
    return APP_INFO_SINGLETON


def get_app_runtime_info() -> AppRuntimeInfo:
    global RUNTIME_INFO_SINGLETON
    if RUNTIME_INFO_SINGLETON is None:
        raise AppRuntimeException("App runtime info is not initialized.")
    return RUNTIME_INFO_SINGLETON


def setup_runtime_info(base_dir: Path, profile: str) -> AppRuntimeInfo:
    global RUNTIME_INFO_SINGLETON
    RUNTIME_INFO_SINGLETON = AppRuntimeInfo(
        base_dir=base_dir,
        profile=profile,
    )
    return RUNTIME_INFO_SINGLETON
