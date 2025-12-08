from dataclasses import dataclass
from typing import Callable

from ..context import PapicoContext
from .handler import PapicoHandler


@dataclass(frozen=True, kw_only=True)
class PapicoRegisterHandlerContext(PapicoContext):
    handler_generator: Callable[[], PapicoHandler]
