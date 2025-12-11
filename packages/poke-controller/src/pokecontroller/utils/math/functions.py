from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _typeshed import SupportsRichComparison


def clamp[T: SupportsRichComparison](
    value: T,
    min_value: T,
    max_value: T,
) -> T:
    return max(min_value, min(value, max_value))
