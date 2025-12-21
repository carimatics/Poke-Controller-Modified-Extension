from ..button import ButtonState
from ..stick import StickAxisRange, StickRange, StickState
from .dpad import SwitchDpad, SwitchDpadState

STICK_RANGE = StickRange(
    x=StickAxisRange(min=0, max=255, neutral=128),
    y=StickAxisRange(min=0, max=255, neutral=127),
)


class SwitchControllerState:
    def __init__(self) -> None:
        self._button = ButtonState()
        self._hat = SwitchDpadState(neutral=SwitchDpad.NEUTRAL)
        self._lstick = StickState(STICK_RANGE)
        self._rstick = StickState(STICK_RANGE)

    @property
    def button(self) -> ButtonState:
        return self._button

    @property
    def hat(self) -> SwitchDpadState:
        return self._hat

    @property
    def lstick(self) -> StickState:
        return self._lstick

    @property
    def rstick(self) -> StickState:
        return self._rstick

    def reset(self) -> None:
        self._button.reset()
        self._hat.reset()
        self._lstick.reset()
        self._rstick.reset()

    def clean(self) -> None:
        self._lstick.clean()
        self._rstick.clean()
