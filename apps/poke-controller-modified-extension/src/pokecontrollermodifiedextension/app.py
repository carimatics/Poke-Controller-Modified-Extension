import logging
import tkinter as tk
from typing import Any

from .core.command import setup_app_command_state
from .core.papico import get_papico
from .exception import AppRuntimeException
from .info import get_app_info
from .model import setup_app_model
from .resources import get_app_resources
from .runtime_info import get_app_runtime_info
from .settings import AppSettings, setup_app_settings
from .style import StyleManager
from .translation import setup_translation

logger = logging.getLogger(__name__)


class App(tk.Tk):
    _settings: AppSettings

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
        self._papico.initialize_command()
        if (settings := self._papico.load_settings().data) is None:
            raise AppRuntimeException("App settings couldn't load.")
        self._settings = setup_app_settings(settings)
        setup_app_model()

        setup_translation(
            base_dir=self._app_runtime_info.base_dir / "translations",
            language=self._settings.general.language.get(),
        )

        self._resources = get_app_resources()

        self._style_manager = StyleManager(self)
        self._style_manager.change_theme(self._settings.general.theme.get())

        # Title
        self.title(f"{self._app_info.name}(v{self._app_info.version})")

        # Camera
        self._camera_id = self._settings.capture.camera_id
        try:
            self._resources.camera.open(camera_id=int(self._camera_id.get()))
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
        self._camera_id.trace_add("write", self._on_camera_id_changed)
        self._settings.general.theme.trace_add("write", self._apply_theme)

    def _apply_theme(self, *_: Any) -> None:
        self._style_manager.change_theme(self._settings.general.theme.get())

    def _on_camera_id_changed(self, *_: Any) -> None:
        self._resources.camera.open(camera_id=int(self._camera_id.get()))
