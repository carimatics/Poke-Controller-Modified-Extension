import tkinter as tk
import tkinter.ttk as ttk


def separator(master: ttk.Widget, orient: str = tk.VERTICAL):
    return ttk.Separator(master=master, orient=orient)
