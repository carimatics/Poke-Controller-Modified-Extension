from dataclasses import dataclass
from pathlib import Path

from pokecontrollermodifiedextension.exception import AppRuntimeException


@dataclass(kw_only=True, frozen=True)
class AppRuntimeInfo:
    base_dir: Path
    profile: str


RUNTIME_INFO_SINGLETON: AppRuntimeInfo | None = None


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
