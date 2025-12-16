import logging
from pathlib import Path
from typing import Callable

from ...info import get_app_runtime_info
from ...settings import (
    AppSettings,
    get_app_settings,
    get_app_settings_or_none,
    setup_app_settings,
)
from .context import PapicoExecContext, PapicoFailure, PapicoResult, PapicoSuccess
from .exception import PapicoExecException
from .handlers import PapicoHandler, PapicoRegisterHandlerContext

type PapicoContainer[T] = dict[str, dict[str, dict[str, T]]]
PapicoHandlerGenerator = Callable[[], PapicoHandler]

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
        self._current_handler: PapicoHandler | None = None

    @property
    def _base_dir(self) -> Path:
        return self._runtime_info.base_dir

    @property
    def _profile(self) -> str:
        return self._runtime_info.profile

    @property
    def settings_path(self) -> Path:
        return self._settings_path

    def register_handler(self, ctx: PapicoRegisterHandlerContext) -> None:
        self._handler_generators.setdefault(
            ctx.api_version,
            {},
        ).setdefault(
            ctx.domain,
            {},
        )[ctx.operation] = ctx.handler_generator

    def load_settings(self) -> PapicoResult[AppSettings]:
        if (settings := get_app_settings_or_none()) is not None:
            return PapicoSuccess(
                ctx=PapicoExecContext(
                    api_version=settings.general.version.get(),
                    domain="settings",
                    operation="load",
                ),
                data=settings,
            )

        path_v0_2 = (
            self._runtime_info.base_dir
            / "profiles"
            / self._runtime_info.profile
            / "settings.json"
        )
        path_v0_1 = (
            self._runtime_info.base_dir
            / "profiles"
            / self._runtime_info.profile
            / "settings.ini"
        )
        if path_v0_2.exists() and path_v0_2.is_file():
            logger.info(f"Loading settings from {path_v0_2}")
            result = self._exec(
                PapicoExecContext(
                    api_version="0.2.0",
                    domain="settings",
                    operation="load",
                    params={"path": str(path_v0_2)},
                )
            )
            self._settings_path = path_v0_2
        elif path_v0_1.exists() and path_v0_1.is_file():
            logger.info(f"Loading settings from {path_v0_1}")
            result = self._exec(
                PapicoExecContext(
                    api_version="0.1.8",
                    domain="settings",
                    operation="load",
                    params={"path": str(path_v0_1)},
                )
            )
            self._settings_path = path_v0_1
        else:
            logger.info("Loading default settings from the latest version")
            result = self._exec(
                PapicoExecContext(
                    api_version=LATEST_API_VERSION,
                    domain="settings",
                    operation="load",
                    params={"path": str(path_v0_2)},
                )
            )
            self._settings_path = path_v0_2
        return result

    def reload_settings(self) -> PapicoResult[AppSettings]:
        result = self.load_settings()
        if not result.success:
            return PapicoFailure(
                ctx=PapicoExecContext(
                    api_version=result.ctx.api_version,
                    domain="settings",
                    operation="reload",
                ),
                error=result.error,
            )

        if (settings := get_app_settings_or_none()) is None:
            settings = setup_app_settings(result.data)
        else:
            settings.apply_dict(result.data.to_dict())

        return PapicoSuccess(
            ctx=PapicoExecContext(
                api_version=settings.general.version.get(),
                domain="settings",
                operation="reload",
            ),
            data=settings,
        )

    def save_settings(self) -> PapicoResult[None]:
        if (settings := get_app_settings()) is None:
            raise PapicoExecException(
                "Settings is not loaded yet. Please call load_settings() first.",
            )

        version = settings.general.version.get()
        if version == "0.2.0":
            path = self._base_dir / "profiles" / self._profile / "settings.json"
            return self._exec(
                PapicoExecContext(
                    api_version=version,
                    domain="settings",
                    operation="save",
                    params={"settings": settings, "path": str(path)},
                )
            )
        elif version == "0.1.8":
            path = self._base_dir / "profiles" / self._profile / "settings.ini"
            return self._exec(
                PapicoExecContext(
                    api_version=version,
                    domain="settings",
                    operation="save",
                    params={"settings": settings, "path": str(path)},
                )
            )
        else:
            raise PapicoExecException(f"Unknown version: {version}")

    def _exec(self, ctx: PapicoExecContext) -> PapicoResult:
        if self._current_handler is not None:
            raise PapicoExecException(message="Other handler is running already.")
        try:
            self._current_handler = handler = self._handler_generators[ctx.api_version][
                ctx.domain
            ][ctx.operation]()
            return handler.handle(ctx)
        except KeyError as e:
            raise PapicoExecException(message=f"Operation not found: {e}") from e
        finally:
            self._current_handler = None


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
