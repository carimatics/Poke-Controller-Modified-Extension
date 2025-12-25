import logging
import tkinter as tk
from typing import Any

from pokecontrollermodifiedextension.core.exception import AppRuntimeException
from pokecontrollermodifiedextension.core.style import (
    StyleManager,
)
from pokecontrollermodifiedextension.singletons.app.command import (
    setup_app_command_state,
)
from pokecontrollermodifiedextension.singletons.app.model import setup_app_model
from pokecontrollermodifiedextension.singletons.app.settings import setup_app_settings
from pokecontrollermodifiedextension.singletons.app.style import setup_style_manager
from pokecontrollermodifiedextension.singletons.app.translation import setup_translation
from pokecontrollermodifiedextension.singletons.runtime.app_info import get_app_info
from pokecontrollermodifiedextension.singletons.runtime.papico import get_papico
from pokecontrollermodifiedextension.singletons.runtime.resources import (
    get_app_resources,
)
from pokecontrollermodifiedextension.singletons.runtime.runtime_info import (
    get_app_runtime_info,
)

logger = logging.getLogger(__name__)


class App(tk.Tk):
    def __init__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)

        self._app_runtime_info = get_app_runtime_info()
        self._app_info = get_app_info()
        self._app_command_state = setup_app_command_state()

        self._papico = get_papico()
        if (settings := self._papico.load_settings().data) is None:
            raise AppRuntimeException("App settings couldn't load.")
        self._settings = setup_app_settings(settings)
        setup_app_model()

        setup_translation(
            base_dir=self._app_info.application_root / "translations",
            language=self._settings.general.language.get(),
        )

        self._resources = get_app_resources()

        self._style_manager = setup_style_manager(self)
        self._style_manager.change_theme(self._settings.general.theme.get())

        # Title
        self.title(f"{self._app_info.name}(v{self._app_info.version})")

        # Camera
        self._camera_id = self._settings.capture.camera_id
        try:
            self._resources.camera.open(camera_id=self._camera_id.get())
        except Exception as e:
            logger.warning(f"Failed to open camera: {e}")

        # Serial
        self._serial_port = self._settings.serial.port
        self._serial_baud_rate = self._settings.serial.baud_rate
        try:
            self._resources.serial.open(
                port_path=self._serial_port.get(),
                baud_rate=self._serial_baud_rate.get(),
            )
        except Exception as e:
            logger.warning(f"Failed to open serial port: {e}")

        self._register_traces()

    @property
    def style_manager(self) -> StyleManager:
        return self._style_manager

    def run(self) -> None:
        self.mainloop()

    def _register_traces(self) -> None:
        self._settings.general.theme.trace_add("write", self._apply_theme)

    def _apply_theme(self, *_: Any) -> None:
        self._style_manager.change_theme(self._settings.general.theme.get())
