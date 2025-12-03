from .app import App
from .core.logging import setup_logging
from .values import literals as l
from .widgets.menu import AppMenu
from .windows import MainWindow


def run_app() -> None:
    setup_logging()

    app = App()

    menu = AppMenu(app)
    app.config(menu=menu)

    main_window = MainWindow(app)
    main_window.pack(expand=True, fill=l.BOTH)

    app.mainloop()
