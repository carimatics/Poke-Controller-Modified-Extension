from pokecontrollermodifiedextension.api.v0_1_8.command.commands.mcu.base import (
    McuCommand,
)
from pokecontrollermodifiedextension.api.v0_1_8.command.commands.python.base import (
    PythonCommand,
)
from pokecontrollermodifiedextension.core.command.state import CommandState
from pokecontrollermodifiedextension.core.papico.context import (
    PapicoExecContext,
    PapicoFailure,
    PapicoResult,
    PapicoSuccess,
)
from pokecontrollermodifiedextension.core.papico.exception import (
    PapicoCommandGetStateHandlerException,
)
from pokecontrollermodifiedextension.core.papico.handlers import PapicoHandler


class PapicoCommandGetStateHandler(PapicoHandler):
    def handle(self, ctx: PapicoExecContext) -> PapicoResult[CommandState]:
        if (params := ctx.params) is None:
            return PapicoFailure(
                ctx=ctx,
                error=PapicoCommandGetStateHandlerException("params is required."),
            )
        if "command" not in params:
            return PapicoFailure(
                ctx=ctx,
                error=PapicoCommandGetStateHandlerException("Klass is required."),
            )

        command = params["command"]
        if isinstance(command, PythonCommand):
            state = CommandState(
                is_running=command.thread is not None,
                is_paused=command.isPause,
                is_alive=command.alive,
                is_cancelled=False,
                is_stopped=command.thread is None,
            )
        elif isinstance(command, McuCommand):
            state = CommandState(
                is_running=command.isRunning,
                is_paused=command.isPause,
                is_alive=command.isRunning,
                is_cancelled=False,
                is_stopped=not command.isRunning,
            )
        else:
            return PapicoFailure(
                ctx=ctx,
                error=PapicoCommandGetStateHandlerException(
                    f"Invalid command: {command}"
                ),
            )

        return PapicoSuccess(ctx=ctx, data=state)
