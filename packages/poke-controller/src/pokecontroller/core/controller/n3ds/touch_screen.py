class N3dsTouchScreenState:
    def __init__(self) -> None:
        self._x = 0
        self._y = 0

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    def touch(self, x: int, y: int) -> None:
        self._x = x
        self._y = y

    def untouch(self) -> None:
        self._x = 0
        self._y = 0

    def reset(self) -> None:
        self.untouch()
