import platform
import tkinter as tk
import tkinter.ttk as ttk

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

class ControllerPane(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.build_ui()

    def build_ui(self):
        labelframe = ttk.Labelframe(self, text="Software-Controller")

        # Functions
        button_functions = {
            A___: lambda: print(A___),
            B___: lambda: print(B___),
            X___: lambda: print(X___),
            Y___: lambda: print(Y___),
            L___: lambda: print(L___),
            R___: lambda: print(R___),
            ZL__: lambda: print(ZL__),
            ZR__: lambda: print(ZR__),
            LC__: lambda: print(LC__),
            RC__: lambda: print(RC__),
            LSL_: lambda: print(LSL_),
            LSU_: lambda: print(LSU_),
            LSR_: lambda: print(LSR_),
            LSD_: lambda: print(LSD_),
            CAP_: lambda: print(CAP_),
            HOME: lambda: print(HOME),
            MIN_: lambda: print(MIN_),
            PLUS: lambda: print(PLUS),
        }

        # Wrapper
        frame = ttk.Frame(labelframe)

        # Left
        left_frame = tk.Frame(frame,
                              bg="#56CCF2",
                              width=200,
                              height=200)
        left_buttons = [bs[:3] for bs in BUTTONS]
        for r, row in enumerate(left_buttons):
            for c, btn in enumerate(row):
                if btn is not None:
                    b = tk.Button(left_frame,
                                  text=btn,
                                  width=5,
                                  bg=BUTTON_COLORS['bg'],
                                  highlightbackground=BUTTON_COLORS['bg'],
                                  fg=BUTTON_COLORS['fg'],
                                  command=button_functions[btn])
                    b.grid(row=r, column=c, padx=2, pady=2, sticky=tk.NSEW)

        # Right
        right_frame = tk.Frame(frame,
                               bg="#E9514E",
                               width=200,
                               height=200)
        right_buttons = [bs[3:] for bs in BUTTONS]
        for r, row in enumerate(right_buttons):
            for c, btn in enumerate(row):
                if btn is not None:
                    b = tk.Button(right_frame,
                                  text=btn,
                                  width=5,
                                  bg=BUTTON_COLORS['bg'],
                                  highlightbackground=BUTTON_COLORS['bg'],
                                  fg=BUTTON_COLORS['fg'],
                                  command=button_functions[btn])
                    b.grid(row=r, column=c, padx=2, pady=2, sticky=tk.NSEW)

        # Layout
        left_frame.pack(expand=False, fill=tk.BOTH, side=tk.LEFT)
        right_frame.pack(expand=False, fill=tk.BOTH, side=tk.LEFT)
        frame.pack(expand=False, fill=tk.Y, anchor=tk.CENTER)
        labelframe.pack(expand=False, fill=tk.BOTH)
