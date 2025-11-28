from contextlib import contextmanager
from typing import Generator

from ...serial import Serial
from .controller import SwitchController


@contextmanager
def use_switch_controller(serial: Serial) -> Generator[SwitchController, None, None]:
    controller = SwitchController(serial)
    try:
        yield controller
    finally:
        controller.close()
