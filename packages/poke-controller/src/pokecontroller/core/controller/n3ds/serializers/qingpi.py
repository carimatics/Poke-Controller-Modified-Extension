from pokecontroller.core.controller.n3ds.state import N3dsControllerState


class N3dsControllerStateSerializer:
    @staticmethod
    def serialize(state: N3dsControllerState) -> list[int]:
        header = 0xAB
        buttons = state.button.value
        dpad = state.dpad.value
        stick_x = state.stick.x
        stick_y = state.stick.y
        center = 128
        touch_x = state.touchscreen.x
        touch_y = state.touchscreen.y

        return [
            header,
            buttons & 0xFF,
            (buttons >> 8) & 0xFF,
            dpad,
            stick_x,
            stick_y,
            center,
            center,
            touch_x & 0xFF,
            (touch_x >> 8) & 0xFF,
            touch_y,
        ]
