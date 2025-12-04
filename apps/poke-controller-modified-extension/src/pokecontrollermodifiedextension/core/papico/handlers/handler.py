from abc import ABC, abstractmethod

from ..context import PapicoExecContext, PapicoResult


class PapicoHandler(ABC):
    @abstractmethod
    def handle(self, ctx: PapicoExecContext) -> PapicoResult: ...
