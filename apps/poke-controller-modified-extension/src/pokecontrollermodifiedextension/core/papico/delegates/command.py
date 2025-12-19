import logging
import threading
from typing import Any, Callable

from pokecontrollermodifiedextension.core.command import CommandInfo
from pokecontrollermodifiedextension.core.command.state import CommandState
from pokecontrollermodifiedextension.core.papico.context import (
    PapicoExecContext,
    PapicoFailure,
    PapicoResult,
    PapicoSuccess,
)
from pokecontrollermodifiedextension.core.papico.exception import (
    PapicoCommandGetStateHandlerException,
    PapicoCommandLoadHandlerException,
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
        self._handler_generators = handler_generators
        self._latest_api_version = latest_api_version
        self._domain = "command"
        self._app_runtime_info = get_app_runtime_info()

        self._current_command_info: CommandInfo | None = None
        self._current_command: Any | None = None
        self._current_thread: threading.Thread | None = None

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
                    error=PapicoCommandLoadHandlerException(f"{e}"),
                )
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

    def get_state(self) -> PapicoResult[CommandState]:
        operation = "get_state"
        if (command := self._current_command) is None:
            return PapicoFailure(
                ctx=self._create_context(
                    api_version=self._latest_api_version,
                    operation=operation,
                ),
                error=PapicoCommandGetStateHandlerException("Command is not running."),
            )

        if (command_info := self._current_command_info) is None:
            return PapicoFailure(
                ctx=self._create_context(
                    api_version=self._latest_api_version,
                    operation=operation,
                ),
                error=PapicoCommandGetStateHandlerException(
                    "Command info is not loaded yet."
                ),
            )

        api_version = command_info.api_version
        ctx = self._create_context(
            api_version=api_version,
            operation=operation,
            params={"command": command},
        )
        handler = self._get_handler(ctx)
        return handler.handle(ctx)

    def start(
        self,
        command_info: CommandInfo,
        *,
        post_process: Callable[[], None] | None = None,
        sync_name: str | None = None,
    ) -> PapicoResult[None]:
        operation = "start"
        state = self.get_state()
        if state.success:
            if state.data.is_running:
                return PapicoFailure(
                    ctx=self._create_context(
                        api_version=self._latest_api_version,
                        operation="start",
                    ),
                    error=PapicoCommandGetStateHandlerException("Command is running."),
                )

        initialize_result = self.initialize()
        if not initialize_result.success:
            return initialize_result

        self._current_command_info = command_info
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
        return handler.handle(ctx)

    def stop(self) -> PapicoResult[None]:
        operation = "stop"
        if (command := self._current_command) is None:
            return PapicoFailure(
                ctx=self._create_context(
                    api_version=self._latest_api_version,
                    operation=operation,
                ),
                error=PapicoCommandGetStateHandlerException("Command is not running."),
            )

        if (command_info := self._current_command_info) is None:
            return PapicoFailure(
                ctx=self._create_context(
                    api_version=self._latest_api_version,
                    operation=operation,
                ),
                error=PapicoCommandGetStateHandlerException("Command info is not set."),
            )

        ctx = self._create_context(
            api_version=command_info.api_version,
            operation=operation,
            params={"command": command},
        )
        handler = self._get_handler(ctx=ctx)
        result = handler.handle(ctx)
        if result.success:
            self._current_command_info = None
            self._current_command = None
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
