from dataclasses import dataclass
from typing import Any, Callable

from .exception import PapicoException
from .handlers.handler import PapicoHandler


@dataclass(frozen=True, kw_only=True)
class PapicoContext:
    api_version: str
    domain: str
    operation: str


@dataclass(frozen=True, kw_only=True)
class PapicoRegisterHandlerContext(PapicoContext):
    handler_generator: Callable[[], PapicoHandler]


@dataclass(frozen=True, kw_only=True)
class PapicoExecContext(PapicoContext):
    args: tuple[Any, ...]
    kwargs: dict[str, Any]


@dataclass(frozen=True, kw_only=True)
class PapicoResult:
    success: bool
    api_version: str
    domain: str
    operation: str
    args: tuple[Any, ...]
    kwargs: dict[str, Any]
    data: Any | None = None
    error: PapicoException | None = None
