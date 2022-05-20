from typing import Callable
from PyQt5.QtWidgets import QPushButton

class ButtonWidget(QPushButton):

    def __init__(self, title: str, onPressed: Callable[[None], None], width: float = None) -> None:
        super().__init__()

        self.setText(title)
        self.clicked.connect(onPressed)
        if width: self.setFixedWidth(width)

        return