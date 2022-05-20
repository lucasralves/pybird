from typing import Callable, Union
from PyQt5.QtWidgets import QDialog, QVBoxLayout

from pybird.gui.widgets.input_widget import InputWidget
from pybird.gui.widgets.button_widget import ButtonWidget

class SaveDialogComponent(QDialog):

    def __init__(self, saveFilename: Callable[[str], None], save: Callable[[], None], initialValue: Union[str, None]) -> None:
        super().__init__()

        self.setWindowTitle('Save Geometry')

        vBox = QVBoxLayout()
        vBox.addWidget(InputWidget(
            title='File',
            onChanged=saveFilename,
            initialValue=initialValue,
            isFloat=False,
        ))
        vBox.addWidget(ButtonWidget(
            title='Save',
            onPressed=save
        ))

        self.setLayout(vBox)

        return