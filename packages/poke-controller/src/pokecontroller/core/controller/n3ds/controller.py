import logging

from pokecontroller.core.controller.button import ButtonState
from pokecontroller.core.controller.dpad import DpadState
from pokecontroller.core.controller.n3ds.serializers.n3ds_controller import (
    N3dsControllerStateSerializer as N3dsControllerSerializer,
)
from pokecontroller.core.controller.n3ds.serializers.qingpi import (
    N3dsControllerStateSerializer as QingpiSerializer,
)
from pokecontroller.core.controller.n3ds.state import N3dsControllerState
from pokecontroller.core.controller.n3ds.touchscreen import N3dsTouchscreenState
from pokecontroller.core.controller.stick import StickState
from pokecontroller.core.serial import Serial

logger = logging.getLogger(__name__)


class N3dsController:
    def __init__(self, serial: Serial, fmt: str):
        self._state: N3dsControllerState = N3dsControllerState()
        self._serial: Serial = serial
        self.format = fmt

    @property
    def format(self) -> str:
        return self._format

    @format.setter
    def format(self, value: str) -> None:
        self._format = value.lower()
        self._is_qingpi = self._format == "qingpi"
        self._is_3ds_controller = self._format == "3ds controller"

    @property
    def state(self) -> N3dsControllerState:
        return self._state

    @property
    def buttons(self) -> ButtonState:
        return self._state.button

    @property
    def dpad(self) -> DpadState:
        return self._state.dpad

    @property
    def stick(self) -> StickState:
        return self._state.stick

    @property
    def touchscreen(self) -> N3dsTouchscreenState:
        return self._state.touchscreen

    @property
    def is_opened(self) -> bool:
        return self._serial.is_opened

    def open(self, name: str, baud_rate: int) -> None:
        self._serial.open(name, baud_rate)

    def close(self) -> None:
        self._serial.close()

    def send_state(self) -> None:
        if self._is_qingpi:
            serialized = QingpiSerializer.serialize(self._state)
        elif self._is_3ds_controller:
            serialized = N3dsControllerSerializer.serialize(self._state)
        else:
            logger.warning(f"Unknown format: {self._format}")
            return
        self._serial.write(serialized)  # type: ignore[arg-type]
