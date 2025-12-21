import json
from pathlib import Path
from typing import Any

from pokecontroller.utils.collection.dict import deep_merge


class Translation:
    def __init__(
        self,
        base_path: Path,
        platform: str = "windows",
        language: str = "en",
    ) -> None:
        self._base_path = base_path
        self._platform = platform
        self._language = language
        self._translations = self._load_translations()

    def get(self, key: str, **kwargs: Any) -> str:
        ts: Any = self._translations
        for k in key.split("."):
            if k not in ts:
                break
            ts = ts[k]
        if isinstance(ts, dict):
            if "text" not in ts:
                return key
            if not isinstance(txt := ts["text"], str):
                return key
            text = txt
        elif isinstance(ts, str):
            text = ts
        else:
            return key
        return text.format_map(kwargs)

    def _load_translations(self) -> dict[str, Any]:
        base_file = self._base_path / f"{self._language}.json"

        with open(base_file, "r", encoding="utf-8-sig") as f:
            base = json.load(f)

        platform_file = self._base_path / f"{self._language}.{self._platform}.json"
        if not platform_file.exists():
            return base  # type: ignore[no-any-return]

        with open(platform_file, "r", encoding="utf-8-sig") as f:
            platform = json.load(f)

        return deep_merge(base, platform)
