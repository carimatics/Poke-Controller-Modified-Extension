from .app import PokeControllerExtensionApp
from .values import literals as l
from .windows import MainWindow


def run_app():
    app = PokeControllerExtensionApp()
    main_window = MainWindow(app)
    main_window.pack(expand=True, fill=l.BOTH)
    app.mainloop()
