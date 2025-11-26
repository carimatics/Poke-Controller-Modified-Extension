from typing import Any

import serial


class Serial:
    def __init__(self) -> None:
        self._serial: serial.Serial | None = None

    @property
    def is_opened(self) -> bool:
        if (s := self._serial) is None:
            return False
        return s.is_open  # type: ignore[no-any-return]

    def open(self, port_name: str, baud_rate: int) -> None:
        self.close()
        self._serial = serial.Serial(port_name, baud_rate)

    def close(self) -> None:
        if (s := self._serial) is None:
            return

        if s.is_open:
            s.close()
        self._serial = None

    def write(self, data: Any) -> None:
        if (s := self._serial) is None:
            return

        if s.is_open:
            s.write(data)

    def write_line(self, line: str) -> None:
        self.write((line + "\r\n").encode("utf-8"))
