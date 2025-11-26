from ..base import Command


class McuCommand(Command):
    def __init__(self, sync_name: str):
        super().__init__()
        self.sync_name = sync_name
        self.postProcess = None

    def start(self, ser, postProcess=None):
        ser.writeRow(self.sync_name)
        self.isRunning = True
        self.postProcess = postProcess

    def end(self, ser):
        ser.writeRow("end")
        self.isRunning = False
        if self.postProcess:
            self.postProcess()

    def finish(self):
        pass

    def checkIfAlive(self):
        pass
