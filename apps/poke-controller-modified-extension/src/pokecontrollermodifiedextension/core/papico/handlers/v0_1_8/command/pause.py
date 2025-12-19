from pokecontrollermodifiedextension.api.v0_1_8.command.commands.python.base import (
    PythonCommand,
)
from pokecontrollermodifiedextension.core.papico.context import (
    PapicoExecContext,
    PapicoFailure,
    PapicoResult,
    PapicoSuccess,
)
from pokecontrollermodifiedextension.core.papico.exception import (
    PapicoCommandPauseHandlerException,
)
from pokecontrollermodifiedextension.core.papico.handlers import PapicoHandler


class PapicoCommandPauseHandler(PapicoHandler):
    def handle(self, ctx: PapicoExecContext) -> PapicoResult[None]:
        if (params := ctx.params) is None:
            return PapicoFailure(
                ctx=ctx,
                error=PapicoCommandPauseHandlerException("params is required."),
            )
        if "command" not in params:
            return PapicoFailure(
                ctx=ctx,
                error=PapicoCommandPauseHandlerException("Command is required."),
            )

        command = params["command"]
        if issubclass(command.__class__, PythonCommand):
            command.isPause = True
            return PapicoSuccess(ctx=ctx, data=None)

        return PapicoFailure(
            ctx=ctx, error=PapicoCommandPauseHandlerException("Invalid command.")
        )
