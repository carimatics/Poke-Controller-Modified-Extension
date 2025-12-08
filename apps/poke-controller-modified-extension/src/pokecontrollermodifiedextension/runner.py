from pathlib import Path

from pokecontroller.core.camera import use_camera
from pokecontroller.core.serial import use_serial

from .app import App
from .core.logging import setup_logging
from .core.papico.handlers.v0_1_8.gui_state import PapicoGuiStateLoadHandler_v0_1_8
from .core.papico.handlers.v0_2_0.gui_state import PapicoGuiStateLoadHandler_v0_2_0
from .core.papico.papico import Papico, PapicoRegisterHandlerContext
from .values import literals as l
from .widgets.menu import AppMenu
from .windows import MainWindow


def run_app(*, base_dir: str, profile: str) -> None:
    setup_logging()

    with (
        use_camera() as camera,
        use_serial() as serial,
    ):
        base_dir_path = Path(base_dir)
        papico = Papico(base_dir=base_dir_path, profile=profile)
        _register_handlers(papico)

        app = App(
            base_dir=base_dir_path,
            profile=profile,
            papico=papico,
            camera=camera,
            serial=serial,
        )

        # config menubar
        menu = AppMenu(app)
        app.config(menu=menu)

        # create main window
        main_window = MainWindow(app)
        main_window.pack(expand=True, fill=l.BOTH)

        # run app
        app.mainloop()

def _register_handlers(papico: Papico) -> None:
    # GUI State
    papico.register_handler(
        PapicoRegisterHandlerContext(
            api_version="0.1.8",
            domain="gui_state",
            operation="load",
            handler_generator=PapicoGuiStateLoadHandler_v0_1_8,
        ),
    )
    papico.register_handler(
        PapicoRegisterHandlerContext(
            api_version="0.2.0",
            domain="gui_state",
            operation="load",
            handler_generator=PapicoGuiStateLoadHandler_v0_2_0,
        ),
    )
