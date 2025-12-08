import logging
from pathlib import Path
from tkinter import BooleanVar, DoubleVar, IntVar, StringVar
from typing import Any

from pokecontroller.core.config import Config

from pokecontrollermodifiedextension.settings import (
    DEFAULT_SETTINGS,
    SCHEMA,
    AppSettings,
)

from ....context import PapicoExecContext, PapicoResult
from ....exception import PapicoSettingsLoadHandlerException
from ...handler import PapicoHandler
from .mapping import MAPPING

logger = logging.getLogger(__name__)


class PapicoSettingsLoadHandler(PapicoHandler):
    _path: str
    _settings: dict[str, Any]
    _tk_variables: dict[str, Any]

    def handle(self, ctx: PapicoExecContext) -> PapicoResult[AppSettings]:
        try:
            if (params := ctx.params) is None or "path" not in params:
                raise PapicoSettingsLoadHandlerException("Path is required.")
            self._path: str = params["path"]
            self._settings = self._load_settings()
            self._fill_by_default()
            self._tk_variables = self._value_to_tk_variables()
            return PapicoResult(
                success=True,
                ctx=ctx,
                data=AppSettings.from_dict(self._tk_variables),
            )
        except Exception as e:
            logger.error(f"Settings load failed: {e}")
            return PapicoResult(
                success=False,
                ctx=ctx,
                error=PapicoSettingsLoadHandlerException(
                    f"{e}",
                ),
            )

    def _load_settings(self) -> dict[str, Any]:
        if not Path(self._path).exists():
            return {}
        config = Config(self._path)
        config.load()

        def convert(mapping: Any, res: dict[str, Any]) -> None:
            for k, m in mapping.items():
                if isinstance(m, dict):
                    r = res.setdefault(k, {})
                    convert(m, r)
                elif isinstance(m, str):
                    (section, option) = m.split("/")
                    if config.has_option(section, option):
                        res[k] = config[section][option]

        result: dict[str, Any] = {}
        convert(MAPPING, result)

        # 以下は特別対応
        result["general"]["version"] = "0.1.8"
        widget_mode = config["Output"]["widget_mode"]
        if "ALL" in widget_mode:
            result["widget"]["output"]["visible_output1"] = True
            result["widget"]["output"]["visible_output2"] = True
            result["widget"]["software_controller"]["visible"] = True
        else:
            result["widget"]["output"]["visible_output1"] = "Output$1" in widget_mode
            result["widget"]["output"]["visible_output2"] = "Output$2" in widget_mode
            result["widget"]["software_controller"]["visible"] = (
                "Software-Controller" in widget_mode
            )

        software_controller_position_num = int(
            config["Output"]["software_controller_position"]
        )
        if software_controller_position_num == 1:
            result["widget"]["software_controller"]["position"] = "top"
        else:
            result["widget"]["software_controller"]["position"] = "bottom"

        dialogue_buttons_position_num = int(
            config["Output"]["dialogue_buttons_position"]
        )
        if dialogue_buttons_position_num == 1:
            result["widget"]["dialog"]["confirm_buttons_position"] = "top"
        elif dialogue_buttons_position_num == 2:
            result["widget"]["dialog"]["confirm_buttons_position"] = "bottom"
        else:
            result["widget"]["dialog"]["confirm_buttons_position"] = "both"

        return result

    def _fill_by_default(self) -> None:
        def assign_default(data: dict[str, Any], default: dict[str, Any]) -> None:
            for k, v in default.items():
                if isinstance(v, dict):
                    d = data.setdefault(k, {})
                    assign_default(d, v)
                else:
                    data.setdefault(k, v)

        assign_default(self._settings, DEFAULT_SETTINGS)

    def _value_to_tk_variables(self) -> dict[str, Any]:
        def to_tk_variables(
            data: dict[str, Any], schema: dict[str, Any], res: dict[str, Any]
        ) -> None:
            for k, v in data.items():
                if isinstance(v, dict):
                    d = res.setdefault(k, {})
                    to_tk_variables(v, schema[k], d)
                elif schema[k] is bool:
                    res[k] = BooleanVar(value=v)
                elif schema[k] is int:
                    res[k] = IntVar(value=v)
                elif schema[k] is float:
                    res[k] = DoubleVar(value=v)
                elif schema[k] is str:
                    res[k] = StringVar(value=v)
                else:
                    raise ValueError(f"unsupported type: {type(v)}")

        result: dict[str, Any] = {}
        to_tk_variables(self._settings, SCHEMA, result)
        return result
