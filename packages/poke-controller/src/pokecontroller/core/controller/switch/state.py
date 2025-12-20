from ..button import ButtonState
from ..dpad import DpadState
from ..stick import StickAxisRange, StickRange, StickState
from .dpad import SwitchDpad

stick_range = StickRange(
    x=StickAxisRange(min=0, max=255, neutral=128),
    y=StickAxisRange(min=0, max=255, neutral=127),
)


class SwitchControllerState:
    def __init__(self) -> None:
        self._button = ButtonState()
        self._hat = DpadState(neutral=SwitchDpad.NEUTRAL)
        self._lstick = StickState(stick_range)
        self._rstick = StickState(stick_range)

    @property
    def button(self) -> ButtonState:
        return self._button

    @property
    def hat(self) -> DpadState:
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


class SwitchControllerStateSerializer:
    @staticmethod
    def serialize(state: SwitchControllerState) -> str:
        # buttons
        buttons = state.button.value << 2

        # sticks
        y_max = stick_range.y.max
        lstick, rstick = ("", "")
        if state.lstick.is_dirty:
            buttons |= 0x2
            lstick = (
                f"{format(state.lstick.x, 'x')} {format(y_max - state.lstick.y, 'x')}"
            )
        if state.rstick.is_dirty:
            buttons |= 0x1
            rstick = (
                f"{format(state.rstick.x, 'x')} {format(y_max - state.rstick.y, 'x')}"
            )

        # hat
        hat = str(int(state.hat.value))

        # contract
        serialized = f"{format(buttons, '#06x')} {hat} {lstick} {rstick}"

        state.clean()
        return serialized
