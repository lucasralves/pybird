from typing import Callable, List
from PyQt5.QtWidgets import QComboBox

class DropdownWidget(QComboBox):

    def __init__(self, items: List[str], initialValue: str, onChanged: Callable[[str], None], width: float = None) -> None:
        super().__init__()

        self.onChanged = onChanged

        self.addItems(items)
        self.setCurrentText(initialValue)
        self.currentTextChanged.connect(self.onChanged)
        if width: self.setFixedWidth(width)

        return