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
    PapicoCommandResumeHandlerException,
)
from pokecontrollermodifiedextension.core.papico.handlers import PapicoHandler


class PapicoCommandResumeHandler(PapicoHandler):
    def handle(self, ctx: PapicoExecContext) -> PapicoResult[None]:
        if (params := ctx.params) is None:
            return PapicoFailure(
                ctx=ctx,
                error=PapicoCommandResumeHandlerException("params is required."),
            )
        if "command" not in params:
            return PapicoFailure(
                ctx=ctx,
                error=PapicoCommandResumeHandlerException("Command is required."),
            )

        command = params["command"]
        if issubclass(command.__class__, PythonCommand):
            command.isPause = False
            return PapicoSuccess(ctx=ctx, data=None)

        return PapicoFailure(
            ctx=ctx, error=PapicoCommandResumeHandlerException("Invalid command.")
        )
