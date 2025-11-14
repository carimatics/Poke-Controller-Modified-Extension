import serial


class Serial:
    def __init__(self):
        self.serial = None

    @property
    def is_opened(self) -> bool:
        if self.serial is None:
            return False
        return self.serial.isOpen()

    def open(self, port_name: str, baud_rate: int) -> None:
        self.close()
        self.serial = serial.Serial(port_name, baud_rate)

    def close(self) -> None:
        if self.is_opened:
            self.serial.close()
            self.serial = None

    def write(self, data) -> None:
        self.serial.write(data)

    def write_line(self, line: str) -> None:
        self.write((line + "\r\n").encode("utf-8"))
