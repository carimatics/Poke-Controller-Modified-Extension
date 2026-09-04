import json
from pathlib import Path
from typing import Any

from pokecontrollerext.app.settings import AppSettings, settings_to_dict
from pokecontrollerext.papico.context import (
    PapicoExecContext,
    PapicoFailure,
    PapicoResult,
    PapicoSuccess,
)
from pokecontrollerext.papico.exception import (
    PapicoSettingsSaveHandlerException,
)
from pokecontrollerext.papico.handlers import (
    PapicoHandler,
)


class PapicoSettingsSaveHandler(PapicoHandler):
    _path: Path
    _settings: AppSettings
    _values: dict[str, Any]

    def handle(self, ctx: PapicoExecContext) -> PapicoResult[None]:
        if (params := ctx.params) is None:
            raise PapicoSettingsSaveHandlerException("params is required.")
        if "settings" not in params:
            raise PapicoSettingsSaveHandlerException("Settings is required.")
        if "path" not in params:
            raise PapicoSettingsSaveHandlerException("Path is required.")

        try:
            self._path = params["path"]
            self._values = settings_to_dict(params["settings"])
            self._save_settings()
            return PapicoSuccess(
                ctx=ctx,
                data=None,
            )
        except Exception as e:
            return PapicoFailure(
                ctx=ctx,
                error=PapicoSettingsSaveHandlerException(f"{e}"),
            )

    def _save_settings(self) -> None:
        base = self._path.parent
        if base.exists() and not base.is_dir():
            raise PapicoSettingsSaveHandlerException(f"{base} is not directory.")

        if not base.exists():
            base.mkdir(parents=True, exist_ok=True)

        self._path.write_text(
            json.dumps(self._values, indent=4),
            encoding="utf-8",
        )
