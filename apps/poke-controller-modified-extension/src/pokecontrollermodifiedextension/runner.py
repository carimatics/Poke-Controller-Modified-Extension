import sys
import tkinter as tk
from pathlib import Path
from typing import Any

from pokecontroller.core.camera import use_camera
from pokecontroller.core.serial import use_serial

from .api.v0_1_8.camera import use_camera as use_camera_v0_1_8
from .api.v0_1_8.command.sender import use_sender as use_sender_v0_1_8
from .app import App
from .core.logging import setup_logging
from .core.papico.handlers.v0_1_8.settings import (
    PapicoSettingsLoadHandler as PapicoSettingsLoadHandler_v0_1_8,
    PapicoSettingsSaveHandler as PapicoSettingsSaveHandler_v0_1_8,
)
from .core.papico.handlers.v0_2_0.settings import (
    PapicoSettingsLoadHandler as PapicoSettingsLoadHandler_v0_2_0,
    PapicoSettingsSaveHandler as PapicoSettingsSaveHandler_v0_2_0,
)
from .core.papico.papico import Papico, PapicoRegisterHandlerContext, setup_papico
from .resources import setup_app_resources
from .runtime_info import setup_runtime_info
from .widgets.app import AppMenu
from .windows import MainWindow


def run_app(*, base_dir: Path, profile: str) -> None:
    sys.path.append(str(base_dir))
    setup_logging()

    with (
        use_camera() as camera,
        use_serial() as serial,
        use_sender_v0_1_8() as sender_v0_1_8,
        use_camera_v0_1_8() as camera_v0_1_8,
    ):
        camera_v0_1_8._set_camera(camera)

        setup_app_resources(
            camera=camera,
            serial=serial,
            camera_v0_1_8=camera_v0_1_8,
            sender_v0_1_8=sender_v0_1_8,
        )

        # runtime info
        setup_runtime_info(
            base_dir=base_dir,
            profile=profile,
        )

        # papico
        papico = setup_papico()
        _register_handlers(papico)

        # app
        app = App()

        # menubar
        menu = AppMenu(app)
        app.config(menu=menu)

        # main window
        main_window = MainWindow(app)
        main_window.pack(expand=True, fill=tk.BOTH)

        main_window.focus_force()

        # run app
        app.mainloop()


def _register_handlers(papico: Papico) -> None:
    handlers: dict[str, Any] = {
        "settings": {
            "load": {
                "0.2.0": PapicoSettingsLoadHandler_v0_2_0,
                "0.1.8": PapicoSettingsLoadHandler_v0_1_8,
            },
            "save": {
                "0.2.0": PapicoSettingsSaveHandler_v0_2_0,
                "0.1.8": PapicoSettingsSaveHandler_v0_1_8,
            },
        },
    }

    # register handlers
    for domain, operations in handlers.items():
        for operation, versions in operations.items():
            for version, handler_generator in versions.items():
                papico.register_handler(
                    PapicoRegisterHandlerContext(
                        api_version=version,
                        domain=domain,
                        operation=operation,
                        handler_generator=handler_generator,
                    ),
                )
