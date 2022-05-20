from typing import Optional

from pybird.geometry.main import Geometry
from pybird.mesh.main import Mesh


class Model:

    def __init__(self, name: str, description: Optional[str]) -> None:
        self.name = name
        self.description = description
        self.geo = Geometry()
        self.mesh = Mesh(self.geo)

def model(name: str, description: Optional[str] = None) -> Model:
    return Model(name, description)