import tkinter as tk

from ...app import PokeControllerApp
from ...info import PokeControllerAppInfo
from ...state import PokeControllerAppState

from .windows import MainWindow


class PokeControllerExtensionApp(tk.Tk, PokeControllerApp):
    def __init__(self, info: PokeControllerAppInfo, state: PokeControllerAppState, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        PokeControllerApp.__init__(self, info, state)

        # FIXME
        self.title("PokeController Extension")

        self.build_ui()

    def run(self):
        self.mainloop()

    def build_ui(self):
        main_window = MainWindow(self,
                                 padding=5,
                                 relief=tk.SOLID,
                                 borderwidth=5)
        main_window.pack(expand=True, fill=tk.BOTH)
