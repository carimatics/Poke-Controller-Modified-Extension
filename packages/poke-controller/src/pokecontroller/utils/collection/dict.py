from typing import Any


def deep_merge[T, U](
    original: dict[T, U],
    update: dict[T, U],
) -> dict[T, U]:
    def updater(d: Any, u: Any) -> None:
        if not isinstance(d, dict) or not isinstance(u, dict):
            raise RuntimeError()

        for k, v in u.items():
            if isinstance(v, dict):
                d.setdefault(k, {})
                updater(d[k], v)
            else:
                d[k] = v

    result: dict[T, U] = {}
    updater(result, original)
    updater(result, update)
    return result
