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
        self._value = 0

    @property
    def value(self) -> int:
        return self._value

    def reset(self) -> None:
        self._value = 0

    def push(self, buttons: list[SwitchButton]) -> None:
        for button in buttons:
            self._value |= button

    def release(self, buttons: list[SwitchButton]) -> None:
        for button in buttons:
            self._value &= ~button
