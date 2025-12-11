import json
from pathlib import Path
from typing import Any


class Translation:
    def __init__(self, base_path: Path, language: str = "en") -> None:
        self._base_path = base_path
        self._language = language
        self._translations = self._load_translations()

    @property
    def filepath(self) -> str:
        return str(self._base_path / f"{self._language}.json")

    @property
    def language(self) -> str:
        return self._language

    def get(self, key: str, **kwargs: Any) -> str:
        ts: Any = self._translations
        for k in key.split("."):
            if k not in ts:
                break
            ts = ts[k]
        text = ts if isinstance(ts, str) else key
        return text.format_map(kwargs)

    def _load_translations(self) -> dict[str, Any]:
        trans_file = self._base_path / f"{self._language}.json"
        if not trans_file.exists():
            # fallback
            self._language = "en"
            trans_file = self._base_path / "en.json"
        with open(trans_file, "r", encoding="utf-8-sig") as f:
            return json.load(f)  # type: ignore[no-any-return]
