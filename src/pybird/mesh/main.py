from pybird.geometry.main import Geometry
from pybird.mesh.utilities.build_mesh import build_mesh


class Mesh:
    
    def __init__(self, geo: Geometry) -> None:
        self.geo = geo
    
    def build(self, size: float,
                    coeff_wing_le: float = 1., coeff_wing_te: float = 1.,
                    coeff_tail_le: float = 1., coeff_tail_te: float = 1.,
                    coeff_head: float = 1.) -> None:
        """size in meters and refinement_ratio is the between the local and background mesh"""
        self.vertices, self.edges, self.faces = build_mesh(
            self.geo,
            size,
            coeff_wing_le,
            coeff_wing_te,
            coeff_tail_le,
            coeff_tail_te,
            coeff_head,
        )