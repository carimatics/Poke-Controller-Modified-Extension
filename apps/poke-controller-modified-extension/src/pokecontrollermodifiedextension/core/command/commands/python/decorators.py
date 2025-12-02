from typing import Callable, Concatenate, Protocol
from functools import wraps
from time import sleep


class Pausable(Protocol):
    isPause: bool

    def show_var(self) -> None: ...

    def checkIfAlive(self) -> bool: ...


def pausable[**P, S: Pausable, R](
    func: Callable[Concatenate[S, P], R],
) -> Callable[Concatenate[S, P], R]:
    """
    メソッドを一時停止できるできるようにします
    """

    @wraps(func)
    def inner(self: S, /, *args: P.args, **kwargs: P.kwargs) -> R:
        result: R = func(self, *args, **kwargs)
        if self.isPause:
            self.show_var()
        while self.isPause:
            sleep(0.5)
            self.checkIfAlive()
        return result

    return inner
