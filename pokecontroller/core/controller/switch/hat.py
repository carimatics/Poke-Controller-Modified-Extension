from enum import IntEnum


class SwitchHat(IntEnum):
    TOP = 0
    TOP_RIGHT = 1
    RIGHT = 2
    BOTTOM_RIGHT = 3
    BOTTOM = 4
    BOTTOM_LEFT = 5
    LEFT = 6
    TOP_LEFT = 7
    NEUTRAL = 8


class SwitchHatState:
    def __init__(self):
        self.state = SwitchHat.NEUTRAL

    def push(self, hat: SwitchHat):
        self.state = hat

    def reset(self):
        self.state = SwitchHat.NEUTRAL
