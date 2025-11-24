import tkinter as tk
from .tkinter import (
    PokeControllerExtensionApp,
    MainWindow,
)


def run_app():
    app = PokeControllerExtensionApp()
    main_window = MainWindow(app)
    main_window.pack(expand=True, fill=tk.BOTH)
    app.mainloop()
