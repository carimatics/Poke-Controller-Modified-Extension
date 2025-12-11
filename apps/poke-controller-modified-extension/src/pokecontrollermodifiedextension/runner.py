from pathlib import Path
from typing import Any

from pokecontroller.core.camera import use_camera
from pokecontroller.core.serial import use_serial

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
from .core.papico.papico import Papico, PapicoRegisterHandlerContext
from .values import literals as l
from .widgets.app import AppMenu
from .windows import MainWindow


def run_app(*, base_dir: str, profile: str) -> None:
    setup_logging()

    with (
        use_camera() as camera,
        use_serial() as serial,
    ):
        base_dir_path = Path(base_dir)

        # papico
        papico = Papico(base_dir=base_dir_path, profile=profile)
        _register_handlers(papico)

        # app
        app = App(
            base_dir=base_dir_path,
            profile=profile,
            papico=papico,
            camera=camera,
            serial=serial,
        )

        # menubar
        menu = AppMenu(app)
        app.config(menu=menu)

        # main window
        main_window = MainWindow(app)
        main_window.pack(expand=True, fill=l.BOTH)

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
