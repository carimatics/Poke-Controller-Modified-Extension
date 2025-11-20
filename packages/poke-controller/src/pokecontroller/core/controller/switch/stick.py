from enum import IntFlag, auto
import math


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


class SwitchStickState:
    def __init__(self):
        self._x: int = xy_range["center_x"]
        self._y: int = xy_range["center_y"]
        self._is_dirty: bool = False

    def __eq__(self, other: "SwitchStickState"):
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
        normalize = SwitchStickState._normalize_value
        self._set_xy(
            x=normalize(x),
            y=normalize(y),
        )

    def to_neutral(self) -> None:
        self._set_xy(
            x=xy_range["center_x"],
            y=xy_range["center_y"],
        )

    def reset(self) -> None:
        self.to_neutral()

    def tilt_by_polar(self, r: float, degree: float) -> None:
        x, y = SwitchStickState._polar_to_xy(r, degree)
        self._set_xy(x, y)

    def tilt_by_preset(self, tilt: int) -> None:
        presets = SwitchStickState._xy_presets
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

    def calculate_tilting(self) -> list[SwitchStickTilt]:
        tilting = []
        if self.x < xy_range["center_x"]:
            tilting.append(SwitchStickTilt.LEFT)
        elif self.x > xy_range["center_x"]:
            tilting.append(SwitchStickTilt.RIGHT)
        if self.y < xy_range["center_y"]:
            tilting.append(SwitchStickTilt.BOTTOM)
        elif self.y > xy_range["center_y"]:
            tilting.append(SwitchStickTilt.TOP)
        return tilting

    def clean(self) -> None:
        self._is_dirty = False

    def _set_xy(self, x: int, y: int) -> None:
        if self._x != x or self._y != y:
            self._x, self._y, self._is_dirty = x, y, True

    @staticmethod
    def from_polar(r: float, degree: float) -> "SwitchStickState":
        x, y = SwitchStickState._polar_to_xy(r, degree)
        return SwitchStickState(x, y)

    @staticmethod
    def _polar_to_xy(r: float, degree: float) -> tuple[int, int]:
        nr = SwitchStickState._normalize_r(r if r >= 0.0 else -r)
        nd = SwitchStickState._normalize_degree(degree if r >= 0.0 else degree + 180.0)
        theta = math.radians(nd)
        x = math.ceil(127.5 * math.cos(theta) * nr + 127.5)
        y = math.floor(127.5 * math.sin(theta) * nr + 127.5)
        return x, y

    @staticmethod
    def _normalize_r(r: float) -> float:
        if r < 0.0:
            return 0.0
        if r > 1.0:
            return 1.0
        return r

    @staticmethod
    def _normalize_degree(degree: float) -> float:
        return degree % 360

    @staticmethod
    def _normalize_value(value: int) -> int:
        if value < xy_range["min"]:
            return xy_range["min"]
        if value > xy_range["max"]:
            return xy_range["max"]
        return math.floor(value)

    @staticmethod
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
        neutral = (xy_range["center_x"], xy_range["center_y"])
        right = SwitchStickState._polar_to_xy(1.0, 0.0)
        top_right = SwitchStickState._polar_to_xy(1.0, 45.0)
        top = SwitchStickState._polar_to_xy(1.0, 90.0)
        top_left = SwitchStickState._polar_to_xy(1.0, 135.0)
        left = SwitchStickState._polar_to_xy(1.0, 180.0)
        bottom_left = SwitchStickState._polar_to_xy(1.0, 225.0)
        bottom = SwitchStickState._polar_to_xy(1.0, 270.0)
        bottom_right = SwitchStickState._polar_to_xy(1.0, 315.0)

        return {
            # LBRT
            0b0000: neutral,
            0b0001: top,
            0b0010: right,
            0b0011: top_right,
            0b0100: bottom,
            0b0110: bottom_right,
            0b1000: left,
            0b1001: top_left,
            0b1100: bottom_left,
        }

    _xy_presets: dict[int, tuple[int, int]] = _generate_xy_presets()
