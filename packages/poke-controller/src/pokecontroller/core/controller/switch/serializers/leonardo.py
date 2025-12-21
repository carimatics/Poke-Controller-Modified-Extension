from ..state import STICK_RANGE, SwitchControllerState


class SwitchControllerStateSerializer:
    @staticmethod
    def serialize(state: SwitchControllerState) -> str:
        # buttons
        buttons = state.button.value << 2

        # sticks
        y_max = STICK_RANGE.y.max
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
