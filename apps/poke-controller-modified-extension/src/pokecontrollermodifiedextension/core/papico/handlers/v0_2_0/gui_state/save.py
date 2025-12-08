from pathlib import Path

from pokecontroller.core.string import substitute_nested

from ......state import AppGuiState
from ....context import PapicoExecContext, PapicoResult
from ....exception import PapicoGuiStateLoadHandlerException
from ....handlers.handler import PapicoHandler
from .utils import SETTINGS_TEMPLATE, to_dict


class PapicoGuiStateSaveHandler(PapicoHandler):
    _path: str
    _state: AppGuiState
    _state_str: str

    def handle(self, ctx: PapicoExecContext) -> PapicoResult[AppGuiState]:
        try:
            if (params := ctx.params) is None:
                raise PapicoGuiStateLoadHandlerException("params is required.")
            if "path" not in params:
                raise PapicoGuiStateLoadHandlerException("Path is required.")
            if "state" not in params:
                raise PapicoGuiStateLoadHandlerException("State is required.")

            self._path = params["path"]
            self._state = params["state"]

            self._state_str = self._state_to_string()
            self._save_setting()

            return PapicoResult(
                success=True,
                ctx=ctx,
            )
        except Exception as e:
            return PapicoResult(
                success=False,
                ctx=ctx,
                error=PapicoGuiStateLoadHandlerException(
                    f"{e}",
                ),
            )

    def _state_to_string(self) -> str:
        return substitute_nested(SETTINGS_TEMPLATE, to_dict(self._state))

    def _save_setting(self) -> None:
        path = Path(self._path)

        if path.parent.exists() and not path.parent.is_dir():
            raise PapicoGuiStateLoadHandlerException(f"{path.parent} is not directory.")

        if not path.parent.exists():
            path.parent.mkdir(parents=True, exist_ok=True)

        with open(self._path, "wb") as f:
            f.write(self._state_str.encode("utf-8"))
