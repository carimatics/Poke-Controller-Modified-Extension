import logging
from typing import Any, Callable

from pokecontrollermodifiedextension.core.command import CommandInfo
from pokecontrollermodifiedextension.core.command.info import (
    clear_current_command_info,
    get_current_command_info,
    set_current_command_info,
)
from pokecontrollermodifiedextension.core.command.state import get_app_command_state
from pokecontrollermodifiedextension.core.papico.context import (
    PapicoExecContext,
    PapicoFailure,
    PapicoResult,
    PapicoSuccess,
)
from pokecontrollermodifiedextension.core.papico.exception import (
    PapicoCommandInitializeHandlerException,
    PapicoCommandLoadHandlerException,
    PapicoCommandPauseHandlerException,
    PapicoCommandResumeHandlerException,
    PapicoCommandStartHandlerException,
    PapicoCommandStopHandlerException,
)
from pokecontrollermodifiedextension.core.papico.handlers.handler import PapicoHandler
from pokecontrollermodifiedextension.core.papico.types import (
    PapicoContainer,
    PapicoHandlerGenerator,
)
from pokecontrollermodifiedextension.runtime_info import get_app_runtime_info

logger = logging.getLogger(__name__)


class PapicoCommandDelegate:
    def __init__(
        self,
        latest_api_version: str,
        handler_generators: PapicoContainer[PapicoHandlerGenerator],
    ) -> None:
        self._initialized = False

        self._handler_generators = handler_generators
        self._latest_api_version = latest_api_version
        self._domain = "command"
        self._app_runtime_info = get_app_runtime_info()

        self._current_command: Any | None = None

        self._api_versions = ("0.1.8",)

    def initialize(self) -> PapicoResult[None]:
        operation = "initialize"

        for api_version in self._api_versions:
            ctx = self._create_context(
                api_version=api_version,
                operation=operation,
            )
            try:
                handler = self._get_handler(ctx=ctx)
                handler.handle(ctx)
            except KeyError:
                continue
            except Exception as e:
                return PapicoFailure(
                    ctx=self._create_context(
                        api_version=api_version,
                        operation=operation,
                    ),
                    error=PapicoCommandInitializeHandlerException(f"{e}"),
                )

        if not self._initialized:
            self._register_traces()
            self._initialized = True

        return PapicoSuccess(
            ctx=self._create_context(
                api_version=self._latest_api_version,
                operation=operation,
            ),
            data=None,
        )

    def load(self) -> PapicoResult[list[CommandInfo]]:
        operation = "load"
        result_data: list[CommandInfo] = []
        for api_version in self._api_versions:
            ctx = self._create_context(
                api_version=api_version,
                operation=operation,
            )
            handler = self._get_handler(ctx)
            try:
                result = handler.handle(ctx)
                if not result.success:
                    return result
            except Exception as e:
                logger.warning(f"Failed to load commands: {e}")
                return PapicoFailure(
                    ctx=self._create_context(
                        api_version=api_version,
                        operation=operation,
                    ),
                    error=PapicoCommandLoadHandlerException(f"{e}"),
                )
            result_data.extend(result.data)
        return PapicoSuccess(
            ctx=self._create_context(
                api_version=self._latest_api_version,
                operation=operation,
            ),
            data=result_data,
        )

    def start(
        self,
        command_info: CommandInfo,
        *,
        post_process: Callable[[], None] | None = None,
        sync_name: str | None = None,
    ) -> PapicoResult[None]:
        operation = "start"

        initialize_result = self.initialize()
        if not initialize_result.success:
            return PapicoFailure(
                ctx=self._create_context(
                    api_version=self._latest_api_version,
                    operation=operation,
                ),
                error=initialize_result.error,
            )

        command_state = get_app_command_state()
        if command_state.is_running.get():
            return PapicoFailure(
                ctx=self._create_context(
                    api_version=self._latest_api_version,
                    operation="start",
                ),
                error=PapicoCommandStartHandlerException("Command is running."),
            )

        set_current_command_info(command_info)
        params: dict[str, Any] = {
            "info": command_info,
        }
        if sync_name is not None:
            params["sync_name"] = sync_name
        if post_process is not None:
            params["post_process"] = post_process

        ctx = self._create_context(
            api_version=command_info.api_version,
            operation=operation,
            params=params,
        )
        handler = self._get_handler(ctx=ctx)
        result = handler.handle(ctx)
        if result.success:
            self._current_command = result.data[0]
        return result

    def stop(self) -> PapicoResult[None]:
        operation = "stop"

        command_state = get_app_command_state()
        if not command_state.is_running.get():
            return PapicoSuccess(
                ctx=self._create_context(
                    api_version=self._latest_api_version,
                    operation=operation,
                ),
                data=None,
            )

        if (command := self._current_command) is None:
            return PapicoFailure(
                ctx=self._create_context(
                    api_version=self._latest_api_version,
                    operation=operation,
                ),
                error=PapicoCommandStopHandlerException("Command is not running."),
            )

        if (command_info := get_current_command_info()) is None:
            return PapicoFailure(
                ctx=self._create_context(
                    api_version=self._latest_api_version,
                    operation=operation,
                ),
                error=PapicoCommandStopHandlerException("Command info is not set."),
            )

        ctx = self._create_context(
            api_version=command_info.api_version,
            operation=operation,
            params={"command": command},
        )
        handler = self._get_handler(ctx=ctx)
        result = handler.handle(ctx)
        return result

    def pause(self) -> PapicoResult[None]:
        operation = "pause"

        command_state = get_app_command_state()
        if not command_state.is_running.get():
            return PapicoSuccess(
                ctx=self._create_context(
                    api_version=self._latest_api_version,
                    operation=operation,
                ),
                data=None,
            )

        if (command := self._current_command) is None:
            return PapicoFailure(
                ctx=self._create_context(
                    api_version=self._latest_api_version,
                    operation=operation,
                ),
                error=PapicoCommandPauseHandlerException("Command is not running."),
            )

        if (command_info := get_current_command_info()) is None:
            return PapicoFailure(
                ctx=self._create_context(
                    api_version=self._latest_api_version,
                    operation=operation,
                ),
                error=PapicoCommandPauseHandlerException("Command info is not set."),
            )

        ctx = self._create_context(
            api_version=command_info.api_version,
            operation=operation,
            params={"command": command},
        )
        handler = self._get_handler(ctx=ctx)
        result = handler.handle(ctx)
        return result

    def resume(self) -> PapicoResult[None]:
        operation = "resume"

        command_state = get_app_command_state()
        if not command_state.is_paused.get():
            return PapicoSuccess(
                ctx=self._create_context(
                    api_version=self._latest_api_version,
                    operation=operation,
                ),
                data=None,
            )

        if (command := self._current_command) is None:
            return PapicoFailure(
                ctx=self._create_context(
                    api_version=self._latest_api_version,
                    operation=operation,
                ),
                error=PapicoCommandResumeHandlerException("Command is not running."),
            )

        if (command_info := get_current_command_info()) is None:
            return PapicoFailure(
                ctx=self._create_context(
                    api_version=self._latest_api_version,
                    operation=operation,
                ),
                error=PapicoCommandResumeHandlerException("Command info is not set."),
            )

        ctx = self._create_context(
            api_version=command_info.api_version,
            operation=operation,
            params={"command": command},
        )
        handler = self._get_handler(ctx=ctx)
        result = handler.handle(ctx)
        return result

    def _create_context(
        self,
        api_version: str,
        operation: str,
        params: dict[str, Any] | None = None,
    ) -> PapicoExecContext:
        return PapicoExecContext(
            api_version=api_version,
            domain=self._domain,
            operation=operation,
            params=params,
        )

    def _get_handler(self, ctx: PapicoExecContext) -> PapicoHandler:
        return self._handler_generators[ctx.api_version][ctx.domain][ctx.operation]()

    def _on_stopped_changed(self, *_: str) -> None:
        command_state = get_app_command_state()
        if command_state.is_stopped.get():
            self._current_command = None
            clear_current_command_info()

    def _register_traces(self) -> None:
        command_state = get_app_command_state()
        command_state.is_stopped.trace_add("write", self._on_stopped_changed)
