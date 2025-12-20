class ButtonState:
    def __init__(self) -> None:
        self._value = 0

    @property
    def value(self) -> int:
        return self._value

    def reset(self) -> None:
        self._value = 0

    def push(self, buttons: list[int]) -> None:
        for button in buttons:
            self._value |= button

    def release(self, buttons: list[int]) -> None:
        for button in buttons:
            self._value &= ~button
