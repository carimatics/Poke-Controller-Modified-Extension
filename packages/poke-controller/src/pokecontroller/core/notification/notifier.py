from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..image import RawImage


@dataclass(kw_only=True, frozen=True)
class RateLimit:
    key: str | None = None
    limit: str | None = None
    remaining: str | None = None
    reset_time: str | None = None
    image_limit: str | None = None
    image_remaining: str | None = None


class Notifier(ABC):
    @property
    @abstractmethod
    def keys(self) -> list[str]: ...

    @property
    @abstractmethod
    def has_error(self) -> bool: ...

    @abstractmethod
    def notify(
        self,
        message: str | None = None,
        image: RawImage | None = None,
        keys: list[str] | None = None,
    ) -> None: ...

    @abstractmethod
    def get_late_limits(self) -> list[RateLimit]: ...

    @abstractmethod
    def apply_config(self) -> None: ...
