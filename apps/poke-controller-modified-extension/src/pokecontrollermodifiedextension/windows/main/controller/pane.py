import platform
import tkinter as tk
import tkinter.ttk as ttk
from typing import Any

from ....model import AppModel
from ....values import literals as l
from ....widgets.app import AppFrame

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
BUTTONS_LAYOUT: list[list[str | None]] = [
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
    def __init__(self, master: tk.Misc, *args: Any, **kwargs: Any) -> None:
        super().__init__(master, *args, **kwargs)
        self.build_ui()

    def build_ui(self) -> None:
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

    @property
    def app_model(self) -> AppModel:
        return self.app.app_model

    def _build_grid_frame(
        self,
        frame: tk.Frame,
        button_matrix: list[list[str | None]],
    ) -> None:
        for row, buttons in enumerate(button_matrix):
            for column, button in enumerate(buttons):
                if button is None:
                    continue

                b = tk.Button(
                    frame,
                    text=button,
                    width=4,
                )
                if bg := BUTTON_COLORS.get("bg"):
                    b.config(bg=bg, highlightbackground=bg)
                if fg := BUTTON_COLORS.get("fg"):
                    b.config(fg=fg)

                def on_pushed(_: tk.Event, btn: str | None = button) -> None:
                    if btn is not None:
                        self._on_button_pushed(btn)

                def on_released(_: tk.Event, btn: str | None = button) -> None:
                    if btn is not None:
                        self._on_button_released(btn)

                b.bind("<ButtonPress>", func=on_pushed, add="")
                b.bind("<ButtonRelease>", func=on_released, add="")
                b.grid(row=row, column=column, padx=2, pady=2, sticky=tk.NSEW)

    def _on_button_pushed(self, button: str) -> None:
        self.app_model.push_controller_button(button)

    def _on_button_released(self, button: str) -> None:
        self.app_model.release_controller_button(button)
