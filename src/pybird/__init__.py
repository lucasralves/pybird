from typing import Optional

from pybird.geometry.main import Geometry
from pybird.mesh.main import Mesh
from pybird.view.main import View


class Model:

    def __init__(self, name: str, description: Optional[str]) -> None:
        self.name = name
        self.description = description
        self.geo = Geometry()
        self.mesh = Mesh(self.geo)
        self.view = View(self.mesh)

def model(name: str, description: Optional[str] = None) -> Model:
    return Model(name, description)