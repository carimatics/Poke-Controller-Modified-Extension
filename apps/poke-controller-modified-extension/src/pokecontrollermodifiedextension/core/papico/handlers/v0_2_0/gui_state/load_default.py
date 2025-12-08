import tomllib
from typing import Any

from ......state import AppGuiState
from ....context import PapicoExecContext, PapicoResult
from ....exception import PapicoGuiStateLoadHandlerException
from ....handlers.handler import PapicoHandler
from .default import DEFAULT_GUI_STATE


class PapicoGuiStateLoadDefaultHandler(PapicoHandler):
    def handle(self, ctx: PapicoExecContext) -> PapicoResult[AppGuiState]:
        try:
            default: dict[str, Any] = tomllib.loads(DEFAULT_GUI_STATE)
            return PapicoResult(
                success=True,
                ctx=ctx,
                data=AppGuiState.from_dict(default),
            )
        except Exception as e:
            return PapicoResult(
                success=False,
                ctx=ctx,
                error=PapicoGuiStateLoadHandlerException(
                    f"{e}",
                ),
            )
