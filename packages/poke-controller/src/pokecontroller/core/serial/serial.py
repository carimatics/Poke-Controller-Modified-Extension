import logging
from collections.abc import Buffer
from dataclasses import dataclass

import serial
from serial.tools import list_ports

logger = logging.getLogger(__name__)

LINESEP = "\r\n"


@dataclass
class SerialPort:
    path: str
    name: str
    description: str


def get_serial_ports() -> list[SerialPort]:
    return [
        SerialPort(
            path=port.device,
            name=port.name,
            description=port.description,
        )
        for port in list_ports.comports()
    ]


class Serial:
    def __init__(self) -> None:
        self._serial: serial.Serial | None = None

    @property
    def is_opened(self) -> bool:
        if (s := self._serial) is None:
            return False
        return s.is_open  # type: ignore[no-any-return]

    def open(self, port_path: str, baud_rate: int) -> None:
        self.close()
        self._serial = serial.Serial(port_path, baud_rate)

    def close(self) -> None:
        if (s := self._serial) is None:
            logger.debug("Serial port is not opened")
            return
        if s.is_open:
            logger.debug(f"Closing serial port: {s.port}")
            s.close()
            logger.debug(f"Serial port closed: {s.port}")
        self._serial = None

    def write(self, data: Buffer) -> None:
        if (s := self._serial) is None:
            return

        if s.is_open:
            s.write(data)

    def write_line(self, line: str) -> None:
        self.write(f"{line}{LINESEP}".encode("utf-8"))
