from pokecontrollermodifiedextension.api.v0_1_8.command.commands.mcu.base import (
    McuCommand,
)
from pokecontrollermodifiedextension.api.v0_1_8.command.commands.python.base import (
    PythonCommand,
    StopThread,
)
from pokecontrollermodifiedextension.api.v0_1_8.command.sender import Sender
from pokecontrollermodifiedextension.core.papico.context import (
    PapicoExecContext,
    PapicoFailure,
    PapicoResult,
    PapicoSuccess,
)
from pokecontrollermodifiedextension.core.papico.exception import (
    PapicoCommandStopHandlerException,
)
from pokecontrollermodifiedextension.core.papico.handlers import PapicoHandler
from pokecontrollermodifiedextension.settings import get_app_settings


class PapicoCommandStopHandler(PapicoHandler):
    def handle(self, ctx: PapicoExecContext) -> PapicoResult[None]:
        if (params := ctx.params) is None:
            return PapicoFailure(
                ctx=ctx,
                error=PapicoCommandStopHandlerException("params is required."),
            )
        if "command" not in params:
            return PapicoFailure(
                ctx=ctx,
                error=PapicoCommandStopHandlerException("Command is required."),
            )

        app_settings = get_app_settings()

        command = params["command"]
        if issubclass(command, PythonCommand):
            sender = Sender(app_settings.serial.show_data)
            try:
                command.end(ser=sender)
            except StopThread:
                pass
            return PapicoSuccess(ctx=ctx, data=None)
        if issubclass(command, McuCommand):
            sender = Sender(app_settings.serial.show_data)
            command.end(ser=sender)
            return PapicoSuccess(ctx=ctx, data=None)

        return PapicoFailure(
            ctx=ctx, error=PapicoCommandStopHandlerException("Invalid command.")
        )
