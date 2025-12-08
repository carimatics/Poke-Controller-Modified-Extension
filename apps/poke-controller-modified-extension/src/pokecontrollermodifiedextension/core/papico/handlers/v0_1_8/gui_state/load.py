from configparser import ConfigParser
from pathlib import Path

from ......state import AppGuiState
from ....context import PapicoExecContext, PapicoResult
from ....exception import PapicoGuiStateLoadHandlerException
from ....handlers.handler import PapicoHandler
from .default import DEFAULT_SETTINGS
from .utils import config_to_state


class PapicoGuiStateLoadHandler(PapicoHandler):
    def handle(self, ctx: PapicoExecContext) -> PapicoResult[AppGuiState]:
        try:
            if (params := ctx.params) is None or "path" not in params:
                raise PapicoGuiStateLoadHandlerException("Path is required.")
            path: str = params["path"]
            config = self._read_config(path)
            self._fill_by_default(config)
            return PapicoResult(
                success=True,
                ctx=ctx,
                data=config_to_state(config),
            )
        except Exception as e:
            default = ConfigParser(allow_no_value=True)
            default.read_string(DEFAULT_SETTINGS)
            return PapicoResult(
                success=False,
                ctx=ctx,
                data=config_to_state(default),
                error=PapicoGuiStateLoadHandlerException(
                    f"{e}",
                ),
            )

    def _read_config(self, path: str) -> ConfigParser:
        p = Path(path)
        config = ConfigParser(
            allow_no_value=True,
            comment_prefixes=("#", ";"),
        )
        config.optionxform = str  # type: ignore[assignment]

        if not p.exists() or not p.is_file():
            return config

        try:
            config.read(path, encoding="utf-8")
        except Exception as e:
            raise PapicoGuiStateLoadHandlerException(
                f"Config could not read: {e}",
            ) from e

        return config

    def _fill_by_default(self, config: ConfigParser) -> None:
        default = ConfigParser(allow_no_value=True)
        default.read_string(DEFAULT_SETTINGS)

        # General Setting
        sections = default.sections()
        for section in sections:
            if not config.has_section(section):
                config.add_section(section)
            for key, value in default.items(section):
                config[section].setdefault(key, value)
