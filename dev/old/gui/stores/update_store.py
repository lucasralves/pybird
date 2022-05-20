from typing import Callable


class UpdateStore:

    def __init__(self) -> None:
        self.topFunc: Callable[[], None] = None
        return
    
    def addTopFunc(self, func: Callable[[], None]) -> None:
        self.topFunc = func
        return

    def update(self) -> None:
        self.topFunc()
        return