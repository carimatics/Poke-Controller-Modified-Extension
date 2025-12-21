from dataclasses import dataclass
from typing import Callable

from pokecontrollermodifiedextension.core.papico.context import PapicoContext
from pokecontrollermodifiedextension.core.papico.handlers.handler import PapicoHandler


@dataclass(frozen=True, kw_only=True)
class PapicoRegisterHandlerContext(PapicoContext):
    handler_generator: Callable[[], PapicoHandler]
