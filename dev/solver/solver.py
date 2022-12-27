from abc import ABC
from scipy.optimize import fsolve
import numpy as np
from math import sin, cos

class Mesh:
    n_f: int
    n_te: int
    e3: np.ndarray
    wake_faces_te: np.ndarray # [[id1, id2], [id3, id4], ...]

class SOLVER_ABS(ABC):
    
    def __init__(self, mesh: Mesh, verbose: bool) -> None:
        """Stores the mesh model"""
        pass

    def solve(self, freestream: float,
                    alpha: float,
                    beta: float,
                    wake_length: float = None,
                    time_step: float = None,) -> None:
        """Solve the aerodynamic model"""
        pass

class Solver(SOLVER_ABS):

    def __init__(self, mesh: Mesh, verbose: bool) -> None:

        self.__mesh = mesh
        self.__verbose = verbose

        # Parâmetros nas faces
        self.sigma_f: np.ndarray = np.empty(self.__mesh.n_f, dtype=np.double)
        self.doublet_f: np.ndarray = np.empty(self.__mesh.n_f, dtype=np.double)
        self.transpiration_f: np.ndarray = np.empty(self.__mesh.n_f, dtype=np.double)

        # Coeficientes A e B
        self.__Aij: np.ndarray = np.empty((self.__mesh.n_f, 3), dtype=np.double)
        self.__Bi: np.ndarray = np.empty((self.__mesh.n_f, 3), dtype=np.double)

        return
    
    def solve(self, freestream: float,
                    alpha: float,
                    beta: float,
                    wake_length: float = 10,
                    time_step: float = 0.1) -> None:
        
        # Esteira de vórtices
        self.__n_w = int(wake_length / (freestream * time_step)) + 1
        self.wake_circulation = np.empty((self.__mesh.n_te, self.__n_w), dtype=np.double)

        # Cria o vetor do vento
        self.__freestream = np.array([
            freestream * cos(np.deg2rad(beta)) * cos(np.deg2rad(alpha)),
            freestream * sin(np.deg2rad(beta)) * cos(np.deg2rad(alpha)),
            freestream * sin(np.deg2rad(alpha)),
        ])
        
        # Calcula as fontes nas faces
        self.sigma_f = self.__mesh.e3[:, 0] * self.__freestream[:, 0] + self.__mesh.e3[:, 1] * self.__freestream[:, 1] + self.__mesh.e3[:, 2] * self.__freestream[:, 2]

        # Calcula os coeficientes A e B
        self.__calculate_coefficients()

        # Resolve o sistema linear
        self.__solve_linear_system()

        # Loop (Sistema não linear)
        for i in range(self.__n_w - 1):

            # Atualiza a esteira
            self.__update_wake()

            # Resolve o sistem não linear
            self.__solve_non_linear_system()

        return
    
    def __calculate_coefficients(self) -> None:
        return
    
    def __solve_linear_system(self) -> None:

        matrix = np.empty((self.__mesh.n_f, self.__mesh.n_f), dtype=np.double)
        array = np.empty(self.__mesh.n_f, dtype=np.double)

        for i in range(self.__mesh.n_f):
            matrix[i, :] = self.__Aij[:, 0] * self.__mesh.e3[:, 0] + self.__Aij[:, 1] * self.__mesh.e3[:, 1] + self.__Aij[:, 2] * self.__mesh.e3[:, 2]
        
        array = - (self.__Bi[:, 0] * self.__mesh.e3[:, 0] + self.__Bi[:, 1] * self.__mesh.e3[:, 1] + self.__Bi[:, 2] * self.__mesh.e3[:, 2])

        self.doublet_f = np.linalg.solve(matrix, array)
        self.transpiration_f[:] = 0.0

        return
    
    def __update_wake(self) -> None:
        return
    
    def __solve_non_linear_system(self, interaction: int) -> None:

        def f(x):

            out = np.empty(self.__mesh.n_f + self.__mesh.n_te, dtype=np.double)
            
            for i in range(self.__mesh.n_f):

                surf_doublet_normal_vel = self.__Aij[:, 0] * self.__mesh.e3[:, 0] + self.__Aij[:, 1] * self.__mesh.e3[:, 1] + self.__Aij[:, 2] * self.__mesh.e3[:, 2]
                surf_source_normal_vel = self.__Bi[i, 0] * self.__mesh.e3[i, 0] + self.__Bi[i, 1] * self.__mesh.e3[i, 1] + self.__Bi[i, 2] * self.__mesh.e3[i, 2]
                wake_doublet_normal_vel = 0.0

                out[i] = self.transpiration_f[i] - surf_doublet_normal_vel - surf_source_normal_vel - wake_doublet_normal_vel
            
            return out

        def jac(x):

            matrix = np.empty((self.__mesh.n_f + self.__mesh.n_te, self.__mesh.n_f + self.__mesh.n_te), dtype=np.double)

            return

        x0 = np.empty(self.__mesh.n_f + self.__mesh.n_te, dtype=np.double)
        x0[:self.__mesh.n_f] = self.doublet_f
        x0[self.__mesh.n_f:] = 0.0 if interaction == 0 else self.wake_circulation[:, 0]

        sol = fsolve(f, x0, fprime=jac)

        self.doublet_f = sol[:self.__mesh.n_f]
        self.wake_circulation[:, 0] = sol[self.__mesh.n_f:]

        return