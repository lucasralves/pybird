from PyQt5.QtWidgets import QMainWindow

from pybird.geometry.geometry import Geometry
from pybird.gui.components.charts_component import ChartsComponent

from pybird.gui.stores.store import Store

from pybird.gui.widgets.row_widget import RowWidget, StretchRow

from pybird.gui.components.controlls_component import ControllsComponent

class MainWindow(QMainWindow):

    def __init__(self, geo: Geometry) -> None:
        super().__init__()

        # Set screen
        self.setWindowTitle('Geometry')
        self.setGeometry(0, 0, 1000, 600)

        # Store
        self.store = Store(geo=geo)

        # Set view
        self.setCentralWidget(
            RowWidget(
                children=[
                    StretchRow,
                    ControllsComponent(store=self.store),
                    ChartsComponent(store=self.store),
                    StretchRow,
                ],
            )
        )