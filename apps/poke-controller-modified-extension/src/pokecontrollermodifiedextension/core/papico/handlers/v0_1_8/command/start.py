from threading import Thread

from pokecontrollermodifiedextension.api.v0_1_8.camera import Camera
from pokecontrollermodifiedextension.api.v0_1_8.command.commands.mcu.base import (
    McuCommand,
)
from pokecontrollermodifiedextension.api.v0_1_8.command.commands.python.base import (
    PythonCommand,
)
from pokecontrollermodifiedextension.api.v0_1_8.command.commands.python.image_processing import ImageProcPythonCommand
from pokecontrollermodifiedextension.api.v0_1_8.command.sender import Sender
from pokecontrollermodifiedextension.core.command import CommandInfo
from pokecontrollermodifiedextension.core.papico.context import (
    PapicoExecContext,
    PapicoFailure,
    PapicoResult,
    PapicoSuccess,
)
from pokecontrollermodifiedextension.core.papico.exception import (
    PapicoCommandStartHandlerException,
)
from pokecontrollermodifiedextension.core.papico.handlers import PapicoHandler
from pokecontrollermodifiedextension.settings import get_app_settings


class PapicoCommandStartHandler(PapicoHandler):
    def handle(
        self, ctx: PapicoExecContext
    ) -> PapicoResult[tuple[PythonCommand | McuCommand, Thread | None]]:
        if (params := ctx.params) is None:
            return PapicoFailure(
                ctx=ctx, error=PapicoCommandStartHandlerException("params is required.")
            )
        if "info" not in params:
            return PapicoFailure(
                ctx=ctx, error=PapicoCommandStartHandlerException("info is required.")
            )

        info = params["info"]
        if not isinstance(info, CommandInfo):
            return PapicoFailure(
                ctx=ctx,
                error=PapicoCommandStartHandlerException("info must be CommandInfo."),
            )

        app_settings = get_app_settings()

        klass = info.klass
        if issubclass(klass, ImageProcPythonCommand):
            camera = Camera(app_settings.capture.fps.get())
            post_process = params.get("post_process", None)
            sender = Sender(app_settings.serial.show_data)
            python_command = klass(cam=camera)
            python_command.start(ser=sender, postProcess=post_process)
            return PapicoSuccess(
                ctx=ctx,
                data=(python_command, python_command.thread),
            )
        if issubclass(klass, PythonCommand):
            post_process = params.get("post_process", None)
            sender = Sender(app_settings.serial.show_data)
            python_command = klass()
            python_command.start(ser=sender, postProcess=post_process)
            return PapicoSuccess(
                ctx=ctx,
                data=(python_command, python_command.thread),
            )
        if issubclass(klass, McuCommand):
            if "sync_name" not in params:
                return PapicoFailure(
                    ctx=ctx,
                    error=PapicoCommandStartHandlerException("sync_name is required."),
                )
            sync_name = params["sync_name"]
            post_process = params.get("post_process", None)
            sender = Sender(app_settings.serial.show_data)
            mcu_command = klass(sync_name=sync_name)
            mcu_command.start(ser=sender, postProcess=post_process)
            return PapicoSuccess(ctx=ctx, data=(mcu_command, None))

        return PapicoFailure(
            ctx=ctx, error=PapicoCommandStartHandlerException("Invalid command class.")
        )
