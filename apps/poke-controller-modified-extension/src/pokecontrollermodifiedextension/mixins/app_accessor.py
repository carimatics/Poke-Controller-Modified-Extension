import tkinter as tk
from typing import cast

from ..app import App


class AppAccessorMixIn(tk.Misc):
    @property
    def app(self) -> App:
        return cast(App, self.winfo_toplevel())
