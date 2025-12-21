from pokecontroller.core.controller.button import ButtonState
from pokecontroller.core.controller.dpad import DpadState
from pokecontroller.core.controller.stick import StickState
from pokecontroller.core.controller.switch.serializers.leonardo import (
    SwitchControllerStateSerializer,
)
from pokecontroller.core.controller.switch.state import SwitchControllerState
from pokecontroller.core.serial import Serial


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
    def dpad(self) -> DpadState:
        return self._state.dpad

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
