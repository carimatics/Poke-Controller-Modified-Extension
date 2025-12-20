import math
from dataclasses import dataclass
from enum import IntFlag, auto
from typing import Self

from pokecontroller.utils.math import clamp


class StickTilt(IntFlag):
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()


@dataclass(kw_only=True, frozen=True)
class StickAxisRange:
    min: int
    max: int
    neutral: int

    def clamp(self, value: int) -> int:
        return clamp(value, self.min, self.max)


@dataclass(kw_only=True, frozen=True)
class StickRange:
    x: StickAxisRange
    y: StickAxisRange


@dataclass
class StickPolar:
    degree: float
    r: float = 1.0

    @classmethod
    def of(cls, degree: float, r: float = 1.0) -> Self:
        return cls(degree % 360, clamp(r, 0.0, 1.0))

    def to_xy(self, stick_range: StickRange) -> tuple[int, int]:
        theta = math.radians(self.degree)
        x_center = (stick_range.x.max - stick_range.x.min) / 2
        y_center = (stick_range.y.max - stick_range.y.min) / 2
        x = math.ceil(x_center * math.cos(theta) * self.r + x_center)
        y = math.floor(y_center * math.sin(theta) * self.r + y_center)
        return x, y


class StickState:
    _tilt_coefficient = {
        tilt: coefficient
        for coefficient, tilt in enumerate(
            (
                # LDRU
                0b0010,  # RIGHT
                0b0011,  # UP|RIGHT
                0b0001,  # UP
                0b1001,  # UP|LEFT
                0b1000,  # LEFT
                0b1100,  # DOWN|LEFT
                0b0100,  # DOWN
                0b0110,  # DOWN|RIGHT
            )
        )
    }

    def __init__(
        self,
        stick_range: StickRange,
    ) -> None:
        self._range = stick_range
        self._x = stick_range.x.neutral
        self._y = stick_range.y.neutral
        self._is_dirty = False

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def is_dirty(self) -> bool:
        return self._is_dirty

    @classmethod
    def from_polar(cls, stick_range: StickRange, degree: float, r: float = 1.0) -> Self:
        self = cls(stick_range)
        self.tilt_by_polar(degree, r)
        return self

    def set_xy(self, x: int, y: int) -> None:
        self._set_xy(
            x=self._range.x.clamp(x),
            y=self._range.y.clamp(y),
        )

    def to_neutral(self) -> None:
        self._set_xy(
            x=self._range.x.neutral,
            y=self._range.y.neutral,
        )

    def reset(self) -> None:
        self.to_neutral()

    def clean(self) -> None:
        self._is_dirty = False

    def tilt_by_polar(self, degree: float, r: float = 1.0) -> None:
        polar = StickPolar.of(degree, r)
        self.set_xy(*polar.to_xy(self._range))

    def tilt_full(self, tilt: int) -> None:
        coefficient = self._tilt_coefficient.get(tilt, None)
        if coefficient is None:
            self._set_xy(self._range.x.neutral, self._range.y.neutral)
        else:
            self.tilt_by_polar(45.0 * coefficient)

    def negate_tilt(self, tilts: list[StickTilt]) -> None:
        x, y = self._x, self._y
        for tilt in tilts:
            if tilt == StickTilt.LEFT and x < self._range.x.neutral:
                x = self._range.x.neutral
            elif tilt == StickTilt.RIGHT and x > self._range.x.neutral:
                x = self._range.x.neutral
            elif tilt == StickTilt.DOWN and y < self._range.y.neutral:
                y = self._range.y.neutral
            elif tilt == StickTilt.UP and y > self._range.y.neutral:
                y = self._range.y.neutral
        self._set_xy(x, y)

    def get_tiltings(self) -> list[StickTilt]:
        tiltings = []
        if self._x < self._range.x.neutral:
            tiltings.append(StickTilt.LEFT)
        elif self._x > self._range.x.neutral:
            tiltings.append(StickTilt.RIGHT)
        if self._y < self._range.y.neutral:
            tiltings.append(StickTilt.DOWN)
        elif self._y > self._range.y.neutral:
            tiltings.append(StickTilt.UP)
        return tiltings

    def _set_xy(self, x: int, y: int) -> None:
        if self._x != x or self._y != y:
            self._x = x
            self._y = y
            self._is_dirty = True
