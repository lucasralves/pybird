from pybird.geometry.geometry import Geometry
from pybird.gui.main import showUI

class State:

    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description
        self.geo = Geometry()
        return
    
    def geometryUI(self) -> None:
        showUI(self.geo)
        return


def model(name: str, description: str = ''):
    return State(name, description)