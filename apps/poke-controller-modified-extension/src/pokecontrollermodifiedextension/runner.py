import sys
import tkinter as tk
from pathlib import Path
from typing import Any

from pokecontroller.core.camera import use_camera
from pokecontroller.core.serial import use_serial

from pokecontrollermodifiedextension.app import App
from pokecontrollermodifiedextension.logging import setup_logging
from pokecontrollermodifiedextension.papico import (
    Papico,
    setup_papico,
)
from pokecontrollermodifiedextension.papico.handlers import (
    PapicoRegisterHandlerContext,
)
from pokecontrollermodifiedextension.papico.handlers.v0_1_8.command import (
    PapicoCommandInitializeHandler as PapicoCommandInitializeHandler_v0_1_8,
    PapicoCommandLoadHandler as PapicoCommandLoadHandler_v0_1_8,
    PapicoCommandPauseHandler as PapicoCommandPauseHandler_v0_1_8,
    PapicoCommandResumeHandler as PapicoCommandResumeHandler_v0_1_8,
    PapicoCommandStartHandler as PapicoCommandStartHandler_v0_1_8,
    PapicoCommandStopHandler as PapicoCommandStopHandler_v0_1_8,
)
from pokecontrollermodifiedextension.papico.handlers.v0_1_8.settings import (
    PapicoSettingsLoadHandler as PapicoSettingsLoadHandler_v0_1_8,
    PapicoSettingsSaveHandler as PapicoSettingsSaveHandler_v0_1_8,
)
from pokecontrollermodifiedextension.papico.handlers.v0_2_0.settings import (
    PapicoSettingsLoadHandler as PapicoSettingsLoadHandler_v0_2_0,
    PapicoSettingsSaveHandler as PapicoSettingsSaveHandler_v0_2_0,
)
from pokecontrollermodifiedextension.state.resources import setup_app_resources
from pokecontrollermodifiedextension.state.runtime_info import setup_runtime_info
from pokecontrollermodifiedextension.widgets.menu import Menu
from pokecontrollermodifiedextension.windows import MainWindow


def run_app(*, base_dir: Path, profile: str) -> None:
    sys.path.append(str(base_dir))
    setup_logging()

    with (
        use_camera() as camera,
        use_serial() as serial,
    ):
        setup_app_resources(
            camera=camera,
            serial=serial,
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
        menu = Menu(app)
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
        "command": {
            "initialize": {
                "0.1.8": PapicoCommandInitializeHandler_v0_1_8,
            },
            "load": {
                "0.1.8": PapicoCommandLoadHandler_v0_1_8,
            },
            "start": {
                "0.1.8": PapicoCommandStartHandler_v0_1_8,
            },
            "stop": {
                "0.1.8": PapicoCommandStopHandler_v0_1_8,
            },
            "pause": {
                "0.1.8": PapicoCommandPauseHandler_v0_1_8,
            },
            "resume": {
                "0.1.8": PapicoCommandResumeHandler_v0_1_8,
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
