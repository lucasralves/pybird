from typing import List
from PyQt5.QtWidgets import QScrollArea, QWidget

from pybird.gui.widgets.column_widget import ColumnWidget

class ScrollWidget(QScrollArea):

    def __init__(self, children: List[QWidget]) -> None:
        super().__init__()

        self.setWidget(ColumnWidget(children=children))

        return