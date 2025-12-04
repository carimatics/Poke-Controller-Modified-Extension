from pokecontroller.core.camera import use_camera

from .app import App
from .core.logging import setup_logging
from .values import literals as l
from .widgets.menu import AppMenu
from .windows import MainWindow


def run_app(*, base_dir: str, profile: str) -> None:
    setup_logging()

    with use_camera() as camera:
        app = App(
            base_dir=base_dir,
            profile=profile,
            camera=camera,
        )

        # config menubar
        menu = AppMenu(app)
        app.config(menu=menu)

        # create main window
        main_window = MainWindow(app)
        main_window.pack(expand=True, fill=l.BOTH)

        # run app
        app.mainloop()
