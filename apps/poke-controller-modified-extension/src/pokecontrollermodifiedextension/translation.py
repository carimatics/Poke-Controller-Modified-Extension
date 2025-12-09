from pathlib import Path
from typing import Any

from pokecontroller.core.translation import Translation

_translation: Translation | None = None


def setup_translation(base_dir: Path, language: str) -> None:
    global _translation
    _translation = Translation(base_dir, language)


class TranslationMeta(type):
    def __call__(cls, key: str, **kwargs: Any) -> str:
        if (translation := _translation) is None:
            raise RuntimeError("Translation is not initialized.")
        return translation.get(key, **kwargs)


class t(metaclass=TranslationMeta):
    @staticmethod
    def _get(key: str, **kwargs: Any) -> str:
        if (translation := _translation) is None:
            raise RuntimeError("Translation is not initialized.")
        return translation.get(key, **kwargs)

    @classmethod
    def w(cls, key: str, **kwargs: Any) -> str:
        return cls._get(f"gui.window.{key}", **kwargs)

    @classmethod
    def mw(cls, key: str, **kwargs: Any) -> str:
        return cls._get(f"gui.window.main.{key}", **kwargs)

    @classmethod
    def mwt(cls, key: str, **kwargs: Any) -> str:
        return cls._get(f"gui.window.main.tooltip.{key}", **kwargs)

    @classmethod
    def sw(cls, key: str, **kwargs: Any) -> str:
        return cls._get(f"gui.window.settings.{key}", **kwargs)
