from contextlib import contextmanager
from typing import Generator

from pokecontroller.core.serial.serial import Serial


@contextmanager
def use_serial() -> Generator[Serial, None, None]:
    serial = Serial()
    try:
        yield serial
    finally:
        serial.close()
