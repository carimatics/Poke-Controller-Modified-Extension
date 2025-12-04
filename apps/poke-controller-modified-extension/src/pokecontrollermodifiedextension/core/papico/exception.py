from ...exception import PokeControllerModifiedExtensionException
from .context import PapicoContext


class PapicoException(PokeControllerModifiedExtensionException):
    def __init__(self, message: str, ctx: PapicoContext):
        super().__init__(message)
        self.message = message
        self.ctx = ctx


class PapicoExecException(PapicoException):
    pass


class PapicoRegisterHandlerException(PapicoException):
    pass
