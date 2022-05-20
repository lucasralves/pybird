from typing import List, TypeVar, Union
from PyQt5.QtWidgets import QWidget, QHBoxLayout

StretchRow = TypeVar('StretchRow')

class RowWidget(QWidget):
    
    def __init__(self, children: List[Union[QWidget, StretchRow]], scale: List[int] = None) -> None:
        super().__init__()

        hbox = QHBoxLayout()

        for i in range(len(children)):
            if children[i] == StretchRow:
                hbox.addStretch()
            else:
                if scale is not None:
                    hbox.addWidget(children[i], scale[i])
                else:
                    hbox.addWidget(children[i])
        
        self.setLayout(hbox)

        return