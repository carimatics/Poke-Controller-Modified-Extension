import platform
import tkinter as tk
import tkinter.ttk as ttk

from ....components import AppFrame
from ....values import literals as l

A = "A"
B = "B"
X = "X"
Y = "Y"
L = "L"
R = "R"
ZL = "ZL"
ZR = "ZR"
LC = "L-C"
RC = "R-C"
LSL = "←"
LSU = "↑"
LSR = "→"
LSD = "↓"
CAP = "CAP"
HOME = "HOME"
MIN = "-"
PLUS = "+"
# @formatter:off (for PyCharm)
# fmt: off
BUTTONS_LAYOUT = [
    [ZL  , None, None, None, None, ZR  ],
    [L   , LC  , MIN , PLUS, X   , R   ],
    [None, LSU , None, Y   , None, A   ],
    [LSL , None, LSR , None, B   , None],
    [None, LSD , CAP , HOME, RC  , None],
]
# fmt: on
# @formatter:on
LEFT_FRAME_COLUMNS = 3

# ボタンの色
BUTTON_COLORS = {
    "bg": "#343434" if platform.system() == "Windows" else None,
    "fg": "#FFFFFF" if platform.system() == "Windows" else None,
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
        left_buttons = [bs[:LEFT_FRAME_COLUMNS] for bs in BUTTONS_LAYOUT]
        self._build_grid_frame(left_frame, left_buttons)

        # Right
        right_frame = tk.Frame(wrapper, bg="#E9514E")
        right_buttons = [bs[LEFT_FRAME_COLUMNS:] for bs in BUTTONS_LAYOUT]
        self._build_grid_frame(right_frame, right_buttons)

        # Layout
        left_frame.pack(expand=False, fill=l.BOTH, side=l.LEFT)
        right_frame.pack(expand=False, fill=l.BOTH, side=l.LEFT)
        wrapper.pack(expand=False, fill=l.Y, anchor=l.CENTER)
        labelframe.pack(expand=False, fill=l.BOTH)

    def _build_grid_frame(self, frame: tk.Frame, button_matrix: list[list[str]]):
        for row, buttons in enumerate(button_matrix):
            for column, button in enumerate(buttons):
                if button is None:
                    continue

                b = tk.Button(
                    frame,
                    text=button,
                    width=4,
                    bg=BUTTON_COLORS["bg"],
                    highlightbackground=BUTTON_COLORS["bg"],
                    fg=BUTTON_COLORS["fg"],
                )
                b.bind(
                    "<ButtonPress>",
                    lambda _, btn=button: self._on_button_pushed(btn),
                    add="",
                )
                b.bind(
                    "<ButtonRelease>",
                    lambda _, btn=button: self._on_button_released(btn),
                    add="",
                )
                b.grid(row=row, column=column, padx=2, pady=2, sticky=tk.NSEW)

    def _on_button_pushed(self, button: str):
        self.app_model.push_controller_button(button)

    def _on_button_released(self, button: str):
        self.app_model.release_controller_button(button)
