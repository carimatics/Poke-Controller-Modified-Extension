from typing import Any

from pokecontrollerext.singletons.app.translation import get_translation


def t(key: str, **kwargs: Any) -> str:
    translation = get_translation()
    return translation.get(key, **kwargs)
