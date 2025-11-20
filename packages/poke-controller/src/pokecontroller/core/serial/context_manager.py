from contextlib import contextmanager
from typing import Generator

from .serial import Serial


@contextmanager
def open(port: str, baudrate: int = 115200) -> Generator[Serial, None, None]:
    serial = Serial()
    try:
        serial.open(port, baudrate)
        yield serial
    finally:
        serial.close()
