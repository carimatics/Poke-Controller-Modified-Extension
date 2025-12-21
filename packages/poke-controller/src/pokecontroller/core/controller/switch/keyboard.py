from typing import Any

from pynput.keyboard import Key, Listener

from ...serial import Serial
from .. import StickTilt
from .button import SwitchButton
from .dpad import SwitchDpad
from .serializers.leonardo import SwitchControllerStateSerializer
from .state import SwitchControllerState

KEYMAP_JSON_ACTIONS: dict[str, dict[str, Any]] = {
    "button": {
        "y": SwitchButton.Y,
        "b": SwitchButton.B,
        "x": SwitchButton.X,
        "a": SwitchButton.A,
        "l": SwitchButton.L,
        "r": SwitchButton.R,
        "zl": SwitchButton.ZL,
        "zr": SwitchButton.ZR,
        "minus": SwitchButton.MINUS,
        "plus": SwitchButton.PLUS,
        "lclick": SwitchButton.LS,
        "rclick": SwitchButton.RS,
        "home": SwitchButton.HOME,
        "capture": SwitchButton.CAPTURE,
    },
    "direction": {
        "right": StickTilt.RIGHT,
        "up": StickTilt.UP,
        "left": StickTilt.LEFT,
        "down": StickTilt.DOWN,
        "up_right": StickTilt.UP | StickTilt.RIGHT,
        "up_left": StickTilt.UP | StickTilt.LEFT,
        "down_right": StickTilt.DOWN | StickTilt.RIGHT,
        "down_left": StickTilt.DOWN | StickTilt.LEFT,
    },
    "dpad": {
        "right": SwitchDpad.RIGHT,
        "up": SwitchDpad.UP,
        "left": SwitchDpad.LEFT,
        "down": SwitchDpad.DOWN,
        "up_right": SwitchDpad.UP_RIGHT,
        "up_left": SwitchDpad.UP_LEFT,
        "down_right": SwitchDpad.DOWN_RIGHT,
        "down_left": SwitchDpad.DOWN_LEFT,
        "neutral": SwitchDpad.NEUTRAL,
    },
}


def parse_keymap_json(key_map_json: dict[str, dict[str, str]]) -> dict[Key | str, Any]:
    parsed: dict[Key | str, Any] = {}
    for kind, value in key_map_json.items():
        for action, key in value.items():
            if isinstance(key, str) and len(key) == 1:
                parsed[key] = KEYMAP_JSON_ACTIONS[kind][action]
            elif isinstance(key, str):
                if key.isdigit():
                    parsed[key] = KEYMAP_JSON_ACTIONS[kind][action]
                else:
                    _, v = key.split(".")
                    parsed[getattr(Key, v)] = KEYMAP_JSON_ACTIONS[kind][action]
    return parsed


class SwitchKeyboard:
    def __init__(self, serial: Serial, keymap: dict[Key | str, Any]) -> None:
        self._serial = serial
        self._keymap = keymap
        self._enabled = False

        self._state = SwitchControllerState()
        self._listener: Listener | None = None
        self._current_direction: int = 0

    def start(self) -> None:
        self._enabled = True

        if self._listener is not None:
            return

        self._listener = Listener(
            on_press=self._on_press,
            on_release=self._on_release,
            daemon=True,
        )
        self._listener.start()

    def stop(self) -> None:
        self._enabled = False

        if (listener := self._listener) is None:
            return
        listener.stop()
        listener.join()
        self._listener = None

    def _on_press(self, key: Key) -> None:
        if not self._enabled:
            return

        action = self._get_action(key)
        if action is None:
            return

        if isinstance(action, SwitchButton):
            self._state.button.push([action])
        elif isinstance(action, SwitchDpad):
            self._state.hat.add(action)
        elif isinstance(action, StickTilt):
            self._current_direction |= action
            self._state.lstick.tilt_full(self._current_direction)
        self._send_state()

    def _on_release(self, key: Key) -> None:
        if not self._enabled:
            return

        action = self._get_action(key)
        if action is None:
            return

        if isinstance(action, SwitchButton):
            self._state.button.release([action])
        elif isinstance(action, SwitchDpad):
            self._state.hat.sub(action)
        elif isinstance(action, StickTilt):
            self._current_direction &= ~action
            self._state.lstick.tilt_full(self._current_direction)
        self._send_state()

    def _get_action(self, key: Key) -> Any | None:
        if key is None:
            return None
        if hasattr(key, "char") and key.char in self._keymap:
            return self._keymap[key.char]
        elif key in self._keymap:
            return self._keymap[key]
        return None

    def _send_state(self) -> None:
        serialized = SwitchControllerStateSerializer.serialize(self._state)
        self._serial.write_line(serialized)
