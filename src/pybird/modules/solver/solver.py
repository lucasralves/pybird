from abc import ABC
from math import cos, sin
from typing import List
from numpy import ndarray, empty, array, deg2rad, double, int32, sqrt, dot, cross, argwhere, zeros
from numpy.linalg import solve, norm
from scipy.interpolate import griddata
from scipy.optimize import newton_krylov

from pybird.modules.mesh.mesh import Mesh
from pybird.modules.solver.utils.get_vertices_connection import get_vertices_connection
from pybird.modules.solver.utils.get_vertices_values import get_scalar_vertices_values, get_vector_vertices_values
from pybird.modules.solver.utils.indulced_velocity import get_Aij_and_Bi_coefs, get_point_velocity, get_Cij
from pybird.modules.helpers import warnings

class SOLVER_ABS(ABC):

    def __init__(self, mesh: Mesh, verbose: bool) -> None:
        """Stores the geometry points and curves"""
        pass
    
    def solve(self, freestream: float, alpha: float = 0.0, beta: float = 0.0) -> None:
        """Aerodynamic solver"""
        pass

class Solver(SOLVER_ABS):

    def __init__(self, mesh: Mesh, verbose: bool) -> None:
        self.__mesh = mesh
        self.__verbose = verbose

        self.source_f: ndarray = None
        self.doublet_f: ndarray = None
        self.vel_f: ndarray = None
        self.cp_f: ndarray = None
        self.transpiration_f: ndarray = None

        self.source_v: ndarray = None
        self.doublet_v: ndarray = None
        self.vel_v: ndarray = None
        self.cp_v: ndarray = None
        self.transpiration_v: ndarray = None

        return
    
    @property
    def done(self) -> True:
        return self.source_v is not None
    
    def solve(self, freestream: float,
                    alpha: float = 0,
                    beta: float = 0,
                    wake_length: float = 10.0,
                    time_step: float = 1.0) -> None:
        
        warnings.title('Aerodynamic solver', self.__verbose)
        warnings.subtitle('pre-processing', self.__verbose)

        vertices_connection = get_vertices_connection(self.__mesh)

        ############################################
        # Freestream vector
        ############################################
        self.__freestream = array([
            -freestream * cos(deg2rad(beta)) * cos(deg2rad(alpha)),
            -freestream * sin(deg2rad(beta)) * cos(deg2rad(alpha)),
            freestream * sin(deg2rad(alpha)),
        ])

        ############################################
        # Source strength
        ############################################
        self.source_f = -(self.__mesh.e3[:, 0] * self.__freestream[0] + self.__mesh.e3[:, 1] * self.__freestream[1] + self.__mesh.e3[:, 2] * self.__freestream[2])

        ############################################
        # Calculate A and B coefs
        ############################################
        self.__Aij = empty((self.__mesh.nf, self.__mesh.nf, 3), dtype=double)
        self.__Bi = empty((self.__mesh.nf, 3), dtype=double)

        get_Aij_and_Bi_coefs(self.__mesh.nf,
                             self.__mesh.faces,
                             self.__mesh.p_avg,
                             self.__mesh.p_ctrl,
                             self.__mesh.e1,
                             self.__mesh.e2,
                             self.__mesh.e3,
                             self.__mesh.p1,
                             self.__mesh.p2,
                             self.__mesh.p3,
                             self.__mesh.p4,
                             self.__mesh.area,
                             self.__mesh.max_distance,
                             self.__mesh.scale_factor,
                             self.__freestream,
                             self.source_f,
                             self.__Aij,
                             self.__Bi)
        
        ############################################
        # Calculate doublet surface without wake
        ############################################
        warnings.subtitle('solving doublet without wake', self.__verbose)
        self.__solve_linear_system()

        self.doublet_v = get_scalar_vertices_values(self.__mesh.nv, vertices_connection, self.doublet_f)
        self.__calc_surface_parameters()
        self.vel_v = get_vector_vertices_values(self.__mesh.nv, vertices_connection, self.vel_f)

        ############################################
        # Calculate wake
        ############################################
        warnings.subtitle('generating free wake', self.__verbose)

        # Find the ids of vertices in trailing edge
        wake_id_list = []
        wake_te_faces_list = []

        for i in range(self.__mesh.nte_wake):

            if self.__mesh.trailing_edge[i, 0] not in wake_id_list:
                wake_id_list.append(self.__mesh.trailing_edge[i, 0])

                ids = argwhere((self.__mesh.trailing_edge[:, 0] == self.__mesh.trailing_edge[i, 0]) | (self.__mesh.trailing_edge[:, 1] == self.__mesh.trailing_edge[i, 0]))
                if len(ids) == 1:
                    wake_te_faces_list.append([self.__mesh.trailing_edge_faces[ids[0][0], 0], self.__mesh.trailing_edge_faces[ids[0][0], 1]])
                else:
                    wake_te_faces_list.append([self.__mesh.trailing_edge_faces[ids[0][0], 0], self.__mesh.trailing_edge_faces[ids[0][0], 1], self.__mesh.trailing_edge_faces[ids[1][0], 0], self.__mesh.trailing_edge_faces[ids[1][0], 1]])
                
            if self.__mesh.trailing_edge[i, 1] not in wake_id_list:
                wake_id_list.append(self.__mesh.trailing_edge[i, 1])

                ids = argwhere((self.__mesh.trailing_edge[:, 0] == self.__mesh.trailing_edge[i, 1]) | (self.__mesh.trailing_edge[:, 1] == self.__mesh.trailing_edge[i, 1]))
                if len(ids) == 1:
                    wake_te_faces_list.append([self.__mesh.trailing_edge_faces[ids[0][0], 0], self.__mesh.trailing_edge_faces[ids[0][0], 1]])
                else:
                    wake_te_faces_list.append([self.__mesh.trailing_edge_faces[ids[0][0], 0], self.__mesh.trailing_edge_faces[ids[0][0], 1], self.__mesh.trailing_edge_faces[ids[1][0], 0], self.__mesh.trailing_edge_faces[ids[1][0], 1]])
        
        # Trailing edge size
        self.__mesh.nv_wake = len(wake_id_list)
        self.__mesh.nw_wake = int(wake_length / (time_step * freestream)) + 1

        # Trailing edge matrix ids
        self.__mesh.wake_ids = empty((self.__mesh.nte_wake, self.__mesh.nw_wake, 2), dtype=int32)

        for i in range(self.__mesh.nte_wake):

            id1 = wake_id_list.index(self.__mesh.trailing_edge[i, 0])
            id2 = wake_id_list.index(self.__mesh.trailing_edge[i, 1])

            for j in range(self.__mesh.nw_wake):
                self.__mesh.wake_ids[i, j, 0] = id1 + j * self.__mesh.nv_wake
                self.__mesh.wake_ids[i, j, 1] = id2 + j * self.__mesh.nv_wake
        
        # Trailing edge vertices
        self.__mesh.vertices_wake = empty((self.__mesh.nv_wake * self.__mesh.nw_wake, 3), dtype=double)

        for i in range(self.__mesh.nv_wake):
            self.__mesh.vertices_wake[i, :] = self.__mesh.vertices[wake_id_list[i], :]
        
        # Circulation and areas
        self.wake_circulation = empty((self.__mesh.nte_wake, self.__mesh.nw_wake - 1), dtype=double)
        self.wake_area = empty((self.__mesh.nte_wake, self.__mesh.nw_wake - 1), dtype=double)

        # Create wake
        for wake_id in range(self.__mesh.nw_wake - 1):
            print('    * section: {}/{}'.format(wake_id + 1, self.__mesh.nw_wake - 1))

            # Update wake
            self.__update_wake(time_step, wake_id_list, wake_te_faces_list, wake_id)

            # Calculate new doublet distribution
            self.__calculate_surf_wake_doublet_distribution(wake_id)


        # Surface parameters
        self.__calc_surface_parameters()

        # Vertices values
        self.source_v = get_scalar_vertices_values(self.__mesh.nv, vertices_connection, self.source_f)
        self.doublet_v = get_scalar_vertices_values(self.__mesh.nv, vertices_connection, self.doublet_f)
        self.vel_v = get_vector_vertices_values(self.__mesh.nv, vertices_connection, self.vel_f)
        self.cp_v = get_scalar_vertices_values(self.__mesh.nv, vertices_connection, self.cp_f)
        self.transpiration_v = get_scalar_vertices_values(self.__mesh.nv, vertices_connection, self.transpiration_f)

        return
    
    def __solve_linear_system(self) -> None:

        A = empty((self.__mesh.nf, self.__mesh.nf), dtype=double)
        b = empty(self.__mesh.nf, dtype=double)

        for i in range(self.__mesh.nf):
            A[i, :] = (self.__Aij[i, :, 0] * self.__mesh.e3[i, 0] + self.__Aij[i, :, 1] * self.__mesh.e3[i, 1] + self.__Aij[i, :, 2] * self.__mesh.e3[i, 2]) # * self.__mesh.scale_factor
        
        b = - (self.__Bi[:, 0] * self.__mesh.e3[:, 0] + self.__Bi[:, 1] * self.__mesh.e3[:, 1] + self.__Bi[:, 2] * self.__mesh.e3[:, 2])

        self.doublet_f = solve(A, b)

        return
    
    def __calc_surface_parameters(self) -> None:

        self.vel_f = empty((self.__mesh.nf, 3), dtype=double)
        self.cp_f = empty(self.__mesh.nf, dtype=double)
        self.transpiration_f = empty(self.__mesh.nf, dtype=double)

        # eps = 1e-8

        # for i in range(self.__mesh.nf):
            
        #     if self.__mesh.faces[i, 0] == 4:
        #         points = array([
        #             [.0, .0],
        #             [self.__mesh.p1[i, 0], self.__mesh.p1[i, 1]],
        #             [self.__mesh.p2[i, 0], self.__mesh.p2[i, 1]],
        #             [self.__mesh.p3[i, 0], self.__mesh.p3[i, 1]],
        #             [self.__mesh.p4[i, 0], self.__mesh.p4[i, 1]],
        #         ])
        #         values = array([self.doublet_f[i], self.doublet_v[self.__mesh.faces[i, 1]], self.doublet_v[self.__mesh.faces[i, 2]], self.doublet_v[self.__mesh.faces[i, 3]], self.doublet_v[self.__mesh.faces[i, 4]]])
        #     else:
        #         points = array([
        #             [.0, .0],
        #             [self.__mesh.p1[i, 0], self.__mesh.p1[i, 1]],
        #             [self.__mesh.p2[i, 0], self.__mesh.p2[i, 1]],
        #             [self.__mesh.p3[i, 0], self.__mesh.p3[i, 1]],
        #         ])
        #         values = array([self.doublet_f[i], self.doublet_v[self.__mesh.faces[i, 1]], self.doublet_v[self.__mesh.faces[i, 2]], self.doublet_v[self.__mesh.faces[i, 3]]])

        #     x_eps = array([eps, 0.0])
        #     y_eps = array([0.0, eps])

        #     vals = griddata(points, values, (x_eps, y_eps), method='cubic')

        #     vel_x = self.__mesh.e1[i, :] * ( dot(self.__mesh.e1[i, :], self.__freestream) - (vals[0] - self.doublet_f[i]) / eps )
        #     vel_y = self.__mesh.e2[i, :] * ( dot(self.__mesh.e2[i, :], self.__freestream) - (vals[1] - self.doublet_f[i]) / eps )

        #     self.vel_f[i, :] = vel_x[:] + vel_y[:]

        self.vel_f[:, 0] = dot(self.__Aij[:, :, 0], self.doublet_f) + self.__Bi[:, 0]
        self.vel_f[:, 1] = dot(self.__Aij[:, :, 1], self.doublet_f) + self.__Bi[:, 1]
        self.vel_f[:, 2] = dot(self.__Aij[:, :, 2], self.doublet_f) + self.__Bi[:, 2]

        freestream_norm = norm(self.__freestream)

        self.cp_f[:] = 1 - sqrt(self.vel_f[:, 0] * self.vel_f[:, 0] + self.vel_f[:, 1] * self.vel_f[:, 1] + self.vel_f[:, 2] * self.vel_f[:, 2]) / freestream_norm
        self.transpiration_f[:] = self.vel_f[:, 0] * self.__mesh.e3[:, 0] + self.vel_f[:, 1] * self.__mesh.e3[:, 1] + self.vel_f[:, 2] * self.__mesh.e3[:, 2]

        return
    
    def __update_wake(self, time_step: float, wake_te_ids: List[int], wake_te_faces_list: List[int], wake_id: int) -> None:

        # Create velocity matrix
        velocity = empty((self.__mesh.nv_wake * (wake_id + 1), 3), dtype=double)

        for i in range(self.__mesh.nv_wake):
            for j in range(wake_id + 1):
                if j == 0:
                    vel = zeros(3)
                    for k in range(len(wake_te_faces_list[i])):
                        vel[:] = vel[:] + self.vel_f[wake_te_faces_list[i][k], :]
                    vel[:] = vel[:] / len(wake_te_faces_list[i])
                    velocity[i + j * self.__mesh.nv_wake, :] = vel[:]

                else:
                    velocity[i + j * self.__mesh.nv_wake, :] = get_point_velocity(
                        self.__mesh.nf,
                        self.__mesh.nte_wake,
                        self.__mesh.nw_wake,
                        wake_id,
                        self.__mesh.faces,
                        self.__mesh.p_avg,
                        self.__mesh.e1,
                        self.__mesh.e2,
                        self.__mesh.e3,
                        self.__mesh.p1,
                        self.__mesh.p2,
                        self.__mesh.p3,
                        self.__mesh.p4,
                        self.__mesh.area,
                        self.__mesh.max_distance,
                        self.__freestream,
                        self.source_f,
                        self.doublet_f,
                        self.__mesh.wake_ids,
                        self.__mesh.vertices_wake,
                        self.wake_area,
                        self.wake_circulation,
                        self.__mesh.vertices_wake[i + j * self.__mesh.nv_wake, :],
                        i,
                        j,
                    )
        
        # Update
        for i in range(self.__mesh.nv_wake):
            for j in range(wake_id + 1, 0, -1):
                self.__mesh.vertices_wake[i + j * self.__mesh.nv_wake, :] = self.__mesh.vertices_wake[i + (j - 1) * self.__mesh.nv_wake, :] + time_step * velocity[i + (j - 1) * self.__mesh.nv_wake, :]
        
        if wake_id != 0:
            for i in range(self.__mesh.nte_wake):
                for j in range(wake_id, 0, -1):
                    self.wake_circulation[i, j] = self.wake_circulation[i, j - 1]
                    self.wake_area[i, j] = self.wake_area[i, j - 1]

        return
    
    def __calculate_surf_wake_doublet_distribution(self, wake_id: int):
        
        # Area
        for i in range(self.__mesh.nte_wake):
            id1 = self.__mesh.wake_ids[i, 0, 0]
            id2 = self.__mesh.wake_ids[i, 0, 1]
            id3 = self.__mesh.wake_ids[i, 1, 0]
            id4 = self.__mesh.wake_ids[i, 1, 1]
            self.wake_area[i, 0] = 0.5 * (norm(cross(self.__mesh.vertices_wake[id2, :] - self.__mesh.vertices_wake[id1, :], self.__mesh.vertices_wake[id3, :] - self.__mesh.vertices_wake[id1, :])) + norm(cross(self.__mesh.vertices_wake[id4, :] - self.__mesh.vertices_wake[id1, :], self.__mesh.vertices_wake[id3, :] - self.__mesh.vertices_wake[id1, :])))

        # Wake surface induced velocity
        self.__Cij = empty((self.__mesh.nte_wake, self.__mesh.nf, 3), dtype=double)
        
        get_Cij(
            self.__mesh.nf,
            self.__mesh.nte_wake,
            self.__mesh.nw_wake,
            self.__mesh.p_ctrl,
            self.__mesh.wake_ids,
            self.__mesh.vertices_wake,
            self.__Cij,
        )

        # Non linear system
        def func(x: ndarray):

            out = empty(self.__mesh.nf + self.__mesh.nte_wake, dtype=double)

            # Transpiration velocity
            for i in range(self.__mesh.nf):
                out[i] = - self.transpiration_f[i] + (sum(self.__Aij[i, :, 0] * x[:self.__mesh.nf]) + self.__Bi[i, 0] + sum(self.__Cij[:, i, 0] * x[self.__mesh.nf:])) * self.__mesh.e3[i, 0] + (sum(self.__Aij[i, :, 1] * x[:self.__mesh.nf]) + self.__Bi[i, 1] + sum(self.__Cij[:, i, 1] * x[self.__mesh.nf:])) * self.__mesh.e3[i, 1] + (sum(self.__Aij[i, :, 2] * x[:self.__mesh.nf]) + self.__Bi[i, 2] + sum(self.__Cij[:, i, 2] * x[self.__mesh.nf:])) * self.__mesh.e3[i, 2]
            
            # Kutta condition
            for i in range(self.__mesh.nte_wake):
                id = self.__mesh.trailing_edge_faces[i, 0]
                v1_x = sum(self.__Aij[id, :, 0] * x[:self.__mesh.nf]) + self.__Bi[id, 0] + sum(self.__Cij[:, id, 0] * x[self.__mesh.nf:])
                v1_y = sum(self.__Aij[id, :, 1] * x[:self.__mesh.nf]) + self.__Bi[id, 1] + sum(self.__Cij[:, id, 1] * x[self.__mesh.nf:])
                v1_z = sum(self.__Aij[id, :, 2] * x[:self.__mesh.nf]) + self.__Bi[id, 2] + sum(self.__Cij[:, id, 2] * x[self.__mesh.nf:])

                id = self.__mesh.trailing_edge_faces[i, 1]
                v2_x = sum(self.__Aij[id, :, 0] * x[:self.__mesh.nf]) + self.__Bi[id, 0] + sum(self.__Cij[:, id, 0] * x[self.__mesh.nf:])
                v2_y = sum(self.__Aij[id, :, 1] * x[:self.__mesh.nf]) + self.__Bi[id, 1] + sum(self.__Cij[:, id, 1] * x[self.__mesh.nf:])
                v2_z = sum(self.__Aij[id, :, 2] * x[:self.__mesh.nf]) + self.__Bi[id, 2] + sum(self.__Cij[:, id, 2] * x[self.__mesh.nf:])

                out[self.__mesh.nf + i] = (v1_x * v1_x + v1_y * v1_y + v1_z * v1_z) - (v2_x * v2_x + v2_y * v2_y + v2_z * v2_z)

            return out

        # Initial condition
        x0 = empty(self.__mesh.nf + self.__mesh.nte_wake, dtype=double)
        x0[:self.__mesh.nf] = self.doublet_f[:]
        x0[self.__mesh.nf:] = 0.0 if wake_id == 0 else self.wake_circulation[:, 0]

        f = func(x0)

        # Solve
        # sol = newton_krylov(func, x0)

        # self.doublet_f[:] = sol[:self.__mesh.nf]

        for i in range(self.__mesh.nte_wake):
            self.wake_circulation[i, 0] = 0.0 # sol[self.__mesh.nf + i]

        return