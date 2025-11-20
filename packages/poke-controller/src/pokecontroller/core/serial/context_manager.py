from contextlib import contextmanager
from typing import Generator

from .serial import Serial


@contextmanager
def open(port: str, baud_rate: int) -> Generator[Serial, None, None]:
    serial = Serial()
    try:
        serial.open(port, baudrate)
        yield serial
    finally:
        serial.close()
