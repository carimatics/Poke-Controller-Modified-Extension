from pokecontrollerext.app.exception import AppException


class PapicoException(AppException):
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


class PapicoCommandInitializeHandlerException(PapicoExecException):
    pass


class PapicoCommandLoadHandlerException(PapicoExecException):
    pass


class PapicoCommandStartHandlerException(PapicoExecException):
    pass


class PapicoCommandStopHandlerException(PapicoExecException):
    pass


class PapicoCommandPauseHandlerException(PapicoExecException):
    pass


class PapicoCommandResumeHandlerException(PapicoExecException):
    pass


class PapicoExternalToolsInitializeHandlerException(PapicoExecException):
    pass
