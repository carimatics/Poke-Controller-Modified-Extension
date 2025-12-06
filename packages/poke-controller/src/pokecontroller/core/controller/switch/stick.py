import logging

import math
from enum import IntFlag, auto
from typing import Self

logger = logging.getLogger(__name__)


class SwitchStickTilt(IntFlag):
    TOP = auto()
    RIGHT = auto()
    BOTTOM = auto()
    LEFT = auto()


xy_range: dict[str, int] = {
    "min": 0,
    "center_x": 128,
    "center_y": 127,
    "max": 255,
}


def _normalize_range(value: int) -> int:
    if value < xy_range["min"]:
        return xy_range["min"]
    if value > xy_range["max"]:
        return xy_range["max"]
    return math.floor(value)


def _normalize_r(r: float) -> float:
    if r < 0.0:
        return 0.0
    if r > 1.0:
        return 1.0
    return r


def _normalize_degree(degree: float) -> float:
    return degree % 360


def _polar_to_xy(r: float, degree: float) -> tuple[int, int]:
    nr = _normalize_r(r if r >= 0.0 else -r)
    nd = _normalize_degree(degree if r >= 0.0 else degree + 180.0)
    theta = math.radians(nd)
    x = math.ceil(127.5 * math.cos(theta) * nr + 127.5)
    y = math.floor(127.5 * math.sin(theta) * nr + 127.5)
    return x, y


def _generate_xy_presets() -> dict[int, tuple[int, int]]:
    """
    Generate dict that accessing presets using tilt.
    _xy_preset[tilt] => (x, y)

    examples:
        _xy_preset[TOP] => top
        _xy_preset[TOP|RIGHT] => top_right
        _xy_preset[TOP|BOTTOM] => None (invalid)
        _xy_preset[TOP|BOTTOM|LEFT] => None (invalid)
    """
    # presets unneutral
    return {
        input_tilt: _polar_to_xy(1.0, 45.0 * coefficient)
        for coefficient, input_tilt in enumerate(
            (
                # LBRT
                0b0010,  # right
                0b0011,  # top_right
                0b0001,  # top
                0b1001,  # top_left
                0b1000,  # left
                0b1100,  # bottom_left
                0b0100,  # bottom
                0b0110,  # bottom_right
            )
        )
    } | {
        0b0000: (xy_range["center_x"], xy_range["center_y"]),  # neutral
    }


class SwitchStickState:
    _xy_presets: dict[int, tuple[int, int]] = _generate_xy_presets()

    def __init__(
        self,
        x: int | None = None,
        y: int | None = None,
    ) -> None:
        if x is None:
            self._x = xy_range["center_x"]
        else:
            self._x = _normalize_range(x)
        if y is None:
            self._y = xy_range["center_y"]
        else:
            self._y = _normalize_range(y)
        self._is_dirty: bool = False

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SwitchStickState):
            return NotImplemented
        return self._x == other.x and self._y == other.y

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def is_dirty(self) -> bool:
        return self._is_dirty

    def set_xy(self, x: int, y: int) -> None:
        self._set_xy(
            x=_normalize_range(x),
            y=_normalize_range(y),
        )

    def to_neutral(self) -> None:
        self._set_xy(
            x=xy_range["center_x"],
            y=xy_range["center_y"],
        )

    def reset(self) -> None:
        self.to_neutral()

    def tilt_by_polar(self, r: float, degree: float) -> None:
        x, y = _polar_to_xy(r, degree)
        self._set_xy(x, y)

    def tilt_by_preset(self, tilt: int) -> None:
        presets = self._xy_presets
        x, y = presets.get(tilt, presets[0])
        self._set_xy(x, y)

    def negate_tilt(self, tilts: list[SwitchStickTilt]) -> None:
        x, y = self._x, self._y
        for tilt in tilts:
            if tilt == SwitchStickTilt.LEFT and x < xy_range["center_x"]:
                x = xy_range["center_x"]
            elif tilt == SwitchStickTilt.RIGHT and x > xy_range["center_x"]:
                x = xy_range["center_x"]
            elif tilt == SwitchStickTilt.BOTTOM and y < xy_range["center_y"]:
                y = xy_range["center_y"]
            elif tilt == SwitchStickTilt.TOP and y > xy_range["center_y"]:
                y = xy_range["center_y"]
        self._set_xy(x, y)

    def calculate_tiltings(self) -> list[SwitchStickTilt]:
        tiltings = []
        if self.x < xy_range["center_x"]:
            tiltings.append(SwitchStickTilt.LEFT)
        elif self.x > xy_range["center_x"]:
            tiltings.append(SwitchStickTilt.RIGHT)
        if self.y < xy_range["center_y"]:
            tiltings.append(SwitchStickTilt.BOTTOM)
        elif self.y > xy_range["center_y"]:
            tiltings.append(SwitchStickTilt.TOP)
        return tiltings

    def clean(self) -> None:
        self._is_dirty = False

    def _set_xy(self, x: int, y: int) -> None:
        if self._x != x or self._y != y:
            self._x, self._y, self._is_dirty = x, y, True
            logger.debug(f"SwitchStickState: x={self._x}, y={self._y}")

    @classmethod
    def from_polar(cls, r: float, degree: float) -> Self:
        x, y = _polar_to_xy(r, degree)
        return cls(x, y)
