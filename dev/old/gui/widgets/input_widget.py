from typing import Callable, Optional
from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QHBoxLayout
from PyQt5 import QtGui


class InputWidget(QWidget):

    def __init__(self, title: str, onChanged: Callable[[str], None], initialValue: Optional[float] = None, isFloat: bool = True) -> None:
        super().__init__()

        # Set size
        self.setMaximumWidth(185)

        # Label
        label = QLabel(title)

        # Input field
        line = QLineEdit()
        line.textChanged.connect(onChanged)
        if isFloat: line.setValidator(QtGui.QDoubleValidator())
        line.setText(str(initialValue) if initialValue is not None else None)

        # Row
        vbox = QHBoxLayout(self)
        vbox.addWidget(label)
        vbox.addWidget(line)
        vbox.addStretch()
        
        return