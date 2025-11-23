from typing import Any

import serial


class Serial:
    def __init__(self):
        self._serial: serial.Serial | None = None

    @property
    def is_opened(self) -> bool:
        if self._serial is None:
            return False
        return self._serial.isOpen()

    def open(self, port_name: str, baud_rate: int) -> None:
        self.close()
        self._serial = serial.Serial(port_name, baud_rate)

    def close(self) -> None:
        if self.is_opened:
            self._serial.close()
        self._serial = None

    def write(self, data: Any) -> None:
        if self.is_opened:
            self._serial.write(data)

    def write_line(self, line: str) -> None:
        self.write((line + "\r\n").encode("utf-8"))
