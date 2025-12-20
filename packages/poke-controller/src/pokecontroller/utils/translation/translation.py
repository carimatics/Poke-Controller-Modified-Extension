import json
from pathlib import Path
from typing import Any


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

    @property
    def filepath(self) -> Path:
        return self._base_path / f"{self._platform}.{self._language}.json"

    @property
    def language(self) -> str:
        return self._language

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
        if not self.filepath.exists():
            # fallback
            self._language = "en"
            self._translations = "windows"
        with open(self.filepath, "r", encoding="utf-8-sig") as f:
            return json.load(f)  # type: ignore[no-any-return]
