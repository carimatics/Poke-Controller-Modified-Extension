import tkinter as tk
import tkinter.ttk as ttk
from typing import Literal


def separator(
    master: ttk.Widget,
    orient: Literal["vertical", "horizontal"] = tk.VERTICAL,
) -> ttk.Separator:
    return ttk.Separator(master=master, orient=orient)
