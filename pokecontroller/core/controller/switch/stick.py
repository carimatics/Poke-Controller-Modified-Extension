import math

from pokecontroller.core.controller.switch.tilt import SwitchStickTilt

xy_range: dict[str, int] = {
    "min": 0,
    "center_x": 128,
    "center_y": 127,
    "max": 255,
}


class SwitchStick:
    def __init__(self, x: int = xy_range["center_x"], y: int = xy_range["center_y"]):
        self.x = SwitchStick._normalize_xy(x)
        self.y = SwitchStick._normalize_xy(y)
        self.is_dirty = False

    def __eq__(self, other: "SwitchStick"):
        return self.x == other.x and self.y == other.y

    def set_xy(self, x: int, y: int) -> None:
        self._set_xy(
            x=SwitchStick._normalize_xy(x),
            y=SwitchStick._normalize_xy(y),
        )

    def to_neutral(self) -> None:
        self._set_xy(
            x=xy_range["center_x"],
            y=xy_range["center_y"],
        )

    def reset(self) -> None:
        self.to_neutral()

    def tilt(self, r: float, degree: float) -> None:
        x, y = self._tilt_to_xy(r, degree)
        self._set_xy(x, y)

    def tilt_by_preset(self, tilt: int) -> None:
        if 0 <= tilt < len(SwitchStick.xy_preset):
            x, y = SwitchStick.xy_preset[tilt]
            self._set_xy(x, y)

    def negate(self, tilts: list[SwitchStickTilt]) -> None:
        x = self.x
        y = self.y
        for tilt in tilts:
            if tilt == SwitchStickTilt.LEFT and x < xy_range["center_x"]:
                x = xy_range["center_x"]
            if tilt == SwitchStickTilt.RIGHT and x > xy_range["center_x"]:
                x = xy_range["center_x"]
            if tilt == SwitchStickTilt.BOTTOM and y < xy_range["center_y"]:
                y = xy_range["center_y"]
            if tilt == SwitchStickTilt.TOP and y > xy_range["center_y"]:
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

    def clean(self):
        self.is_dirty = False

    @staticmethod
    def from_polar(r: float, degree: float) -> "SwitchStick":
        x, y = SwitchStick._tilt_to_xy(r, degree)
        return SwitchStick(x, y)

    @staticmethod
    def from_cartesian(x: int, y: int) -> "SwitchStick":
        return SwitchStick(x, y)

    def _set_xy(self, x: int, y: int) -> None:
        if self.x != x or self.y != y:
            self.x = x
            self.y = y
            self.is_dirty = True

    @staticmethod
    def _tilt_to_xy(r: float, degree: float) -> tuple[int, int]:
        nr = SwitchStick._normalize_r(r)
        nd = SwitchStick._normalize_degree(degree)
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
    def _normalize_xy(value: int) -> int:
        if value < xy_range["min"]:
            return xy_range["min"]
        if value > xy_range["max"]:
            return xy_range["max"]
        return math.floor(value)

    @staticmethod
    def _generate_xy_preset() -> list[tuple[int, int]]:
        neutral = (xy_range["center_x"], xy_range["center_y"])
        right = SwitchStick._tilt_to_xy(1.0, 0.0)
        top_right = SwitchStick._tilt_to_xy(1.0, 45.0)
        top = SwitchStick._tilt_to_xy(1.0, 90.0)
        top_left = SwitchStick._tilt_to_xy(1.0, 135.0)
        left = SwitchStick._tilt_to_xy(1.0, 180.0)
        bottom_left = SwitchStick._tilt_to_xy(1.0, 225.0)
        bottom = SwitchStick._tilt_to_xy(1.0, 270.0)
        bottom_right = SwitchStick._tilt_to_xy(1.0, 315.0)

        # Accessing presets using bitwise operations.
        # xy_preset[tilt] => (x, y)
        #
        # examples:
        #     xy_preset[TOP] => top
        #     xy_preset[TOP|RIGHT] => top_right
        #     xy_preset[TOP|BOTTOM] => neutral (invalid)
        #     xy_preset[TOP|BOTTOM|LEFT] => neutral (invalid)
        return [
            neutral,  # 0000
            top,  # 0001
            right,  # 0010
            top_right,  # 0011
            bottom,  # 0100
            neutral,  # 0101
            bottom_right,  # 0110
            neutral,  # 0111
            left,  # 1000
            top_left,  # 1001
            neutral,  # 1010
            neutral,  # 1011
            bottom_left,  # 1100
            neutral,  # 1101
            neutral,  # 1110
            neutral,  # 1111
        ]

    xy_preset = _generate_xy_preset()
