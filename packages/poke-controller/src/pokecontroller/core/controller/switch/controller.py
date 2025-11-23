from .button import SwitchButtonState
from .hat import SwitchHatState
from .stick import SwitchStickState
from ...serial import Serial


class SwitchControllerState:
    def __init__(self):
        self._button = SwitchButtonState()
        self._hat = SwitchHatState()
        self._lstick = SwitchStickState()
        self._rstick = SwitchStickState()

    @property
    def button(self) -> SwitchButtonState:
        return self._button

    @property
    def hat(self) -> SwitchHatState:
        return self._hat

    @property
    def lstick(self) -> SwitchStickState:
        return self._lstick

    @property
    def rstick(self) -> SwitchStickState:
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
        lstick, rstick = ("", "")
        if state.lstick.is_dirty:
            buttons |= 0x2
            lstick = f"{format(state.lstick.x, 'x')} {format(state.lstick.y, 'x')}"
        if state.rstick.is_dirty:
            buttons |= 0x1
            rstick = f"{format(state.rstick.x, 'x')} {format(state.rstick.y, 'x')}"

        # hat
        hat = str(int(state.hat.state))

        # contract
        serialized = f"{format(buttons, '#06x')} {hat} {lstick} {rstick}"

        state.clean()
        return serialized


class SwitchController:
    def __init__(self, serial: Serial):
        self._state: SwitchControllerState = SwitchControllerState()
        self._serial: Serial = serial

    @property
    def state(self) -> SwitchControllerState:
        return self._state

    @property
    def buttons(self) -> SwitchButtonState:
        return self._state.button

    @property
    def hat(self) -> SwitchHatState:
        return self._state.hat

    @property
    def lstick(self) -> SwitchStickState:
        return self._state.lstick

    @property
    def rstick(self) -> SwitchStickState:
        return self._state.rstick

    @property
    def is_opened(self) -> bool:
        return self._serial.is_opened

    def open(self, name: str, baud_rate: int) -> None:
        self._serial.open(name, baud_rate)

    def close(self) -> None:
        self._serial.close()

    def send_state(self) -> None:
        serialized = SwitchControllerStateSerializer.serialize(self._state)
        self._serial.write_line(serialized)
