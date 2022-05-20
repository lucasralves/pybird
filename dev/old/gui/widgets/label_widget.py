from PyQt5.QtWidgets import QLabel

class LabelWidget(QLabel):
    
    def __init__(self, label: str):
        super().__init__()

        self.setText(label)

        return