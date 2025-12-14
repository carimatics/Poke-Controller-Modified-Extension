from abc import ABC

from ...sender import Sender
from ..base import Command, PostProcess


class McuCommand(Command, ABC):
    def __init__(self, sync_name: str):
        super().__init__()
        self.sync_name = sync_name
        self.postProcess: PostProcess | None = None

    def start(
        self,
        ser: Sender,
        postProcess: PostProcess | None = None,  # noqa
    ) -> None:
        ser.writeRow(self.sync_name)
        self.isRunning = True
        self.postProcess = postProcess

    def end(self, ser: Sender) -> None:
        ser.writeRow("end")
        self.isRunning = False
        if (proc := self.postProcess) is not None:
            proc()
