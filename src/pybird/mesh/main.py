from pybird.geometry.main import Geometry
from pybird.mesh.utilities.build_mesh import build_mesh


class Mesh:
    
    def __init__(self, geo: Geometry) -> None:
        self.geo = geo
    
    def build(self, size: float, refinement_ratio: float = 0.5) -> None:
        """size in meters and refinement_ratio is the between the local and background mesh"""
        build_mesh(self.geo, size, refinement_ratio)