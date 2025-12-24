import logging
from typing import Protocol

import numpy as np
import pygame

from pokecontroller.core.controller import StickState
from pokecontroller.core.controller.stick import StickAxisRange
from pokecontroller.core.controller.switch.button import SwitchButton
from pokecontroller.core.controller.switch.dpad import SwitchDpad
from pokecontroller.core.controller.switch.serializers.leonardo import (
    SwitchControllerStateSerializer,
)
from pokecontroller.core.controller.switch.state import (
    STICK_RANGE as SWITCH_STICK_RANGE,
    SwitchControllerState,
)
from pokecontroller.core.serial import Serial

logger = logging.getLogger(__name__)

STICK_AXIS_RANGE = StickAxisRange(min=-1, max=1, neutral=0)
SWITCH_STICK_AXIS_RANGE = SWITCH_STICK_RANGE.x

BUTTON_MAP = {
    0: SwitchButton.A,
    1: SwitchButton.B,
    2: SwitchButton.X,
    3: SwitchButton.Y,
    4: SwitchButton.MINUS,
    5: SwitchButton.HOME,
    6: SwitchButton.PLUS,
    7: SwitchButton.LS,
    8: SwitchButton.RS,
    9: SwitchButton.L,
    10: SwitchButton.R,
    15: SwitchButton.CAPTURE,
}
DPAD_MAP = {
    11: SwitchDpad.UP,
    12: SwitchDpad.DOWN,
    13: SwitchDpad.LEFT,
    14: SwitchDpad.RIGHT,
}


class StateRecorder(Protocol):
    def record(self, state: SwitchControllerState) -> None: ...


class SwitchProController:
    def __init__(self, serial: Serial, recorder: StateRecorder) -> None:
        self._serial = serial
        self._recorder = recorder

        self._enabled = False
        self._is_running = False
        self._state = SwitchControllerState()
        self._is_dirty = False

    def start_loop(self) -> None:
        if self._is_running:
            return

        logger.info("Starting Switch Pro Controller loop")
        self._enabled = True

        pygame.joystick.init()
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

        try:
            while self._enabled:
                self._is_running = True
                events = pygame.event.get()
                self._apply_joystick(joystick)
                self._apply_events(events)
                self._record_state()
                self._send_state()
        except Exception as e:
            logger.error(f"Error in Pro Controller loop: {e}")
        finally:
            self._is_running = False
            pygame.quit()

        logger.info("Stopped Switch Pro Controller loop")

    def stop(self) -> None:
        self._enabled = False

    def _apply_joystick(self, joystick: pygame.joystick.JoystickType) -> None:
        lstick = self._state.lstick
        lx, ly = joystick.get_axis(0), joystick.get_axis(1)
        self._apply_joystick_value(lstick, (lx, ly))

        rstick = self._state.rstick
        rx, ry = joystick.get_axis(2), joystick.get_axis(3)
        self._apply_joystick_value(rstick, (rx, ry))

    def _apply_joystick_value(self, stick: StickState, xy: tuple[float, float]) -> None:
        if np.sqrt(xy[0] ** 2 + xy[1] ** 2) < 0.35:
            stick.reset()
        else:
            stick.set_xy(
                self._adjust_stick_axis(xy[0]),
                self._adjust_stick_axis(xy[1]),
            )
        if stick.is_dirty:
            self._is_dirty = True

    def _adjust_stick_axis(self, val: float) -> int:
        v = round(val, 3)
        in_min = STICK_AXIS_RANGE.min
        in_max = STICK_AXIS_RANGE.max
        out_min = SWITCH_STICK_AXIS_RANGE.min
        out_max = SWITCH_STICK_AXIS_RANGE.max
        return int((v - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

    def _apply_events(self, events: list[pygame.event.EventType]) -> None:
        for event in events:
            if event.type == pygame.JOYBUTTONDOWN:
                self._is_dirty = True
                button = event.dict["button"]
                if button in BUTTON_MAP:
                    self._state.button.push([BUTTON_MAP[button]])
                elif button in DPAD_MAP:
                    self._state.dpad.add(DPAD_MAP[button])
            elif event.type == pygame.JOYBUTTONUP:
                self._is_dirty = True
                button = event.dict["button"]
                if button in BUTTON_MAP:
                    self._state.button.release([BUTTON_MAP[button]])
                elif button in DPAD_MAP:
                    self._state.dpad.sub(DPAD_MAP[button])

    def _record_state(self) -> None:
        if self._is_dirty:
            self._recorder.record(self._state)

    def _send_state(self) -> None:
        if self._is_dirty:
            serialized = SwitchControllerStateSerializer.serialize(self._state)
            self._serial.write_line(serialized)
            self._is_dirty = False
