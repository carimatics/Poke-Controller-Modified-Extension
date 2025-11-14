from enum import IntFlag, auto


class SwitchButton(IntFlag):
    Y = auto()
    B = auto()
    A = auto()
    X = auto()
    L = auto()
    R = auto()
    ZL = auto()
    ZR = auto()
    MINUS = auto()
    PLUS = auto()
    LS = auto()
    RS = auto()
    HOME = auto()
    CAPTURE = auto()


class SwitchButtonState:
    def __init__(self):
        self.state = 0

    def reset(self):
        self.state = 0

    def push(self, buttons: list[SwitchButton]):
        for button in buttons:
            self.state |= button

    def release(self, buttons: list[SwitchButton]):
        for button in buttons:
            self.state &= ~button
