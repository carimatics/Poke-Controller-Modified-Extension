import tomllib
from pathlib import Path
from typing import Any

from ......state import AppGuiState
from ....context import PapicoExecContext, PapicoResult
from ....exception import PapicoGuiStateLoadHandlerException
from ....handlers.handler import PapicoHandler

# @formatter:off (for PyCharm)
# fmt: off
# language=toml
DEFAULT_GUI_STATE: str = """
[general]
theme = "default"
version = "0.1.8"

[capture]
camera_id = 0
camera_name = "0"
fps = 45
size = "640x360"
show_realtime = true
show_matched = false
show_guide = false

[serial]
port = ""
port_name = ""
baud_rate = 9600
data_format = "Default"
show_data = false

[device_input]
touchscreen.sx = 1
touchscreen.sy = 1
touchscreen.ex = 320
touchscreen.ey = 240
enabled_keyboard = true
enabled_lstick_mouse = true
enabled_rstick_mouse = true
enabled_pro_controller = false
enabled_record_pro_controller = false

[command]
python_commands_filter = "-"
python_command = ""
mcu_commands_filter = "-"
mcu_command = ""

[command.shortcut]
number = 1

[command.shortcut.registered_commands]
1.name = "(empty)"
1.klass = "None"
2.name = "(empty)"
2.klass = "None"
3.name = "(empty)"
3.klass = "None"
4.name = "(empty)"
4.klass = "None"
5.name = "(empty)"
5.klass = "None"
6.name = "(empty)"
6.klass = "None"
7.name = "(empty)"
7.klass = "None"
8.name = "(empty)"
8.klass = "None"
9.name = "(empty)"
9.klass = "None"
10.name = "(empty)"
10.klass = "None"

[notification]
line.enabled_started = false
line.enabled_ended = false
discord.enabled_started = false
discord.enabled_ended = false

[widget]
outputs.size_balance = 50.0
outputs.stdout = 1
outputs.visible_output1 = true
outputs.visible_output2 = true
software_controller.position = "bottom"
software_controller.visible = true
dialog.confirm_buttons_position = "bottom"
"""
# fmt: on
# @formatter:on (for PyCharm)


class PapicoGuiStateLoadHandler(PapicoHandler):
    def handle(self, ctx: PapicoExecContext) -> PapicoResult[AppGuiState]:
        try:
            path: str = ctx.params["path"]
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
            self._fill_by_default(settings)
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

    def _fill_by_default(self, settings: dict[str, Any], default: dict[str, Any]) -> None:
        for k, v in default.items():
            if isinstance(v, dict):
                data = settings.setdefault(k, {})
                self._fill_by_default(data, v)
            else:
                settings.setdefault(k, v)
