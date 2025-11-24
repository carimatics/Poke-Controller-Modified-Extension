from ....components import AppFrame

from .output import Output


class OutputsPane(AppFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # noinspection PyTypeChecker
        self.outputs: list[Output] = []

        self.build_ui()

    def build_ui(self):
        self.outputs += [
            Output(self, id=1),
            Output(self, id=2),
        ]
