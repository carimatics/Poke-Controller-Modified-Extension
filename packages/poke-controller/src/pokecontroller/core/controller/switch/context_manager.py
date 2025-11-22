from contextlib import contextmanager
from typing import Generator

from .controller import SwitchController

from ...serial import Serial


@contextmanager
def open(serial: Serial) -> Generator[SwitchController, None, None]:
    controller = SwitchController(serial)
    try:
        controller.open()
        yield controller
    finally:
        controller.close()
