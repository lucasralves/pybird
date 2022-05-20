from typing import List, TypeVar, Union
from PyQt5.QtWidgets import QWidget, QVBoxLayout

StretchColumn = TypeVar('StretchColumn')

class ColumnWidget(QWidget):
    
    def __init__(self, children: List[Union[QWidget, StretchColumn]], scale: List[int] = None) -> None:
        super().__init__()

        vbox = QVBoxLayout()

        for i in range(len(children)):
            if children[i] == StretchColumn:
                vbox.addStretch()
            else:
                if scale is not None:
                    vbox.addWidget(children[i], scale[i])
                else:
                    vbox.addWidget(children[i])
        
        self.setLayout(vbox)

        return