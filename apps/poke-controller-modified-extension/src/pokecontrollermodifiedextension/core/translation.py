from typing import Any

from pokecontrollermodifiedextension.singletons.app.translation import get_translation


def t(key: str, **kwargs: Any) -> str:
    translation = get_translation()
    return translation.get(key, **kwargs)
