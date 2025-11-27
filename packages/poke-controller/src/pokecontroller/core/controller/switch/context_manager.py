from contextlib import contextmanager
from typing import Generator

from ...serial import Serial
from .controller import SwitchController


@contextmanager
def open(
    serial: Serial,
    name: str,
    baud_rate: int,
) -> Generator[SwitchController, None, None]:
    controller = SwitchController(serial)
    try:
        controller.open(name, baud_rate)
        yield controller
    finally:
        controller.close()
