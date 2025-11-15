from pokecontroller.core.controller.switch.button import SwitchButtonState
from pokecontroller.core.controller.switch.hat import SwitchHatState
from pokecontroller.core.controller.switch.stick import SwitchStick
from pokecontroller.core.serial import Serial


class SwitchControllerState:
    def __init__(self):
        self.button = SwitchButtonState()
        self.hat = SwitchHatState()
        self.lstick = SwitchStick()
        self.rstick = SwitchStick()

    def reset(self):
        self.button.reset()
        self.hat.reset()
        self.lstick.reset()
        self.rstick.reset()

    def clean(self):
        self.lstick.clean()
        self.rstick.clean()


class SwitchControllerStateSerializer:
    @staticmethod
    def serialize(state: SwitchControllerState) -> str:
        # buttons
        buttons = state.button.state << 2

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
        self.state = SwitchControllerState()
        self.serial = serial

    @property
    def buttons(self):
        return self.state.button

    @property
    def hat(self):
        return self.state.hat

    @property
    def lstick(self):
        return self.state.lstick

    @property
    def rstick(self):
        return self.state.rstick

    @property
    def is_opened(self) -> bool:
        return self.serial.is_opened

    def open(self, name: str, baud_rate: int):
        self.serial.open(name, baud_rate)

    def close(self):
        self.serial.close()

    def send_state(self):
        self.serial.write_line(SwitchControllerStateSerializer.serialize(self.state))
