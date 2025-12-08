from dataclasses import dataclass
from typing import Any

from .exception import PapicoException


@dataclass(frozen=True, kw_only=True)
class PapicoContext:
    api_version: str
    domain: str
    operation: str


@dataclass(frozen=True, kw_only=True)
class PapicoExecContext(PapicoContext):
    params: dict[str, Any]


@dataclass(frozen=True, kw_only=True)
class PapicoResult[R]:
    success: bool
    ctx: PapicoExecContext
    data: R | None = None
    error: PapicoException | None = None
