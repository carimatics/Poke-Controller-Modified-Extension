import logging
import math
import time
from typing import Protocol

import serial
from pokecontroller.core import platform

logger = logging.getLogger(__name__)


class BoolGettable(Protocol):
    def get(self) -> bool: ...


class Sender:
    def __init__(
        self,
        is_show_serial: BoolGettable,
        if_print: bool = True,
    ) -> None:
        self.ser: serial.Serial | None = None
        self.is_show_serial = is_show_serial

        self.before: str | list[int] | None = None
        self.L_holding = False
        self._L_holding = None
        self.R_holding = False
        self._R_holding = None
        self.is_print = if_print
        self.time_bef = time.perf_counter()
        self.time_aft = time.perf_counter()
        self.Buttons: list[str] = [
            "Stick.RIGHT",
            "Stick.LEFT",
            "Button.Y",
            "Button.B",
            "Button.A",
            "Button.X",
            "Button.L",
            "Button.R",
            "Button.ZL",
            "Button.ZR",
            "Button.MINUS",
            "Button.PLUS",
            "Button.LCLICK",  # noqa
            "Button.RCLICK",  # noqa
            "Button.HOME",
            "Button.CAPTURE",
        ]
        self.Hat = [
            "TOP",
            "TOP_RIGHT",
            "RIGHT",
            "BTM_RIGHT",
            "BTM",
            "BTM_LEFT",
            "LEFT",
            "TOP_LEFT",
            "CENTER",
        ]

    def openSerial(  # noqa
        self,
        portNum: int,  # noqa
        portName: str | None = None,  # noqa
        baudrate: int = 9600,
    ) -> bool:
        if portName:
            name = portName
        elif platform.is_windows():
            name = f"COM{portNum}"
        elif platform.is_macos():
            name = f"/dev/tty.usbserial-{portNum}"
        elif platform.is_linux():
            name = f"/dev/ttyUSB{portNum}"
        else:
            logger.warning("Not supported OS")
            return False

        logger.info(f"connecting to {name}({baudrate})")
        try:
            self.ser = serial.Serial(name, baudrate)
        except serial.serialutil.SerialException as e:
            logger.error("COM Port: can't be established")
            logger.error(f"{e}")
            return False

        return True

    def closeSerial(self) -> None:  # noqa
        logger.debug("Closing the serial communication")
        if (s := self.ser) is not None:
            s.close()

    def isOpened(self) -> bool:  # noqa
        logger.debug("Checking if serial communication is open")
        return True if self.ser is not None and self.ser.is_open else False

    def writeRow(  # noqa
        self,
        row: str,
        is_show: bool = False,
    ) -> None:
        if (s := self.ser) is None:
            logger.error("Serial is not open")
            return

        if (
            is_show
            and (before := self.before) is not None
            and isinstance(before, str)
            and before != "end"
        ):
            output = before.split(" ")
            self.show_input(output)

        try:
            self.time_bef = time.perf_counter()

            s.write((row + "\r\n").encode("utf-8"))
            self.time_aft = time.perf_counter()
            self.before = row
        except serial.serialutil.SerialException as e:
            logger.error(f"Error : {e}")

        # Show sending serial data
        if self.is_show_serial.get():
            logger.debug(row)

    def writeList(  # noqa
        self,
        values: list[int],
        is_show: bool = False,
    ) -> None:
        if (s := self.ser) is None:
            logger.error("Serial is not open")
            return

        try:
            self.time_bef = time.perf_counter()
            if self.before is not None and self.before != "end" and is_show:
                pass

            s.write(values)  # noqa
            self.time_aft = time.perf_counter()
            self.before = values
        except serial.serialutil.SerialException as e:
            logger.error(f"Error : {e}")
        except AttributeError as e:
            logger.error("Maybe Using a port that is not open.")
            logger.error(e)

        # Show sending serial data
        if self.is_show_serial.get():
            logger.debug(values)

    def writeRow_wo_perf_counter(  # noqa
        self,
        row: str,
        is_show: bool = False,
    ) -> None:
        if (s := self.ser) is None:
            logger.error("Serial is not open")
            return

        try:
            s.write((row + "\r\n").encode("utf-8"))
        except serial.serialutil.SerialException as e:
            logger.error(f"Error : {e}")

        # Show sending serial data
        if is_show:
            logger.debug(row)

    def show_input(self, output: list[str]) -> None:
        if not self.is_print:
            return

        # collect sender states
        (_, using_rstick), (_, using_lstick), *buttons_state = [
            (button, bool(int(output[0], 16) >> i & 1))
            for i, button in enumerate(self.Buttons)
        ]
        if (hat := self.Hat[int(output[1])]) != "CENTER":
            buttons_state.append(("Hat." + str(hat), True))
        lstick_state = [int(x, 16) for x in output[2:4]]
        rstick_state = [int(x, 16) for x in output[4:6]]
        lstick_deg = math.degrees(
            math.atan2(128 - lstick_state[1], lstick_state[0] - 128)
        )
        rstick_deg = math.degrees(
            math.atan2(128 - rstick_state[1], rstick_state[0] - 128)
        )

        # stringify buttons state
        buttons_str: str | None = None
        if buttons := [button for button, using in buttons_state if using]:
            buttons_str = f"{', '.join(buttons)}"

        # stringify stick state
        lstick_str: str | None = None
        rstick_str: str | None = None
        if using_lstick and lstick_state != [128, 128]:
            lstick_str = f"Direction(Stick.LEFT, {lstick_deg:.0f})"
        if using_rstick and rstick_state != [128, 128]:
            rstick_str = f"Direction(Stick.RIGHT, {rstick_deg:.0f})"

        # check has loggable states
        state_strs = [s for s in [buttons_str, lstick_str, rstick_str] if s is not None]
        if not state_strs:
            return

        # log
        duration = self.time_aft - self.time_bef
        args_str = (
            state_strs[0] if len(state_strs) == 1 else f"[{', '.join(state_strs)}]"
        )
        logger.debug(f"self.press({args_str}, duration={duration:.2f})")
