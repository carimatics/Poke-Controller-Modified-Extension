from pathlib import Path
from typing import Callable

from .context import PapicoExecContext, PapicoResult
from .exception import PapicoExecException
from .handlers import PapicoHandler, PapicoRegisterHandlerContext

type PapicoContainer[T] = dict[str, dict[str, dict[str, T]]]
PapicoHandlerGenerator = Callable[[], PapicoHandler]

LATEST_API_VERSION = "0.2.0"


class Papico:
    """Poke-Controller Public API Compatible Orchestrator

    Poke-Controllerの公開APIのバージョンによって異なる処理を適切に振り分けるクラス
    """

    def __init__(self, base_dir: Path, profile: str) -> None:
        self._base_dir = base_dir
        self._profile = profile
        self._handler_generators: PapicoContainer[PapicoHandlerGenerator] = {}
        self._current_handler: PapicoHandler | None = None

    def load_gui_state(self) -> PapicoResult:
        path_v0_2 = self._base_dir / "profiles" / self._profile / "settings.toml"
        path_v0_1 = self._base_dir / "profiles" / self._profile / "settings.ini"
        if path_v0_2.exists() and path_v0_2.is_file():
            result = self._exec(
                PapicoExecContext(
                    api_version="0.2.0",
                    domain="gui_state",
                    operation="load",
                    params={"path": str(path_v0_2)},
                )
            )
        elif path_v0_1.exists() and path_v0_1.is_file():
            result = self._exec(
                PapicoExecContext(
                    api_version="0.1.8",
                    domain="gui_state",
                    operation="load",
                    params={"path": str(path_v0_1)},
                )
            )
        else:
            result = self._exec(
                PapicoExecContext(
                    api_version=LATEST_API_VERSION,
                    domain="gui_state",
                    operation="load",
                    params={"path": str(path_v0_2)},
                )
            )
        return result

    def load_default_gui_state(self) -> PapicoResult:
        return self._exec(
            PapicoExecContext(
                api_version=LATEST_API_VERSION,
                domain="gui_state",
                operation="load_default",
            )
        )

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

    def register_handler(self, ctx: PapicoRegisterHandlerContext) -> None:
        self._handler_generators.setdefault(
            ctx.api_version,
            {},
        ).setdefault(
            ctx.domain,
            {},
        )[ctx.operation] = ctx.handler_generator
