from pathlib import Path
from typing import Any

from pokecontroller.utils import platform
from pokecontroller.utils.translation import Translation

_translation: Translation | None = None


def setup_translation(base_dir: Path, language: str) -> None:
    global _translation
    _translation = Translation(base_dir, platform.get_name(), language)


def t(key: str, **kwargs: Any) -> str:
    global _translation
    if (translation := _translation) is None:
        raise RuntimeError("Translation is not initialized.")
    return translation.get(key, **kwargs)
