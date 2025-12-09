import logging
import tkinter as tk
from pathlib import Path
from typing import Any

from pokecontroller.core.camera import Camera
from pokecontroller.core.serial import Serial

from .core.papico import Papico
from .info import AppInfo
from .model import AppModel
from .settings import AppSettings
from .translation import setup_translation
from .style import setup_style

logger = logging.getLogger(__name__)

INFO = AppInfo(
    name="Poke-Controller Modified Extension",
    version="0.2.0",
)


class App(tk.Tk):
    _settings: AppSettings

    def __init__(
        self,
        base_dir: Path,
        profile: str,
        papico: Papico,
        camera: Camera,
        serial: Serial,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._base_dir = base_dir
        self._profile = profile
        self._papico = papico

        self._camera = camera
        self._serial = serial

        self._app_info = INFO
        self._settings = papico.load_settings().data  # type: ignore[assignment]
        self._app_model = AppModel(self._app_info, self._settings)

        setup_translation(
            base_dir=base_dir / "translations",
            language=self._settings.general.language.get(),
        )

        setup_style(theme=self._settings.general.theme.get())

        # Title
        self.title(f"{INFO.name}(v{INFO.version})")

        # Camera
        self._camera_id = self._settings.capture.camera_id
        self._camera.open(camera_id=int(self._camera_id.get()))

        self._register_hooks()

    @property
    def base_dir(self) -> Path:
        return self._base_dir

    @property
    def profile(self) -> str:
        return self._profile

    @property
    def papico(self) -> Papico:
        return self._papico

    @property
    def camera(self) -> Camera:
        return self._camera

    @property
    def serial(self) -> Serial:
        return self._serial

    @property
    def app_info(self) -> AppInfo:
        return self._app_info

    @property
    def app_model(self) -> AppModel:
        return self._app_model

    @property
    def settings(self) -> AppSettings:
        return self._settings

    def run(self) -> None:
        self.mainloop()

    def _register_hooks(self) -> None:
        self._camera_id.trace_add("write", self._on_camera_id_changed)

    def _on_camera_id_changed(self, *_: Any) -> None:
        self._camera.open(camera_id=int(self._camera_id.get()))
