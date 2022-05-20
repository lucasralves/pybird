import sys
from PyQt5.QtWidgets import QApplication

from pybird.geometry.geometry import Geometry
from pybird.gui.components.main_window import MainWindow

def showUI(geo: Geometry) -> None:
    app = QApplication(sys.argv)
    main = MainWindow(geo)
    main.show()
    sys.exit(app.exec_())
    return