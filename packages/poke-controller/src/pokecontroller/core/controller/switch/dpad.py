from enum import IntEnum

from pokecontroller.core.controller import DpadState


class SwitchDpad(IntEnum):
    UP = 0
    UP_RIGHT = 1
    RIGHT = 2
    DOWN_RIGHT = 3
    DOWN = 4
    DOWN_LEFT = 5
    LEFT = 6
    UP_LEFT = 7
    NEUTRAL = 8


DPAD_ADD: dict[int, dict[int, int]] = {
    SwitchDpad.RIGHT: {
        SwitchDpad.RIGHT: SwitchDpad.RIGHT,
        SwitchDpad.UP: SwitchDpad.UP_RIGHT,
        SwitchDpad.LEFT: SwitchDpad.NEUTRAL,
        SwitchDpad.DOWN: SwitchDpad.DOWN_RIGHT,
    },
    SwitchDpad.UP_RIGHT: {
        SwitchDpad.RIGHT: SwitchDpad.UP_RIGHT,
        SwitchDpad.UP: SwitchDpad.UP_RIGHT,
        SwitchDpad.LEFT: SwitchDpad.NEUTRAL,
        SwitchDpad.DOWN: SwitchDpad.NEUTRAL,
    },
    SwitchDpad.UP: {
        SwitchDpad.RIGHT: SwitchDpad.UP_RIGHT,
        SwitchDpad.UP: SwitchDpad.UP,
        SwitchDpad.LEFT: SwitchDpad.UP_LEFT,
        SwitchDpad.DOWN: SwitchDpad.NEUTRAL,
    },
    SwitchDpad.UP_LEFT: {
        SwitchDpad.RIGHT: SwitchDpad.NEUTRAL,
        SwitchDpad.UP: SwitchDpad.UP_LEFT,
        SwitchDpad.LEFT: SwitchDpad.UP_LEFT,
        SwitchDpad.DOWN: SwitchDpad.NEUTRAL,
    },
    SwitchDpad.LEFT: {
        SwitchDpad.RIGHT: SwitchDpad.NEUTRAL,
        SwitchDpad.UP: SwitchDpad.UP_LEFT,
        SwitchDpad.LEFT: SwitchDpad.LEFT,
        SwitchDpad.DOWN: SwitchDpad.DOWN_LEFT,
    },
    SwitchDpad.DOWN_LEFT: {
        SwitchDpad.RIGHT: SwitchDpad.NEUTRAL,
        SwitchDpad.UP: SwitchDpad.NEUTRAL,
        SwitchDpad.LEFT: SwitchDpad.DOWN_LEFT,
        SwitchDpad.DOWN: SwitchDpad.DOWN_LEFT,
    },
    SwitchDpad.DOWN: {
        SwitchDpad.RIGHT: SwitchDpad.DOWN_RIGHT,
        SwitchDpad.UP: SwitchDpad.NEUTRAL,
        SwitchDpad.LEFT: SwitchDpad.DOWN_LEFT,
        SwitchDpad.DOWN: SwitchDpad.DOWN,
    },
    SwitchDpad.DOWN_RIGHT: {
        SwitchDpad.RIGHT: SwitchDpad.DOWN_RIGHT,
        SwitchDpad.UP: SwitchDpad.NEUTRAL,
        SwitchDpad.LEFT: SwitchDpad.NEUTRAL,
        SwitchDpad.DOWN: SwitchDpad.DOWN_RIGHT,
    },
    SwitchDpad.NEUTRAL: {
        SwitchDpad.RIGHT: SwitchDpad.RIGHT,
        SwitchDpad.UP: SwitchDpad.UP,
        SwitchDpad.LEFT: SwitchDpad.LEFT,
        SwitchDpad.DOWN: SwitchDpad.DOWN,
    },
}
DPAD_SUB: dict[int, dict[int, int]] = {
    SwitchDpad.RIGHT: {
        SwitchDpad.RIGHT: SwitchDpad.NEUTRAL,
        SwitchDpad.UP: SwitchDpad.RIGHT,
        SwitchDpad.LEFT: SwitchDpad.RIGHT,
        SwitchDpad.DOWN: SwitchDpad.RIGHT,
    },
    SwitchDpad.UP_RIGHT: {
        SwitchDpad.RIGHT: SwitchDpad.UP,
        SwitchDpad.UP: SwitchDpad.RIGHT,
        SwitchDpad.LEFT: SwitchDpad.UP_RIGHT,
        SwitchDpad.DOWN: SwitchDpad.UP_RIGHT,
    },
    SwitchDpad.UP: {
        SwitchDpad.RIGHT: SwitchDpad.UP,
        SwitchDpad.UP: SwitchDpad.NEUTRAL,
        SwitchDpad.LEFT: SwitchDpad.UP,
        SwitchDpad.DOWN: SwitchDpad.UP,
    },
    SwitchDpad.UP_LEFT: {
        SwitchDpad.RIGHT: SwitchDpad.UP_LEFT,
        SwitchDpad.UP: SwitchDpad.LEFT,
        SwitchDpad.LEFT: SwitchDpad.UP,
        SwitchDpad.DOWN: SwitchDpad.UP_LEFT,
    },
    SwitchDpad.LEFT: {
        SwitchDpad.RIGHT: SwitchDpad.LEFT,
        SwitchDpad.UP: SwitchDpad.LEFT,
        SwitchDpad.LEFT: SwitchDpad.NEUTRAL,
        SwitchDpad.DOWN: SwitchDpad.LEFT,
    },
    SwitchDpad.DOWN_LEFT: {
        SwitchDpad.RIGHT: SwitchDpad.DOWN_LEFT,
        SwitchDpad.UP: SwitchDpad.DOWN_LEFT,
        SwitchDpad.LEFT: SwitchDpad.DOWN,
        SwitchDpad.DOWN: SwitchDpad.LEFT,
    },
    SwitchDpad.DOWN: {
        SwitchDpad.RIGHT: SwitchDpad.DOWN,
        SwitchDpad.UP: SwitchDpad.DOWN,
        SwitchDpad.LEFT: SwitchDpad.DOWN,
        SwitchDpad.DOWN: SwitchDpad.NEUTRAL,
    },
    SwitchDpad.DOWN_RIGHT: {
        SwitchDpad.RIGHT: SwitchDpad.DOWN,
        SwitchDpad.UP: SwitchDpad.DOWN_RIGHT,
        SwitchDpad.LEFT: SwitchDpad.DOWN_RIGHT,
        SwitchDpad.DOWN: SwitchDpad.RIGHT,
    },
    SwitchDpad.NEUTRAL: {
        SwitchDpad.RIGHT: SwitchDpad.NEUTRAL,
        SwitchDpad.UP: SwitchDpad.NEUTRAL,
        SwitchDpad.LEFT: SwitchDpad.NEUTRAL,
        SwitchDpad.DOWN: SwitchDpad.NEUTRAL,
    },
}


class SwitchDpadState(DpadState):
    def add(self, value: int) -> None:
        self._value = DPAD_ADD[self._value][value]

    def sub(self, value: int) -> None:
        self._value = DPAD_SUB[self._value][value]
