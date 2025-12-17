import logging
from pathlib import Path
from typing import Callable

from ...runtime_info import get_app_runtime_info
from ...settings import AppSettings
from ..command import CommandInfo
from ..command.state import CommandState
from .context import PapicoResult
from .delegates.command import PapicoCommandDelegate
from .delegates.settings import PapicoSettingsDelegate
from .handlers import PapicoRegisterHandlerContext
from .types import PapicoContainer, PapicoHandlerGenerator

LATEST_API_VERSION = "0.2.0"

logger = logging.getLogger(__name__)


class Papico:
    """Poke-Controller Public API Compatible Orchestrator

    Poke-Controllerの公開APIのバージョンによって異なる処理を適切に振り分けるクラス
    """

    _settings_path: Path

    def __init__(self) -> None:
        self._runtime_info = get_app_runtime_info()
        self._handler_generators: PapicoContainer[PapicoHandlerGenerator] = {}

        self._settings_delegate = PapicoSettingsDelegate(
            latest_api_version=LATEST_API_VERSION,
            handler_generators=self._handler_generators,
        )
        self._command_delegate = PapicoCommandDelegate(
            latest_api_version=LATEST_API_VERSION,
            handler_generators=self._handler_generators,
        )

    @property
    def settings_path(self) -> Path:
        return self._settings_delegate.settings_path

    def register_handler(self, ctx: PapicoRegisterHandlerContext) -> None:
        self._handler_generators.setdefault(
            ctx.api_version,
            {},
        ).setdefault(
            ctx.domain,
            {},
        )[ctx.operation] = ctx.handler_generator

    def load_settings(self) -> PapicoResult[AppSettings]:
        return self._settings_delegate.load()

    def reload_settings(self) -> PapicoResult[AppSettings]:
        return self._settings_delegate.reload()

    def save_settings(self) -> PapicoResult[None]:
        return self._settings_delegate.save()

    def initialize_command(self) -> PapicoResult[None]:
        return self._command_delegate.initialize()

    def load_commands(self) -> PapicoResult[list[CommandInfo]]:
        return self._command_delegate.load()

    def get_command_state(self) -> PapicoResult[CommandState]:
        return self._command_delegate.get_state()

    def start_command(
        self,
        command_info: CommandInfo,
        *,
        post_process: Callable[[], None] | None = None,
        sync_name: str | None = None,
    ) -> PapicoResult[None]:
        return self._command_delegate.start(
            command_info,
            post_process=post_process,
            sync_name=sync_name,
        )

    def stop_command(self) -> PapicoResult[None]:
        return self._command_delegate.stop()


PAPICO_SINGLETON: Papico | None = None


def setup_papico() -> Papico:
    global PAPICO_SINGLETON
    PAPICO_SINGLETON = Papico()
    return PAPICO_SINGLETON


def get_papico() -> Papico:
    global PAPICO_SINGLETON
    if PAPICO_SINGLETON is None:
        raise RuntimeError("Papico is not initialized.")
    return PAPICO_SINGLETON
