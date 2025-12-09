import tkinter.ttk as ttk

def setup_style(theme: str):
    style = ttk.Style()

    # Theme
    style.theme_use(theme)

    # Custom Style
    # style.configure('App.TButton')
    # style.map('App.TButton', foreground=[('disabled', '#ff0000')])
