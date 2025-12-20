class DpadState:
    def __init__(self, neutral: int) -> None:
        self._neutral = neutral
        self._value = neutral

    @property
    def value(self) -> int:
        return self._value

    def push(self, hat: int) -> None:
        self._value = hat

    def release(self) -> None:
        self._value = self._neutral

    def reset(self) -> None:
        self.release()
