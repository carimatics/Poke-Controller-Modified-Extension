import logging
from pathlib import Path
from typing import Any

from pokecontroller.utils.config import Config

from pokecontrollermodifiedextension.settings import AppSettings, settings_to_dict

from ....context import PapicoExecContext, PapicoFailure, PapicoResult, PapicoSuccess
from ....exception import PapicoSettingsLoadHandlerException
from ....handlers import PapicoHandler
from .mapping import MAPPING

logger = logging.getLogger(__name__)


class PapicoSettingsSaveHandler(PapicoHandler):
    _path: str
    _settings: AppSettings
    _values: dict[str, Any]

    def handle(self, ctx: PapicoExecContext) -> PapicoResult[None]:
        if (params := ctx.params) is None:
            raise PapicoSettingsLoadHandlerException("params is required.")
        if "settings" not in params:
            raise PapicoSettingsLoadHandlerException("Settings is required.")
        if "path" not in params:
            raise PapicoSettingsLoadHandlerException("Path is required.")

        try:
            self._path = params["path"]
            self._values = settings_to_dict(params["settings"])
            self._save_settings()
            return PapicoSuccess(
                ctx=ctx,
                data=None,
            )
        except Exception as e:
            logger.error(f"Settings save failed: {e}")
            return PapicoFailure(
                ctx=ctx,
                error=PapicoSettingsLoadHandlerException(f"{e}"),
            )

    def _save_settings(self) -> None:
        path = Path(self._path)
        base = path.parent
        if base.exists() and not base.is_dir():
            raise PapicoSettingsLoadHandlerException(f"{base} is not directory.")

        if not base.exists():
            base.mkdir(parents=True, exist_ok=True)

        config = Config(self._path)

        def convert(data: Any, mapping: Any) -> None:
            for k, v in mapping.items():
                if isinstance(v, dict):
                    convert(data[k], v)
                elif isinstance(v, str):
                    (section, option) = v.split("/")
                    config.set(section, option, str(data[k]))

        convert(self._values, MAPPING)

        # 以下は特別対応
        visible_output1 = self._values["widget"]["output"]["visible_output1"]
        visible_output2 = self._values["widget"]["output"]["visible_output2"]
        visible_software_controller = self._values["widget"]["software_controller"][
            "visible"
        ]
        if visible_output1 and visible_output2 and visible_software_controller:
            config.set("Output", "widget_mode", "ALL (default)")
        else:
            vlist: list[str] = []
            if visible_output1:
                vlist.append("Output$1")
            if visible_output2:
                vlist.append("Output$2")
            if visible_software_controller:
                vlist.append("Software-Controller")
            widget_mode = " + ".join(vlist)
            if len(vlist) == 1:
                widget_mode = f"{widget_mode} Only"
            config.set("Output", "widget_mode", widget_mode)

        software_controller_position = self._values["widget"]["software_controller"][
            "position"
        ]
        if software_controller_position == "top":
            software_controller_position = "1"
        else:
            software_controller_position = "2"
        config.set(
            "Output", "software_controller_position", software_controller_position
        )

        dialogue_buttons_position = self._values["widget"]["dialog"][
            "confirm_buttons_position"
        ]
        if dialogue_buttons_position == "top":
            dialogue_buttons_position = "1"
        elif dialogue_buttons_position == "bottom":
            dialogue_buttons_position = "2"
        else:
            dialogue_buttons_position = "3"
        config.set("Output", "dialogue_buttons_position", dialogue_buttons_position)

        pokemon_home_single_or_double = self._values["external"]["pokemon_home"][
            "single_or_double"
        ]
        if pokemon_home_single_or_double == "single":
            pokemon_home_single_or_double = "シングル"
        else:
            pokemon_home_single_or_double = "ダブル"
        config.set("Pokemon Home", "Single or Double", pokemon_home_single_or_double)

        config.save()
