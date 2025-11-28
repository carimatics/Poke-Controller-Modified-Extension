from contextlib import contextmanager
from typing import Generator

from .serial import Serial


@contextmanager
def use_serial() -> Generator[Serial, None, None]:
    serial = Serial()
    try:
        yield serial
    finally:
        serial.close()
