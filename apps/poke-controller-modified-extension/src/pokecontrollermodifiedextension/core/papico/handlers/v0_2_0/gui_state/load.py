import tomllib
from pathlib import Path
from typing import Any

from ......state import AppGuiState
from ....context import PapicoExecContext, PapicoResult
from ....exception import PapicoGuiStateLoadHandlerException
from ....handlers.handler import PapicoHandler
from .default import DEFAULT_GUI_STATE


class PapicoGuiStateLoadHandler(PapicoHandler):
    def handle(self, ctx: PapicoExecContext) -> PapicoResult[AppGuiState]:
        try:
            if (params := ctx.params) is None or "path" not in params:
                raise PapicoGuiStateLoadHandlerException("Path is required.")
            path: str = params["path"]
            settings: dict[str, Any] = self._read_settings(path)
            default: dict[str, Any] = tomllib.loads(DEFAULT_GUI_STATE)
            self._fill_by_default(settings, default)
            return PapicoResult(
                success=True,
                ctx=ctx,
                data=AppGuiState.from_dict(settings),
            )
        except Exception as e:
            settings = {}
            default = tomllib.loads(DEFAULT_GUI_STATE)
            self._fill_by_default(settings, default)
            return PapicoResult(
                success=False,
                ctx=ctx,
                data=AppGuiState.from_dict(settings),
                error=PapicoGuiStateLoadHandlerException(
                    f"{e}",
                ),
            )

    def _read_settings(self, path: str) -> dict[str, Any]:
        p = Path(path)
        if not p.exists() or not p.is_file():
            return {}

        try:
            with open(path, "rb") as f:
                return tomllib.load(f)
        except Exception as e:
            raise PapicoGuiStateLoadHandlerException(
                f"Settings could not read from '{path}': {e}",
            ) from e

    def _fill_by_default(
        self, settings: dict[str, Any], default: dict[str, Any]
    ) -> None:
        for k, v in default.items():
            if isinstance(v, dict):
                data = settings.setdefault(k, {})
                self._fill_by_default(data, v)
            else:
                settings.setdefault(k, v)
