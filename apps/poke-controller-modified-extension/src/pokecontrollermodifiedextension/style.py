import tkinter as tk
import tkinter.ttk as ttk


def setup_style(app: tk.Tk, theme: str) -> None:
    style = ttk.Style(app)

    # Theme
    style.theme_use(theme)

    # Custom Style
    # style.configure('App.TButton')
    # style.map('App.TButton', foreground=[('disabled', '#ff0000')])


def apply_theme(app: tk.Tk, theme: str) -> None:
    style = ttk.Style(app)
    style.theme_use(theme)


def get_themes() -> tuple[str, ...]:
    return ttk.Style().theme_names()
