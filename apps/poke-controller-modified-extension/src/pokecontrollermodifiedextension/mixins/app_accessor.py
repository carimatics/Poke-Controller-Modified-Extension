import tkinter as tk

from ..app import App


class AppAccessorMixIn(tk.Misc):
    @property
    def app(self) -> App:
        toplevel = self.winfo_toplevel()
        if isinstance(toplevel, App):
            return toplevel
        if isinstance(toplevel, tk.Toplevel):
            return toplevel.app  # type: ignore[attr-defined, no-any-return]
        raise RuntimeError("AppAccessorMixIn can only be used in App or Toplevel")
