from dataclasses import dataclass
from typing import Callable

from pokecontrollermodifiedextension.papico.context import PapicoContext
from pokecontrollermodifiedextension.papico.handlers.handler import PapicoHandler


@dataclass(frozen=True, kw_only=True)
class PapicoRegisterHandlerContext(PapicoContext):
    handler_generator: Callable[[], PapicoHandler]
