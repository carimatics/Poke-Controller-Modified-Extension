from pokecontroller.core.logging import setup_logging
from .app import App
from .values import literals as l
from .windows import MainWindow


def run_app() -> None:
    setup_logging()

    app = App()
    main_window = MainWindow(app)
    main_window.pack(expand=True, fill=l.BOTH)
    app.mainloop()
