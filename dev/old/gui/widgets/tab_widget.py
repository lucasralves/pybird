from dataclasses import dataclass
from typing import List
from PyQt5.QtWidgets import QTabWidget, QWidget


@dataclass
class TabItem:
    item: QWidget
    name: str

class TabWidget(QTabWidget):

    def __init__(self, tabs: List[TabItem], width: float = None) -> None:
        super().__init__()

        # Set tabs
        for tab in tabs:
            self.addTab(tab.item, tab.name)
        
        if width: self.setFixedWidth(width)

        return