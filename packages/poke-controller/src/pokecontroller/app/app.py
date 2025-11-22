from abc import ABC, abstractmethod

from .info import PokeControllerAppInfo
from .state import PokeControllerAppState


class PokeControllerApp(ABC):
    def __init__(self, info: PokeControllerAppInfo, state: PokeControllerAppState):
        self._info = info
        self._state = state

    @abstractmethod
    def run(self):
        pass
