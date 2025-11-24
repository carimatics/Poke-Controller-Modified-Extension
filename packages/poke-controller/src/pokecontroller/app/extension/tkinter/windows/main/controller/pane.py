import platform
import tkinter as tk
import tkinter.ttk as ttk

from ....components import AppFrame

# 4字に揃えるためにアンダースコア(_)で名前をパディングしている
A___ = 'A'
B___ = 'B'
X___ = 'X'
Y___ = 'Y'
L___ = 'L'
R___ = 'R'
ZL__ = 'ZL'
ZR__ = 'ZR'
LC__ = 'L-C'
RC__ = 'R-C'
LSL_ = '←'
LSU_ = '↑'
LSR_ = '→'
LSD_ = '↓'
CAP_ = 'CAP'
HOME = 'HOME'
MIN_ = '-'
PLUS = '+'

# ボタンのレイアウト
BUTTONS = [
    [ZL__, None, None, None, None, ZR__],
    [L___, LC__, MIN_, PLUS, X___, R___],
    [None, LSU_, None, Y___, None, A___],
    [LSL_, None, LSR_, None, B___, None],
    [None, LSD_, CAP_, HOME, RC__, None],
]

# ボタンの色
BUTTON_COLORS = {
    'bg': '#343434' if platform.system() == 'Windows' else None,
    'fg': '#FFFFFF' if platform.system() == 'Windows' else None,
}


class ControllerPane(AppFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.build_ui()

    def build_ui(self):
        labelframe = ttk.Labelframe(self, text="Software-Controller")

        # Wrapper Frame
        wrapper = ttk.Frame(labelframe)

        # Left
        left_frame = tk.Frame(wrapper, bg="#56CCF2")
        left_buttons = [bs[:3] for bs in BUTTONS]
        for r, row in enumerate(left_buttons):
            for c, btn in enumerate(row):
                if btn is not None:
                    b = tk.Button(left_frame,
                                  text=btn,
                                  width=4,
                                  bg=BUTTON_COLORS['bg'],
                                  highlightbackground=BUTTON_COLORS['bg'],
                                  fg=BUTTON_COLORS['fg'])
                    b.bind("<ButtonPress>", lambda _, btn=btn: self._on_button_pushed(btn), add="")
                    b.bind("<ButtonRelease>", lambda _, btn=btn: self._on_button_released(btn), add="")
                    b.grid(row=r, column=c, padx=2, pady=2, sticky=tk.NSEW)

        # Right
        right_frame = tk.Frame(wrapper, bg="#E9514E")
        right_buttons = [bs[3:] for bs in BUTTONS]
        for r, row in enumerate(right_buttons):
            for c, btn in enumerate(row):
                if btn is not None:
                    b = tk.Button(right_frame,
                                  text=btn,
                                  width=4,
                                  bg=BUTTON_COLORS['bg'],
                                  highlightbackground=BUTTON_COLORS['bg'],
                                  fg=BUTTON_COLORS['fg'])
                    b.bind("<ButtonPress>", lambda _, btn=btn: self._on_button_pushed(btn), add="")
                    b.bind("<ButtonRelease>", lambda _, btn=btn: self._on_button_released(btn), add="")
                    b.grid(row=r, column=c, padx=2, pady=2, sticky=tk.NSEW)

        # Layout
        left_frame.pack(expand=False, fill=tk.BOTH, side=tk.LEFT)
        right_frame.pack(expand=False, fill=tk.BOTH, side=tk.LEFT)
        wrapper.pack(expand=False, fill=tk.Y, anchor=tk.CENTER)
        labelframe.pack(expand=False, fill=tk.BOTH)

    def _on_button_pushed(self, button: str):
        self.app_model.push_controller_button(button)

    def _on_button_released(self, button: str):
        self.app_model.release_controller_button(button)
