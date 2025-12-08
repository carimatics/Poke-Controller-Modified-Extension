import re
from typing import Any


def substitute_nested(
    template: str,
    data: dict[str, Any],
) -> str:
    def replace_placeholder(match: re.Match[str]) -> str:
        path = match.group(1).split(".")
        current_data = data
        try:
            for key in path:
                current_data = current_data[key]
            return str(current_data)
        except (KeyError, TypeError):
            return match.group(0)

    return re.sub(r"\$\{(.+?)}", replace_placeholder, template)
