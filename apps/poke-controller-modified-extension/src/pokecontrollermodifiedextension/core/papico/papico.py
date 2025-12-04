from typing import Callable

from .context import PapicoExecContext, PapicoRegisterHandlerContext, PapicoResult
from .exception import PapicoExecException
from .handlers.handler import PapicoHandler

type PapicoContainer[T] = dict[str, dict[str, dict[str, T]]]
PapicoHandlerGenerator = Callable[[], PapicoHandler]


class Papico:
    """Poke-Controller Public API Compatible Orchestrator

    Poke-Controllerの公開APIのバージョンによって異なる処理を適切に振り分けるクラス
    """

    def __init__(self) -> None:
        self._handler_generators: PapicoContainer[PapicoHandlerGenerator] = {}
        self._current_handler: PapicoHandler | None = None

    def exec(self, ctx: PapicoExecContext) -> PapicoResult:
        if self._current_handler is None:
            raise PapicoExecException(
                message="Other handler is running already.", ctx=ctx
            )
        try:
            self._current_handler = handler = self._handler_generators[ctx.api_version][
                ctx.domain
            ][ctx.operation]()
            return handler.handle(ctx)
        except KeyError as e:
            raise PapicoExecException(message=f"Operation not found: {e}", ctx=ctx)
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
