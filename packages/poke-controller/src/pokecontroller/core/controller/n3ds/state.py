from ..button import ButtonState
from ..dpad import DpadState
from ..stick import StickAxisRange, StickRange, StickState
from .dpad import N3dsDpad
from .touchscreen import N3dsTouchscreenState

stick_range = StickRange(
    x=StickAxisRange(min=0, max=255, neutral=128),
    y=StickAxisRange(min=0, max=255, neutral=127),
)


class N3dsControllerState:
    def __init__(self) -> None:
        self._button = ButtonState()
        self._dpad = DpadState(neutral=N3dsDpad.NEUTRAL)
        self._stick = StickState(stick_range)
        self._touchscreen = N3dsTouchscreenState()

    @property
    def button(self) -> ButtonState:
        return self._button

    @property
    def dpad(self) -> DpadState:
        return self._dpad

    @property
    def stick(self) -> StickState:
        return self._stick

    @property
    def touchscreen(self) -> N3dsTouchscreenState:
        return self._touchscreen

    def reset(self) -> None:
        self._button.reset()
        self._dpad.reset()
        self._stick.reset()
        self._touchscreen.reset()

    def clean(self) -> None:
        self._stick.clean()
