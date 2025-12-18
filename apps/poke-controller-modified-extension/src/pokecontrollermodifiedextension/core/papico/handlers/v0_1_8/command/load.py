from pathlib import Path

from pokecontroller.core.dynamic import DynamicClassLoader

from ......api.v0_1_8.command.commands.mcu.base import McuCommand
from ......api.v0_1_8.command.commands.python.base import PythonCommand
from ......runtime_info import get_app_runtime_info
from .....command.info import CommandInfo
from ....context import PapicoExecContext, PapicoFailure, PapicoResult, PapicoSuccess
from ....exception import PapicoCommandLoadHandlerException
from ...handler import PapicoHandler


class PapicoCommandLoadHandler(PapicoHandler):
    _base_dir: Path
    _commands: list[CommandInfo]

    def handle(self, ctx: PapicoExecContext) -> PapicoResult[list[CommandInfo]]:
        try:
            app_runtime_info = get_app_runtime_info()
            self._base_dir = app_runtime_info.base_dir / "Commands"
            self._commands: list[CommandInfo] = []
            self._load_python_commands()
            self._load_mcu_commands()
            return PapicoSuccess(ctx=ctx, data=self._commands)
        except Exception as e:
            return PapicoFailure(
                ctx=ctx,
                error=PapicoCommandLoadHandlerException(f"{e}"),
            )

    def _load_python_commands(self) -> None:
        python_commands_path = self._base_dir / "PythonCommands"
        for module, name, klass in DynamicClassLoader[PythonCommand](
            base_dir=python_commands_path,
            klass=PythonCommand,  # type: ignore[type-abstract]
        ).load():
            self._commands.append(
                CommandInfo(
                    name=name,
                    module=module,
                    klass=klass,
                    api_version="0.1.8",
                    kind="python",
                )
            )

    def _load_mcu_commands(self) -> None:
        mcu_commands_path = self._base_dir / "McuCommands"
        for module, name, klass in DynamicClassLoader[McuCommand](
            base_dir=mcu_commands_path,
            klass=McuCommand,  # type: ignore[type-abstract]
        ).load():
            self._commands.append(
                CommandInfo(
                    name=name,
                    module=module,
                    klass=klass,
                    api_version="0.1.8",
                    kind="mcu",
                )
            )
