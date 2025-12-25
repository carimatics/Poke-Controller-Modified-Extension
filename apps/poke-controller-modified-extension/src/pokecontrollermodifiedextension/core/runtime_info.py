from dataclasses import dataclass
from pathlib import Path


@dataclass(kw_only=True, frozen=True)
class AppRuntimeInfo:
    base_dir: Path
    profile: str
