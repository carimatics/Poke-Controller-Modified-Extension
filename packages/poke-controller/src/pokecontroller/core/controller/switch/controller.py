from ...serial import Serial
from ..button import ButtonState
from ..dpad import DpadState
from ..stick import StickState
from .serializers.leonardo import SwitchControllerStateSerializer
from .state import SwitchControllerState


class SwitchController:
    def __init__(self, serial: Serial):
        self._state: SwitchControllerState = SwitchControllerState()
        self._serial: Serial = serial

    @property
    def state(self) -> SwitchControllerState:
        return self._state

    @property
    def buttons(self) -> ButtonState:
        return self._state.button

    @property
    def hat(self) -> DpadState:
        return self._state.hat

    @property
    def lstick(self) -> StickState:
        return self._state.lstick

    @property
    def rstick(self) -> StickState:
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
