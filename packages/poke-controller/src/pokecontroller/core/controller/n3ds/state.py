from ..button import ButtonState
from ..dpad import DpadState
from ..stick import StickAxisRange, StickRange, StickState
from .dpad import N3dsDpad
from .touch_screen import N3dsTouchScreenState

stick_range = StickRange(
    x=StickAxisRange(min=0, max=255, neutral=128),
    y=StickAxisRange(min=0, max=255, neutral=127),
)


class N3dsControllerState:
    def __init__(self) -> None:
        self._button = ButtonState()
        self._hat = DpadState(neutral=N3dsDpad.NEUTRAL)
        self._stick = StickState(stick_range)
        self._touch_screen = N3dsTouchScreenState()

    @property
    def button(self) -> ButtonState:
        return self._button

    @property
    def hat(self) -> DpadState:
        return self._hat

    @property
    def stick(self) -> StickState:
        return self._stick

    @property
    def touch_screen(self) -> N3dsTouchScreenState:
        return self._touch_screen

    def reset(self) -> None:
        self._button.reset()
        self._hat.reset()
        self._stick.reset()
        self._touch_screen.reset()

    def clean(self) -> None:
        self._stick.clean()
