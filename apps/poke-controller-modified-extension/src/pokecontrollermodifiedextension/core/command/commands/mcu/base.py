from abc import ABC
from collections.abc import Callable

from ... import Sender
from ..base import Command


class McuCommand(Command, ABC):
    def __init__(self, sync_name: str):
        super().__init__()
        self.sync_name = sync_name
        self.postProcess: Callable[[], None] | None = None

    def start(
        self,
        ser: Sender,
        postProcess: Callable[[], None] | None = None,  # noqa
    ) -> None:
        ser.writeRow(self.sync_name)
        self.isRunning = True
        self.postProcess = postProcess

    def end(self, ser: Sender) -> None:
        ser.writeRow("end")
        self.isRunning = False
        if (p := self.postProcess) is not None:
            p()
