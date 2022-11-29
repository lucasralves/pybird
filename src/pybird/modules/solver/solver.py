from abc import ABC
from numpy import ndarray

from pybird.modules.mesh.mesh import Mesh

class SOLVER_ABS(ABC):

    def __init__(self, mesh: Mesh, verbose: bool) -> None:
        """Stores the geometry points and curves"""
        pass
    
    def solve(self, freestream: float, alpha: float = 0.0, beta: float = 0.0) -> None:
        """Aerodynamic solver"""
        pass

class Solver(SOLVER_ABS):

    def __init__(self, mesh: Mesh, verbose: bool) -> None:
        self.mesh = mesh
        self.__verbose = verbose

        self.source: ndarray = None
        self.doublet: ndarray = None

        return
    
    def solve(self, freestream: float, alpha: float = 0, beta: float = 0) -> None:
        return
    
