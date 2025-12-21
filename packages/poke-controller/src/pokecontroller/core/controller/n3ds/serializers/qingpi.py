from pokecontroller.core.controller.n3ds.state import N3dsControllerState


class N3dsControllerStateSerializer:
    @staticmethod
    def serialize(state: N3dsControllerState) -> list[int]:
        header = 0xAB
        buttons = state.button.value
        hat = state.hat.value
        stick_x = state.stick.x
        stick_y = state.stick.y
        center = 128
        touch_x = state.touch_screen.x
        touch_y = state.touch_screen.y

        return [
            header,
            buttons & 0xFF,
            (buttons >> 8) & 0xFF,
            hat,
            stick_x,
            stick_y,
            center,
            center,
            touch_x & 0xFF,
            (touch_x >> 8) & 0xFF,
            touch_y,
        ]
