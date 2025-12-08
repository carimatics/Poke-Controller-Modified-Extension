from ...exception import PokeControllerModifiedExtensionException


class PapicoException(PokeControllerModifiedExtensionException):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class PapicoExecException(PapicoException):
    pass


class PapicoRegisterHandlerException(PapicoException):
    pass


class PapicoGuiStateLoadHandlerException(PapicoExecException):
    pass


class PapicoSettingsLoadHandlerException(PapicoExecException):
    pass

class PapicoSettingsSaveHandlerException(PapicoExecException):
    pass
