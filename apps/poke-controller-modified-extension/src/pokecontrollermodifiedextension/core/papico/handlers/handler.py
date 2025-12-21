from abc import ABC, abstractmethod

from pokecontrollermodifiedextension.core.papico.context import (
    PapicoExecContext,
    PapicoResult,
)


class PapicoHandler[R](ABC):
    @abstractmethod
    def handle(self, ctx: PapicoExecContext) -> PapicoResult[R]: ...
