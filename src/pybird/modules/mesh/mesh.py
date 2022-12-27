import sys
from abc import ABC
from typing import List
from numpy import argwhere, ndarray, int32, asarray, cross, empty, double, dot, flip, copy
from numpy.linalg import norm
from math import ceil, fabs, sqrt, pi, sin, acos
import gmsh

from pybird.modules.geo.geo import Geometry
from pybird.modules.helpers import warnings
from pybird.modules.mesh.models.refinement_model import RefinementModel

class MESH_ABS(ABC):

    def __init__(self, geo: Geometry, verbose: bool) -> None:
        """Stores the geometry points and curves"""
        pass
    
    def build(self) -> None:
        """Build the mesh"""
        pass

class Mesh(MESH_ABS):

    def __init__(self, geo: Geometry, verbose: bool) -> None:
        self.__geo = geo
        self.__verbose = verbose
        return

    def build(self, refinement: RefinementModel) -> None:

        vertices, faces3, faces4, trailing_edge_list = self.__create_mesh(refinement)
        
        self.vertices: ndarray = None
        self.faces: ndarray = None
        self.trailing_edge: ndarray = None

        self.vertices, self.faces, self.trailing_edge = self.__correct_vertices_ids(vertices, faces3, faces4, trailing_edge_list)

        self.nf = len(self.faces)
        self.nv = self.vertices.shape[0]
        self.nte_wake = self.trailing_edge.shape[0]

        # Find trailing edge faces
        self.trailing_edge_faces = empty((self.nte_wake, 2), dtype=int32)

        for i in range(self.nte_wake):
            check1 = (self.faces[:, 1] == self.trailing_edge[i, 0]) | (self.faces[:, 2] == self.trailing_edge[i, 0]) | (self.faces[:, 3] == self.trailing_edge[i, 0]) | (self.faces[:, 4] == self.trailing_edge[i, 0])
            check2 = (self.faces[:, 1] == self.trailing_edge[i, 1]) | (self.faces[:, 2] == self.trailing_edge[i, 1]) | (self.faces[:, 3] == self.trailing_edge[i, 1]) | (self.faces[:, 4] == self.trailing_edge[i, 1])
            index = argwhere(check1 & check2)
            self.trailing_edge_faces[i, 0] = index[0][0]
            self.trailing_edge_faces[i, 1] = index[1][0]
        
        self.p_avg = empty((self.nf, 3), dtype=double)
        self.p_ctrl = empty((self.nf, 3), dtype=double)
        self.e1 = empty((self.nf, 3), dtype=double)
        self.e2 = empty((self.nf, 3), dtype=double)
        self.e3 = empty((self.nf, 3), dtype=double)
        self.p1 = empty((self.nf, 2), dtype=double)
        self.p2 = empty((self.nf, 2), dtype=double)
        self.p3 = empty((self.nf, 2), dtype=double)
        self.p4 = empty((self.nf, 2), dtype=double)
        self.area = empty(self.nf, dtype=double)
        self.max_distance = empty(self.nf, dtype=double)
        self.scale_factor = empty(self.nf, dtype=double)

        self.__calculate_faces_params()

        self.nv_wake: int = -1
        self.nw_wake: int = -1
        self.wake_ids: ndarray = None
        self.vertices_wake: ndarray = None

        return

    def __calculate_faces_params(self) -> None:

        p1_local = empty(2, dtype=double)
        p2_local = empty(2, dtype=double)
        p3_local = empty(2, dtype=double)
        p4_local = empty(2, dtype=double)

        for i in range(self.nf):

            # Points
            p1 = self.vertices[self.faces[i, 1], :]
            p2 = self.vertices[self.faces[i, 2], :]
            p3 = self.vertices[self.faces[i, 3], :]

            if self.faces[i, 0] == 4:
                p4 = self.vertices[self.faces[i, 4], :]
            
            # Face center
            if self.faces[i, 0] == 3:
                p_avg = (1 / 3) * (p1 + p2 + p3)
            else:
                p_avg = 0.25 * (p1 + p2 + p3 + p4)

            # Base vectors
            # e3
            if self.faces[i, 0] == 4:
                v1 = p2 - p4
                v2 = p3 - p1
            else:
                v1 = p2 - p1
                v2 = p3 - p1
            
            n = cross(v1, v2)
            n_norm = norm(n)

            e3 = n / n_norm

            # e1
            n[:] = 1.0

            if fabs(e3[0] > 1e-2):
                n[0] = - (e3[1] * n[1] + e3[2] * n[2]) / e3[0]
            else:
                if fabs(e3[1] > 1e-2):
                    n[1] = - (e3[0] * n[0] + e3[2] * n[2]) / e3[1]
                else:
                    n[2] = - (e3[1] * n[1] + e3[0] * n[0]) / e3[2]
            
            n_norm = norm(n)

            e1 = n / n_norm

            # e2
            e2 = cross(e3, e1)

            # Control point
            p_ctrl = p_avg + e3 * 1e-12

            # Local points
            v1 = p1 - p_avg
            v2 = p2 - p_avg
            v3 = p3 - p_avg

            p1_local[0] = dot(e1, v1)
            p1_local[1] = dot(e2, v1)

            p2_local[0] = dot(e1, v2)
            p2_local[1] = dot(e2, v2)

            p3_local[0] = dot(e1, v3)
            p3_local[1] = dot(e2, v3)

            if self.faces[i, 0] == 4:
                v4 = p4 - p_avg

                p4_local[0] = dot(e1, v4)
                p4_local[1] = dot(e2, v4)

            if self.faces[i, 0] == 4:
                area = self.__triangule_area(p1, p2, p3) + self.__triangule_area(p1, p3, p4)
            else:
                area = self.__triangule_area(p1, p2, p3)

            max_distance = 10 * 2 * sqrt(area / pi)

            # Min. distance
            min_list = [
                norm(v1 + dot(v1, v2 - v1) * (v2 - v1) / norm(v2 - v1)),
                norm(v2 + dot(v2, v3 - v2) * (v3 - v2) / norm(v3 - v2)),
                norm(v3 + dot(v3, v4 - v3) * (v4 - v3) / norm(v4 - v3)),
            ]
            
            if self.faces[i, 0] == 4:
                min_list.append(norm(v4 + dot(v4, v1 - v4) * (v1 - v4) / norm(v1 - v4)))
            
            scale_factor = min(min_list)

            # Save
            self.p_avg[i, :] = p_avg[:]
            self.p_ctrl[i, :] = p_ctrl[:]
            self.e1[i, :] = e1[:]
            self.e2[i, :] = e2[:]
            self.e3[i, :] = e3[:]
            self.p1[i, :] = p1_local[:]
            self.p2[i, :] = p2_local[:]
            self.p3[i, :] = p3_local[:]
            self.p4[i, :] = p4_local[:]
            self.area[i] = area
            self.max_distance[i] = max_distance
            self.scale_factor[i] = scale_factor
        
        return
    
    def __triangule_area(self, p1: ndarray, p2: ndarray, p3: ndarray) -> float:
        return 0.5 * fabs(p1[0] * p2[1] + p2[0] * p3[1] + p3[0] * p1[1] - p1[1] * p2[0] - p2[1] * p3[0] - p3[1] * p1[0])

    def __flip(self, a: List[int]) -> List[int]:

        l = []
        for val in a:
            l.append(-val)
        l.reverse()

        return l

    def __create_mesh(self, refinement: RefinementModel) -> List:

        warnings.title('Building mesh', self.__verbose)

        gmsh.initialize()
        gmsh.option.setNumber('General.Verbosity', 1)

        #------------------------------------------#
        # Points                                   #
        #------------------------------------------#
        p_1e = gmsh.model.geo.add_point(self.__geo.p1e[0], self.__geo.p1e[1], self.__geo.p1e[2])
        p_2e = gmsh.model.geo.add_point(self.__geo.p2e[0], self.__geo.p2e[1], self.__geo.p2e[2])
        p_3e = gmsh.model.geo.add_point(self.__geo.p3e[0], self.__geo.p3e[1], self.__geo.p3e[2])
        p_4e = gmsh.model.geo.add_point(self.__geo.p4e[0], self.__geo.p4e[1], self.__geo.p4e[2])
        p_5e = gmsh.model.geo.add_point(self.__geo.p5e[0], self.__geo.p5e[1], self.__geo.p5e[2])
        p_6e = gmsh.model.geo.add_point(self.__geo.p6e[0], self.__geo.p6e[1], self.__geo.p6e[2])
        p_7e = gmsh.model.geo.add_point(self.__geo.p7e[0], self.__geo.p7e[1], self.__geo.p7e[2])
        p_8e = gmsh.model.geo.add_point(self.__geo.p8e[0], self.__geo.p8e[1], self.__geo.p8e[2])
        p_9e = gmsh.model.geo.add_point(self.__geo.p9e[0], self.__geo.p9e[1], self.__geo.p9e[2])
        p_10e = gmsh.model.geo.add_point(self.__geo.p10e[0], self.__geo.p10e[1], self.__geo.p10e[2])
        p_11e = gmsh.model.geo.add_point(self.__geo.p11e[0], self.__geo.p11e[1], self.__geo.p11e[2])
        p_12e = gmsh.model.geo.add_point(self.__geo.p12e[0], self.__geo.p12e[1], self.__geo.p12e[2])
        p_13e = gmsh.model.geo.add_point(self.__geo.p13e[0], self.__geo.p13e[1], self.__geo.p13e[2])
        p_14e = gmsh.model.geo.add_point(self.__geo.p14e[0], self.__geo.p14e[1], self.__geo.p14e[2])
        p_15e = gmsh.model.geo.add_point(self.__geo.p15e[0], self.__geo.p15e[1], self.__geo.p15e[2])
        p_16e = gmsh.model.geo.add_point(self.__geo.p16e[0], self.__geo.p16e[1], self.__geo.p16e[2])
        p_17e = gmsh.model.geo.add_point(self.__geo.p17e[0], self.__geo.p17e[1], self.__geo.p17e[2])
        p_18e = gmsh.model.geo.add_point(self.__geo.p18e[0], self.__geo.p18e[1], self.__geo.p18e[2])
        p_19e = gmsh.model.geo.add_point(self.__geo.p19e[0], self.__geo.p19e[1], self.__geo.p19e[2])
        p_20e = gmsh.model.geo.add_point(self.__geo.p20e[0], self.__geo.p20e[1], self.__geo.p20e[2])
        p_21e = gmsh.model.geo.add_point(self.__geo.p21e[0], self.__geo.p21e[1], self.__geo.p21e[2])
        p_22e = gmsh.model.geo.add_point(self.__geo.p22e[0], self.__geo.p22e[1], self.__geo.p22e[2])
        p_23e = gmsh.model.geo.add_point(self.__geo.p23e[0], self.__geo.p23e[1], self.__geo.p23e[2])
        p_24e = gmsh.model.geo.add_point(self.__geo.p24e[0], self.__geo.p24e[1], self.__geo.p24e[2])
        p_25e = gmsh.model.geo.add_point(self.__geo.p25e[0], self.__geo.p25e[1], self.__geo.p25e[2])

        c_1e = gmsh.model.geo.add_point(self.__geo.c1e[0], self.__geo.c1e[1], self.__geo.c1e[2])
        c_2e = gmsh.model.geo.add_point(self.__geo.c2e[0], self.__geo.c2e[1], self.__geo.c2e[2])
        c_3e = gmsh.model.geo.add_point(self.__geo.c3e[0], self.__geo.c3e[1], self.__geo.c3e[2])
        c_4e = gmsh.model.geo.add_point(self.__geo.c4e[0], self.__geo.c4e[1], self.__geo.c4e[2])
        c_5e = gmsh.model.geo.add_point(self.__geo.c5e[0], self.__geo.c5e[1], self.__geo.c5e[2])
        c_6e = gmsh.model.geo.add_point(self.__geo.c6e[0], self.__geo.c6e[1], self.__geo.c6e[2])
        c_7e = gmsh.model.geo.add_point(self.__geo.c7e[0], self.__geo.c7e[1], self.__geo.c7e[2])
        c_8e = gmsh.model.geo.add_point(self.__geo.c8e[0], self.__geo.c8e[1], self.__geo.c8e[2])
        c_9e = gmsh.model.geo.add_point(self.__geo.c9e[0], self.__geo.c9e[1], self.__geo.c9e[2])
        c_10e = gmsh.model.geo.add_point(self.__geo.c10e[0], self.__geo.c10e[1], self.__geo.c10e[2])
        c_11e = gmsh.model.geo.add_point(self.__geo.c11e[0], self.__geo.c11e[1], self.__geo.c11e[2])
        c_12e = gmsh.model.geo.add_point(self.__geo.c12e[0], self.__geo.c12e[1], self.__geo.c12e[2])
        c_13e = gmsh.model.geo.add_point(self.__geo.c13e[0], self.__geo.c13e[1], self.__geo.c13e[2])
        c_14e = gmsh.model.geo.add_point(self.__geo.c14e[0], self.__geo.c14e[1], self.__geo.c14e[2])
        c_15e = gmsh.model.geo.add_point(self.__geo.c15e[0], self.__geo.c15e[1], self.__geo.c15e[2])
        c_16e = gmsh.model.geo.add_point(self.__geo.c16e[0], self.__geo.c16e[1], self.__geo.c16e[2])
        c_17e = gmsh.model.geo.add_point(self.__geo.c17e[0], self.__geo.c17e[1], self.__geo.c17e[2])
        c_18e = gmsh.model.geo.add_point(self.__geo.c18e[0], self.__geo.c18e[1], self.__geo.c18e[2])
        c_19e = gmsh.model.geo.add_point(self.__geo.c19e[0], self.__geo.c19e[1], self.__geo.c19e[2])
        c_20e = gmsh.model.geo.add_point(self.__geo.c20e[0], self.__geo.c20e[1], self.__geo.c20e[2])
        c_21e = gmsh.model.geo.add_point(self.__geo.c21e[0], self.__geo.c21e[1], self.__geo.c21e[2])

        p_1d = gmsh.model.geo.add_point(self.__geo.p1d[0], self.__geo.p1d[1], self.__geo.p1d[2])
        p_2d = gmsh.model.geo.add_point(self.__geo.p2d[0], self.__geo.p2d[1], self.__geo.p2d[2])
        p_3d = gmsh.model.geo.add_point(self.__geo.p3d[0], self.__geo.p3d[1], self.__geo.p3d[2])
        p_4d = gmsh.model.geo.add_point(self.__geo.p4d[0], self.__geo.p4d[1], self.__geo.p4d[2])
        p_5d = gmsh.model.geo.add_point(self.__geo.p5d[0], self.__geo.p5d[1], self.__geo.p5d[2])
        p_6d = gmsh.model.geo.add_point(self.__geo.p6d[0], self.__geo.p6d[1], self.__geo.p6d[2])
        p_7d = gmsh.model.geo.add_point(self.__geo.p7d[0], self.__geo.p7d[1], self.__geo.p7d[2])
        p_8d = gmsh.model.geo.add_point(self.__geo.p8d[0], self.__geo.p8d[1], self.__geo.p8d[2])
        p_9d = gmsh.model.geo.add_point(self.__geo.p9d[0], self.__geo.p9d[1], self.__geo.p9d[2])
        p_10d = gmsh.model.geo.add_point(self.__geo.p10d[0], self.__geo.p10d[1], self.__geo.p10d[2])
        p_11d = gmsh.model.geo.add_point(self.__geo.p11d[0], self.__geo.p11d[1], self.__geo.p11d[2])
        p_12d = gmsh.model.geo.add_point(self.__geo.p12d[0], self.__geo.p12d[1], self.__geo.p12d[2])
        p_13d = gmsh.model.geo.add_point(self.__geo.p13d[0], self.__geo.p13d[1], self.__geo.p13d[2])
        p_14d = gmsh.model.geo.add_point(self.__geo.p14d[0], self.__geo.p14d[1], self.__geo.p14d[2])
        p_15d = gmsh.model.geo.add_point(self.__geo.p15d[0], self.__geo.p15d[1], self.__geo.p15d[2])
        p_16d = gmsh.model.geo.add_point(self.__geo.p16d[0], self.__geo.p16d[1], self.__geo.p16d[2])
        p_17d = gmsh.model.geo.add_point(self.__geo.p17d[0], self.__geo.p17d[1], self.__geo.p17d[2])
        p_18d = gmsh.model.geo.add_point(self.__geo.p18d[0], self.__geo.p18d[1], self.__geo.p18d[2])
        p_19d = gmsh.model.geo.add_point(self.__geo.p19d[0], self.__geo.p19d[1], self.__geo.p19d[2])
        p_20d = gmsh.model.geo.add_point(self.__geo.p20d[0], self.__geo.p20d[1], self.__geo.p20d[2])
        p_21d = gmsh.model.geo.add_point(self.__geo.p21d[0], self.__geo.p21d[1], self.__geo.p21d[2])
        p_22d = gmsh.model.geo.add_point(self.__geo.p22d[0], self.__geo.p22d[1], self.__geo.p22d[2])
        p_23d = gmsh.model.geo.add_point(self.__geo.p23d[0], self.__geo.p23d[1], self.__geo.p23d[2])
        p_24d = gmsh.model.geo.add_point(self.__geo.p24d[0], self.__geo.p24d[1], self.__geo.p24d[2])
        p_25d = gmsh.model.geo.add_point(self.__geo.p25d[0], self.__geo.p25d[1], self.__geo.p25d[2])

        c_1d = gmsh.model.geo.add_point(self.__geo.c1d[0], self.__geo.c1d[1], self.__geo.c1d[2])
        c_2d = gmsh.model.geo.add_point(self.__geo.c2d[0], self.__geo.c2d[1], self.__geo.c2d[2])
        c_3d = gmsh.model.geo.add_point(self.__geo.c3d[0], self.__geo.c3d[1], self.__geo.c3d[2])
        c_4d = gmsh.model.geo.add_point(self.__geo.c4d[0], self.__geo.c4d[1], self.__geo.c4d[2])
        c_5d = gmsh.model.geo.add_point(self.__geo.c5d[0], self.__geo.c5d[1], self.__geo.c5d[2])
        c_6d = gmsh.model.geo.add_point(self.__geo.c6d[0], self.__geo.c6d[1], self.__geo.c6d[2])
        c_7d = gmsh.model.geo.add_point(self.__geo.c7d[0], self.__geo.c7d[1], self.__geo.c7d[2])
        c_8d = gmsh.model.geo.add_point(self.__geo.c8d[0], self.__geo.c8d[1], self.__geo.c8d[2])
        c_9d = gmsh.model.geo.add_point(self.__geo.c9d[0], self.__geo.c9d[1], self.__geo.c9d[2])
        c_10d = gmsh.model.geo.add_point(self.__geo.c10d[0], self.__geo.c10d[1], self.__geo.c10d[2])
        c_11d = gmsh.model.geo.add_point(self.__geo.c11d[0], self.__geo.c11d[1], self.__geo.c11d[2])
        c_12d = gmsh.model.geo.add_point(self.__geo.c12d[0], self.__geo.c12d[1], self.__geo.c12d[2])
        c_13d = gmsh.model.geo.add_point(self.__geo.c13d[0], self.__geo.c13d[1], self.__geo.c13d[2])
        c_14d = gmsh.model.geo.add_point(self.__geo.c14d[0], self.__geo.c14d[1], self.__geo.c14d[2])
        c_15d = gmsh.model.geo.add_point(self.__geo.c15d[0], self.__geo.c15d[1], self.__geo.c15d[2])
        c_16d = gmsh.model.geo.add_point(self.__geo.c16d[0], self.__geo.c16d[1], self.__geo.c16d[2])
        c_17d = gmsh.model.geo.add_point(self.__geo.c17d[0], self.__geo.c17d[1], self.__geo.c17d[2])
        c_18d = gmsh.model.geo.add_point(self.__geo.c18d[0], self.__geo.c18d[1], self.__geo.c18d[2])
        c_19d = gmsh.model.geo.add_point(self.__geo.c19d[0], self.__geo.c19d[1], self.__geo.c19d[2])
        c_20d = gmsh.model.geo.add_point(self.__geo.c20d[0], self.__geo.c20d[1], self.__geo.c20d[2])
        c_21d = gmsh.model.geo.add_point(self.__geo.c21d[0], self.__geo.c21d[1], self.__geo.c21d[2])

        p_26e = gmsh.model.geo.add_point(self.__geo.p26e[0], self.__geo.p26e[1], self.__geo.p26e[2])
        p_26d = gmsh.model.geo.add_point(self.__geo.p26d[0], self.__geo.p26d[1], self.__geo.p26d[2])
        p_27e = gmsh.model.geo.add_point(self.__geo.p27e[0], self.__geo.p27e[1], self.__geo.p27e[2])
        p_27d = gmsh.model.geo.add_point(self.__geo.p27d[0], self.__geo.p27d[1], self.__geo.p27d[2])

        p_28 = gmsh.model.geo.add_point(self.__geo.p28[0], self.__geo.p28[1], self.__geo.p28[2])
        p_29 = gmsh.model.geo.add_point(self.__geo.p29[0], self.__geo.p29[1], self.__geo.p29[2])
        p_30 = gmsh.model.geo.add_point(self.__geo.p30[0], self.__geo.p30[1], self.__geo.p30[2])
        p_31 = gmsh.model.geo.add_point(self.__geo.p31[0], self.__geo.p31[1], self.__geo.p31[2])
        p_32 = gmsh.model.geo.add_point(self.__geo.p32[0], self.__geo.p32[1], self.__geo.p32[2])
        p_33 = gmsh.model.geo.add_point(self.__geo.p33[0], self.__geo.p33[1], self.__geo.p33[2])
        p_34 = gmsh.model.geo.add_point(self.__geo.p34[0], self.__geo.p34[1], self.__geo.p34[2])
        p_35 = gmsh.model.geo.add_point(self.__geo.p35[0], self.__geo.p35[1], self.__geo.p35[2])
        p_36 = gmsh.model.geo.add_point(self.__geo.p36[0], self.__geo.p36[1], self.__geo.p36[2])
        p_37 = gmsh.model.geo.add_point(self.__geo.p37[0], self.__geo.p37[1], self.__geo.p37[2])

        c_22e = gmsh.model.geo.add_point(self.__geo.c22e[0], self.__geo.c22e[1], self.__geo.c22e[2])
        c_23e = gmsh.model.geo.add_point(self.__geo.c23e[0], self.__geo.c23e[1], self.__geo.c23e[2])
        c_24e = gmsh.model.geo.add_point(self.__geo.c24e[0], self.__geo.c24e[1], self.__geo.c24e[2])
        c_25e = gmsh.model.geo.add_point(self.__geo.c25e[0], self.__geo.c25e[1], self.__geo.c25e[2])
        c_22d = gmsh.model.geo.add_point(self.__geo.c22d[0], self.__geo.c22d[1], self.__geo.c22d[2])
        c_23d = gmsh.model.geo.add_point(self.__geo.c23d[0], self.__geo.c23d[1], self.__geo.c23d[2])
        c_24d = gmsh.model.geo.add_point(self.__geo.c24d[0], self.__geo.c24d[1], self.__geo.c24d[2])
        c_25d = gmsh.model.geo.add_point(self.__geo.c25d[0], self.__geo.c25d[1], self.__geo.c25d[2])

        c_26 = gmsh.model.geo.add_point(self.__geo.c26[0], self.__geo.c26[1], self.__geo.c26[2])
        c_27 = gmsh.model.geo.add_point(self.__geo.c27[0], self.__geo.c27[1], self.__geo.c27[2])
        c_28 = gmsh.model.geo.add_point(self.__geo.c28[0], self.__geo.c28[1], self.__geo.c28[2])
        c_29 = gmsh.model.geo.add_point(self.__geo.c29[0], self.__geo.c29[1], self.__geo.c29[2])
        c_30 = gmsh.model.geo.add_point(self.__geo.c30[0], self.__geo.c30[1], self.__geo.c30[2])
        c_31 = gmsh.model.geo.add_point(self.__geo.c31[0], self.__geo.c31[1], self.__geo.c31[2])
        c_32 = gmsh.model.geo.add_point(self.__geo.c32[0], self.__geo.c32[1], self.__geo.c32[2])
        c_33 = gmsh.model.geo.add_point(self.__geo.c33[0], self.__geo.c33[1], self.__geo.c33[2])
        c_34 = gmsh.model.geo.add_point(self.__geo.c34[0], self.__geo.c34[1], self.__geo.c34[2])
        c_35 = gmsh.model.geo.add_point(self.__geo.c35[0], self.__geo.c35[1], self.__geo.c35[2])
        c_36 = gmsh.model.geo.add_point(self.__geo.c36[0], self.__geo.c36[1], self.__geo.c36[2])
        c_37 = gmsh.model.geo.add_point(self.__geo.c37[0], self.__geo.c37[1], self.__geo.c37[2])
        c_38 = gmsh.model.geo.add_point(self.__geo.c38[0], self.__geo.c38[1], self.__geo.c38[2])
        c_39 = gmsh.model.geo.add_point(self.__geo.c39[0], self.__geo.c39[1], self.__geo.c39[2])
        c_40 = gmsh.model.geo.add_point(self.__geo.c40[0], self.__geo.c40[1], self.__geo.c40[2])
        c_41 = gmsh.model.geo.add_point(self.__geo.c41[0], self.__geo.c41[1], self.__geo.c41[2])

        p_center_head = gmsh.model.geo.add_point(0.5 * (self.__geo.p26e[0] + self.__geo.p26d[0]), 0.5 * (self.__geo.p26e[1] + self.__geo.p26d[1]), 0.5 * (self.__geo.p26e[2] + self.__geo.p26d[2]))

        c_42e = gmsh.model.geo.add_point(self.__geo.c42e[0], self.__geo.c42e[1], self.__geo.c42e[2])
        c_43e = gmsh.model.geo.add_point(self.__geo.c43e[0], self.__geo.c43e[1], self.__geo.c43e[2])
        c_44e = gmsh.model.geo.add_point(self.__geo.c44e[0], self.__geo.c44e[1], self.__geo.c44e[2])
        c_45e = gmsh.model.geo.add_point(self.__geo.c45e[0], self.__geo.c45e[1], self.__geo.c45e[2])

        c_42d = gmsh.model.geo.add_point(self.__geo.c42d[0], self.__geo.c42d[1], self.__geo.c42d[2])
        c_43d = gmsh.model.geo.add_point(self.__geo.c43d[0], self.__geo.c43d[1], self.__geo.c43d[2])
        c_44d = gmsh.model.geo.add_point(self.__geo.c44d[0], self.__geo.c44d[1], self.__geo.c44d[2])
        c_45d = gmsh.model.geo.add_point(self.__geo.c45d[0], self.__geo.c45d[1], self.__geo.c45d[2])

        c_46e = gmsh.model.geo.add_point(self.__geo.c46e[0], self.__geo.c46e[1], self.__geo.c46e[2])
        c_47e = gmsh.model.geo.add_point(self.__geo.c47e[0], self.__geo.c47e[1], self.__geo.c47e[2])
        c_48e = gmsh.model.geo.add_point(self.__geo.c48e[0], self.__geo.c48e[1], self.__geo.c48e[2])
        c_49e = gmsh.model.geo.add_point(self.__geo.c49e[0], self.__geo.c49e[1], self.__geo.c49e[2])

        c_46d = gmsh.model.geo.add_point(self.__geo.c46d[0], self.__geo.c46d[1], self.__geo.c46d[2])
        c_47d = gmsh.model.geo.add_point(self.__geo.c47d[0], self.__geo.c47d[1], self.__geo.c47d[2])
        c_48d = gmsh.model.geo.add_point(self.__geo.c48d[0], self.__geo.c48d[1], self.__geo.c48d[2])
        c_49d = gmsh.model.geo.add_point(self.__geo.c49d[0], self.__geo.c49d[1], self.__geo.c49d[2])

        c_50e = gmsh.model.geo.add_point(self.__geo.c50e[0], self.__geo.c50e[1], self.__geo.c50e[2])
        c_51e = gmsh.model.geo.add_point(self.__geo.c51e[0], self.__geo.c51e[1], self.__geo.c51e[2])
        c_52e = gmsh.model.geo.add_point(self.__geo.c52e[0], self.__geo.c52e[1], self.__geo.c52e[2])
        c_53e = gmsh.model.geo.add_point(self.__geo.c53e[0], self.__geo.c53e[1], self.__geo.c53e[2])

        c_50d = gmsh.model.geo.add_point(self.__geo.c50d[0], self.__geo.c50d[1], self.__geo.c50d[2])
        c_51d = gmsh.model.geo.add_point(self.__geo.c51d[0], self.__geo.c51d[1], self.__geo.c51d[2])
        c_52d = gmsh.model.geo.add_point(self.__geo.c52d[0], self.__geo.c52d[1], self.__geo.c52d[2])
        c_53d = gmsh.model.geo.add_point(self.__geo.c53d[0], self.__geo.c53d[1], self.__geo.c53d[2])

        p_center_tail = gmsh.model.geo.add_point(0.5 * (self.__geo.p27e[0] + self.__geo.p27d[0]), 0.5 * (self.__geo.p27e[1] + self.__geo.p27d[1]), 0.5 * (self.__geo.p27e[2] + self.__geo.p27d[2]))

        p_38 = gmsh.model.geo.add_point(self.__geo.p38[0], self.__geo.p38[1], self.__geo.p38[2])
        p_41e = gmsh.model.geo.add_point(self.__geo.p41e[0], self.__geo.p41e[1], self.__geo.p41e[2])
        p_41d = gmsh.model.geo.add_point(self.__geo.p41d[0], self.__geo.p41d[1], self.__geo.p41d[2])
        p_39 = gmsh.model.geo.add_point(self.__geo.p39[0], self.__geo.p39[1], self.__geo.p39[2])
        p_42 = gmsh.model.geo.add_point(self.__geo.p42[0], self.__geo.p42[1], self.__geo.p42[2])
        
        c_54 = gmsh.model.geo.add_point(self.__geo.c54[0], self.__geo.c54[1], self.__geo.c54[2])
        c_56e = gmsh.model.geo.add_point(self.__geo.c56e[0], self.__geo.c56e[1], self.__geo.c56e[2])
        c_56d = gmsh.model.geo.add_point(self.__geo.c56d[0], self.__geo.c56d[1], self.__geo.c56d[2])
        c_55 = gmsh.model.geo.add_point(self.__geo.c55[0], self.__geo.c55[1], self.__geo.c55[2])
        c_57 = gmsh.model.geo.add_point(self.__geo.c57[0], self.__geo.c57[1], self.__geo.c57[2])
        c_59e = gmsh.model.geo.add_point(self.__geo.c59e[0], self.__geo.c59e[1], self.__geo.c59e[2])
        c_59d = gmsh.model.geo.add_point(self.__geo.c59d[0], self.__geo.c59d[1], self.__geo.c59d[2])
        c_58 = gmsh.model.geo.add_point(self.__geo.c58[0], self.__geo.c58[1], self.__geo.c58[2])

        p_head_center = gmsh.model.geo.add_point(0.5 * (self.__geo.p41e[0] + self.__geo.p41d[0]), 0.5 * (self.__geo.p41e[1] + self.__geo.p41d[1]), 0.5 * (self.__geo.p41e[2] + self.__geo.p41d[2]))

        p_45 = gmsh.model.geo.add_point(self.__geo.p45[0], self.__geo.p45[1], self.__geo.p45[2])
        p_46 = gmsh.model.geo.add_point(self.__geo.p46[0], self.__geo.p46[1], self.__geo.p46[2])
        p_51 = gmsh.model.geo.add_point(self.__geo.p51[0], self.__geo.p51[1], self.__geo.p51[2])
        p_43e = gmsh.model.geo.add_point(self.__geo.p43e[0], self.__geo.p43e[1], self.__geo.p43e[2])
        p_44e = gmsh.model.geo.add_point(self.__geo.p44e[0], self.__geo.p44e[1], self.__geo.p44e[2])
        p_49e = gmsh.model.geo.add_point(self.__geo.p49e[0], self.__geo.p49e[1], self.__geo.p49e[2])
        p_47e = gmsh.model.geo.add_point(self.__geo.p47e[0], self.__geo.p47e[1], self.__geo.p47e[2])
        p_43d = gmsh.model.geo.add_point(self.__geo.p43d[0], self.__geo.p43d[1], self.__geo.p43d[2])
        p_44d = gmsh.model.geo.add_point(self.__geo.p44d[0], self.__geo.p44d[1], self.__geo.p44d[2])
        p_49d = gmsh.model.geo.add_point(self.__geo.p49d[0], self.__geo.p49d[1], self.__geo.p49d[2])
        p_47d = gmsh.model.geo.add_point(self.__geo.p47d[0], self.__geo.p47d[1], self.__geo.p47d[2])
        
        #------------------------------------------#
        # Curves                                   #
        #------------------------------------------#
        curve_1_2_e = gmsh.model.geo.add_bezier([p_1e, c_1e, p_2e])
        curve_2_3_e = gmsh.model.geo.add_bezier([p_2e, c_2e, c_3e, p_3e])
        curve_3_4_e = gmsh.model.geo.add_bezier([p_3e, c_4e, c_5e, p_4e])
        curve_4_5_e = gmsh.model.geo.add_line(p_4e, p_5e)
        curve_5_6_e = gmsh.model.geo.add_bezier([p_5e, c_6e, c_7e, p_6e])
        curve_6_7_e = gmsh.model.geo.add_bezier([p_6e, c_8e, c_9e, p_7e])
        curve_7_8_e = gmsh.model.geo.add_bezier([p_7e, c_10e, c_11e, p_8e])
        curve_8_9_e = gmsh.model.geo.add_bezier([p_8e, c_12e, c_13e, p_9e])
        curve_9_10_e = gmsh.model.geo.add_bezier([p_9e, c_14e, c_15e, p_10e])
        curve_10_11_e = gmsh.model.geo.add_bezier([p_10e, c_16e, c_17e, p_11e])
        curve_11_12_e = gmsh.model.geo.add_bezier([p_11e, c_18e, c_19e, p_12e])
        curve_12_13_e = gmsh.model.geo.add_bezier([p_12e, c_20e, c_21e, p_13e])
        
        curve_14_16_e = gmsh.model.geo.add_polyline([p_14e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve17e] + [p_16e])
        curve_16_18_e = gmsh.model.geo.add_polyline([p_16e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve23e] + [p_18e])
        curve_18_20_e = gmsh.model.geo.add_polyline([p_18e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve29e] + [p_20e])
        curve_20_22_e = gmsh.model.geo.add_polyline([p_20e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve35e] + [p_22e])
        curve_22_24_e = gmsh.model.geo.add_polyline([p_22e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve41e] + [p_24e])
        curve_24_7_e = gmsh.model.geo.add_line(p_24e, p_7e)

        curve_15_17_e = gmsh.model.geo.add_polyline([p_15e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve18e] + [p_17e])
        curve_17_19_e = gmsh.model.geo.add_polyline([p_17e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve24e] + [p_19e])
        curve_19_21_e = gmsh.model.geo.add_polyline([p_19e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve30e] + [p_21e])
        curve_21_23_e = gmsh.model.geo.add_polyline([p_21e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve36e] + [p_23e])
        curve_23_25_e = gmsh.model.geo.add_polyline([p_23e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve42e] + [p_25e])
        curve_25_7_e = gmsh.model.geo.add_line(p_25e, p_7e)

        curve_13_14_e = gmsh.model.geo.add_polyline([p_13e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve15e] + [p_14e])
        curve_14_1_e = gmsh.model.geo.add_polyline([p_14e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve13e] + [p_1e])
        curve_13_15_e = gmsh.model.geo.add_polyline([p_13e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve16e] + [p_15e])
        curve_15_1_e = gmsh.model.geo.add_polyline([p_15e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve14e] + [p_1e])

        curve_12_16_e = gmsh.model.geo.add_polyline([p_12e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve21e] + [p_16e])
        curve_16_2_e = gmsh.model.geo.add_polyline([p_16e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve19e] + [p_2e])
        curve_12_17_e = gmsh.model.geo.add_polyline([p_12e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve22e] + [p_17e])
        curve_17_2_e = gmsh.model.geo.add_polyline([p_17e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve20e] + [p_2e])

        curve_11_18_e = gmsh.model.geo.add_polyline([p_11e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve27e] + [p_18e])
        curve_18_3_e = gmsh.model.geo.add_polyline([p_18e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve25e] + [p_3e])
        curve_11_19_e = gmsh.model.geo.add_polyline([p_11e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve28e] + [p_19e])
        curve_19_3_e = gmsh.model.geo.add_polyline([p_19e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve26e] + [p_3e])

        curve_10_20_e = gmsh.model.geo.add_polyline([p_10e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve33e] + [p_20e])
        curve_20_4_e = gmsh.model.geo.add_polyline([p_20e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve31e] + [p_4e])
        curve_10_21_e = gmsh.model.geo.add_polyline([p_10e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve34e] + [p_21e])
        curve_21_4_e = gmsh.model.geo.add_polyline([p_21e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve32e] + [p_4e])

        curve_9_22_e = gmsh.model.geo.add_polyline([p_9e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve39e] + [p_22e])
        curve_22_5_e = gmsh.model.geo.add_polyline([p_22e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve37e] + [p_5e])
        curve_9_23_e = gmsh.model.geo.add_polyline([p_9e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve40e] + [p_23e])
        curve_23_5_e = gmsh.model.geo.add_polyline([p_23e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve38e] + [p_5e])

        curve_8_24_e = gmsh.model.geo.add_polyline([p_8e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve45e] + [p_24e])
        curve_24_6_e = gmsh.model.geo.add_polyline([p_24e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve43e] + [p_6e])
        curve_8_25_e = gmsh.model.geo.add_polyline([p_8e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve46e] + [p_25e])
        curve_25_6_e = gmsh.model.geo.add_polyline([p_25e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve44e] + [p_6e])

        curve_1_2_d = gmsh.model.geo.add_bezier([p_1d, c_1d, p_2d])
        curve_2_3_d = gmsh.model.geo.add_bezier([p_2d, c_2d, c_3d, p_3d])
        curve_3_4_d = gmsh.model.geo.add_bezier([p_3d, c_4d, c_5d, p_4d])
        curve_4_5_d = gmsh.model.geo.add_line(p_4d, p_5d)
        curve_5_6_d = gmsh.model.geo.add_bezier([p_5d, c_6d, c_7d, p_6d])
        curve_6_7_d = gmsh.model.geo.add_bezier([p_6d, c_8d, c_9d, p_7d])
        curve_7_8_d = gmsh.model.geo.add_bezier([p_7d, c_10d, c_11d, p_8d])
        curve_8_9_d = gmsh.model.geo.add_bezier([p_8d, c_12d, c_13d, p_9d])
        curve_9_10_d = gmsh.model.geo.add_bezier([p_9d, c_14d, c_15d, p_10d])
        curve_10_11_d = gmsh.model.geo.add_bezier([p_10d, c_16d, c_17d, p_11d])
        curve_11_12_d = gmsh.model.geo.add_bezier([p_11d, c_18d, c_19d, p_12d])
        curve_12_13_d = gmsh.model.geo.add_bezier([p_12d, c_20d, c_21d, p_13d])

        curve_14_16_d = gmsh.model.geo.add_polyline([p_14d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve17d] + [p_16d])
        curve_16_18_d = gmsh.model.geo.add_polyline([p_16d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve23d] + [p_18d])
        curve_18_20_d = gmsh.model.geo.add_polyline([p_18d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve29d] + [p_20d])
        curve_20_22_d = gmsh.model.geo.add_polyline([p_20d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve35d] + [p_22d])
        curve_22_24_d = gmsh.model.geo.add_polyline([p_22d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve41d] + [p_24d])
        curve_24_7_d = gmsh.model.geo.add_line(p_24d, p_7d)

        curve_15_17_d = gmsh.model.geo.add_polyline([p_15d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve18d] + [p_17d])
        curve_17_19_d = gmsh.model.geo.add_polyline([p_17d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve24d] + [p_19d])
        curve_19_21_d = gmsh.model.geo.add_polyline([p_19d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve30d] + [p_21d])
        curve_21_23_d = gmsh.model.geo.add_polyline([p_21d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve36d] + [p_23d])
        curve_23_25_d = gmsh.model.geo.add_polyline([p_23d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve42d] + [p_25d])
        curve_25_7_d = gmsh.model.geo.add_line(p_25d, p_7d)

        curve_13_14_d = gmsh.model.geo.add_polyline([p_13d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve15d] + [p_14d])
        curve_14_1_d = gmsh.model.geo.add_polyline([p_14d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve13d] + [p_1d])
        curve_13_15_d = gmsh.model.geo.add_polyline([p_13d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve16d] + [p_15d])
        curve_15_1_d = gmsh.model.geo.add_polyline([p_15d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve14d] + [p_1d])

        curve_12_16_d = gmsh.model.geo.add_polyline([p_12d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve21d] + [p_16d])
        curve_16_2_d = gmsh.model.geo.add_polyline([p_16d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve19d] + [p_2d])
        curve_12_17_d = gmsh.model.geo.add_polyline([p_12d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve22d] + [p_17d])
        curve_17_2_d = gmsh.model.geo.add_polyline([p_17d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve20d] + [p_2d])

        curve_11_18_d = gmsh.model.geo.add_polyline([p_11d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve27d] + [p_18d])
        curve_18_3_d = gmsh.model.geo.add_polyline([p_18d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve25d] + [p_3d])
        curve_11_19_d = gmsh.model.geo.add_polyline([p_11d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve28d] + [p_19d])
        curve_19_3_d = gmsh.model.geo.add_polyline([p_19d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve26d] + [p_3d])

        curve_10_20_d = gmsh.model.geo.add_polyline([p_10d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve33d] + [p_20d])
        curve_20_4_d = gmsh.model.geo.add_polyline([p_20d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve31d] + [p_4d])
        curve_10_21_d = gmsh.model.geo.add_polyline([p_10d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve34d] + [p_21d])
        curve_21_4_d = gmsh.model.geo.add_polyline([p_21d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve32d] + [p_4d])

        curve_9_22_d = gmsh.model.geo.add_polyline([p_9d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve39d] + [p_22d])
        curve_22_5_d = gmsh.model.geo.add_polyline([p_22d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve37d] + [p_5d])
        curve_9_23_d = gmsh.model.geo.add_polyline([p_9d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve40d] + [p_23d])
        curve_23_5_d = gmsh.model.geo.add_polyline([p_23d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve38d] + [p_5d])

        curve_8_24_d = gmsh.model.geo.add_polyline([p_8d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve45d] + [p_24d])
        curve_24_6_d = gmsh.model.geo.add_polyline([p_24d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve43d] + [p_6d])
        curve_8_25_d = gmsh.model.geo.add_polyline([p_8d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve46d] + [p_25d])
        curve_25_6_d = gmsh.model.geo.add_polyline([p_25d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve44d] + [p_6d])

        curve_26_1_e = gmsh.model.geo.add_bezier([p_26e, c_22e, c_23e, p_1e])
        curve_13_27_e = gmsh.model.geo.add_bezier([p_13e, c_24e, c_25e, p_27e])
        curve_26_1_d = gmsh.model.geo.add_bezier([p_26d, c_22d, c_23d, p_1d])
        curve_13_27_d = gmsh.model.geo.add_bezier([p_13d, c_24d, c_25d, p_27d])

        curve_28_29 = gmsh.model.geo.add_bezier([p_28, c_26, c_27, p_29])
        curve_29_30 = gmsh.model.geo.add_bezier([p_29, c_28, c_29, p_30])
        curve_30_31 = gmsh.model.geo.add_bezier([p_30, c_30, c_31, p_31])
        curve_31_32 = gmsh.model.geo.add_bezier([p_31, c_32, c_33, p_32])

        curve_33_34 = gmsh.model.geo.add_bezier([p_33, c_34, c_35, p_34])
        curve_34_35 = gmsh.model.geo.add_bezier([p_34, c_36, c_37, p_35])
        curve_35_36 = gmsh.model.geo.add_bezier([p_35, c_38, c_39, p_36])
        curve_36_37 = gmsh.model.geo.add_bezier([p_36, c_40, c_41, p_37])

        curve_28_26_e = gmsh.model.geo.add_circle_arc(p_28, p_center_head, p_26e)
        curve_26e_33 = gmsh.model.geo.add_circle_arc(p_26e, p_center_head, p_33)
        curve_33_26_d = gmsh.model.geo.add_circle_arc(p_33, p_center_head, p_26d)
        curve_26d_28 = gmsh.model.geo.add_circle_arc(p_26d, p_center_head, p_28)

        curve_29_1_e = gmsh.model.geo.add_bezier([p_29, c_42e, c_43e, p_1e])
        curve_1e_34 = gmsh.model.geo.add_bezier([p_1e, c_44e, c_45e, p_34])
        curve_29_1_d = gmsh.model.geo.add_bezier([p_29, c_42d, c_43d, p_1d])
        curve_1d_34 = gmsh.model.geo.add_bezier([p_1d, c_44d, c_45d, p_34])

        curve_30_14_e = gmsh.model.geo.add_bezier([p_30, c_46e, c_47e, p_14e])
        curve_15e_35 = gmsh.model.geo.add_bezier([p_15e, c_48e, c_49e, p_35])
        curve_30_14_d = gmsh.model.geo.add_bezier([p_30, c_46d, c_47d, p_14d])
        curve_15d_35 = gmsh.model.geo.add_bezier([p_15d, c_48d, c_49d, p_35])

        curve_31_13_e = gmsh.model.geo.add_bezier([p_31, c_50e, c_51e, p_13e])
        curve_13e_36 = gmsh.model.geo.add_bezier([p_13e, c_52e, c_53e, p_36])
        curve_31_13_d = gmsh.model.geo.add_bezier([p_31, c_50d, c_51d, p_13d])
        curve_13d_36 = gmsh.model.geo.add_bezier([p_13d, c_52d, c_53d, p_36])

        curve_32_27_e = gmsh.model.geo.add_ellipse_arc(p_32, p_center_tail, p_27e, p_27e)
        curve_27e_37 = gmsh.model.geo.add_ellipse_arc(p_27e, p_center_tail, p_27e, p_37)
        curve_32_27_d = gmsh.model.geo.add_ellipse_arc(p_32, p_center_tail, p_27d, p_27d)
        curve_27d_37 = gmsh.model.geo.add_ellipse_arc(p_27d, p_center_tail, p_27d, p_37)

        curve_28_38 = gmsh.model.geo.add_bezier([p_28, c_54, p_38])
        curve_38_42 = gmsh.model.geo.add_bezier([p_38, c_57, p_42])
        curve_26_41_e = gmsh.model.geo.add_bezier([p_26e, c_56e, p_41e])
        curve_41e_42 = gmsh.model.geo.add_bezier([p_41e, c_59e, p_42])
        curve_33_39 = gmsh.model.geo.add_bezier([p_33, c_55, p_39])
        curve_39_42 = gmsh.model.geo.add_bezier([p_39, c_58, p_42])
        curve_26_41_d = gmsh.model.geo.add_bezier([p_26d, c_56d, p_41d])
        curve_41d_42 = gmsh.model.geo.add_bezier([p_41d, c_59d, p_42])

        curve_38_41e = gmsh.model.geo.add_circle_arc(p_38, p_head_center, p_41e)
        curve_41e_39 = gmsh.model.geo.add_circle_arc(p_41e, p_head_center, p_39)
        curve_38_41d = gmsh.model.geo.add_circle_arc(p_38, p_head_center, p_41d)
        curve_41d_39 = gmsh.model.geo.add_circle_arc(p_41d, p_head_center, p_39)

        curve_43_27_e = gmsh.model.geo.add_polyline([p_43e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve84e] + [p_27e])
        curve_44_27_e = gmsh.model.geo.add_polyline([p_44e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve85e] + [p_27e])
        curve_49_43_e = gmsh.model.geo.add_polyline([p_49e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve86e] + [p_43e])
        curve_49_44_e = gmsh.model.geo.add_polyline([p_49e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve87e] + [p_44e])

        curve_43_27_d = gmsh.model.geo.add_polyline([p_43d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve84d] + [p_27d])
        curve_44_27_d = gmsh.model.geo.add_polyline([p_44d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve85d] + [p_27d])
        curve_49_43_d = gmsh.model.geo.add_polyline([p_49d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve86d] + [p_43d])
        curve_49_44_d = gmsh.model.geo.add_polyline([p_49d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve87d] + [p_44d])

        curve_47_49_e = gmsh.model.geo.add_polyline([p_47e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve82e] + [p_49e])
        curve_47_49_d = gmsh.model.geo.add_polyline([p_47d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve82d] + [p_49d])
        curve_49e_51 = gmsh.model.geo.add_polyline([p_49e] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve83e] + [p_51])
        curve_49d_51 = gmsh.model.geo.add_polyline([p_49d] + [gmsh.model.geo.add_point(point[0], point[1], point[2]) for point in self.__geo.curve83d] + [p_51])

        curve_27_47_e = gmsh.model.geo.add_line(p_27e, p_47e)
        curve_27_47_d = gmsh.model.geo.add_line(p_27d, p_47d)
        curve_32_45 = gmsh.model.geo.add_line(p_32, p_45)
        curve_37_46 = gmsh.model.geo.add_line(p_37, p_46)
        curve_45_51 = gmsh.model.geo.add_line(p_45, p_51)
        curve_46_51 = gmsh.model.geo.add_line(p_46, p_51)
        curve_43_47_e = gmsh.model.geo.add_line(p_43e, p_47e)
        curve_43_47_d = gmsh.model.geo.add_line(p_43d, p_47d)
        curve_45_43e = gmsh.model.geo.add_line(p_45, p_43e)
        curve_45_43d = gmsh.model.geo.add_line(p_45, p_43d)
        curve_44_47_e = gmsh.model.geo.add_line(p_44e, p_47e)
        curve_44_47_d = gmsh.model.geo.add_line(p_44d, p_47d)
        curve_46_44e = gmsh.model.geo.add_line(p_46, p_44e)
        curve_46_44d = gmsh.model.geo.add_line(p_46, p_44d)

        #------------------------------------------#
        # Curve loops                              #
        #------------------------------------------#
        cl_1_2_16_14_e = gmsh.model.geo.add_curve_loop([curve_1_2_e, -curve_16_2_e, -curve_14_16_e, curve_14_1_e])
        cl_2_3_18_16_e = gmsh.model.geo.add_curve_loop([curve_2_3_e, -curve_18_3_e, -curve_16_18_e, curve_16_2_e])
        cl_3_4_20_18_e = gmsh.model.geo.add_curve_loop([curve_3_4_e, -curve_20_4_e, -curve_18_20_e, curve_18_3_e])
        cl_4_5_22_20_e = gmsh.model.geo.add_curve_loop([curve_4_5_e, -curve_22_5_e, -curve_20_22_e, curve_20_4_e])
        cl_5_6_24_22_e = gmsh.model.geo.add_curve_loop([curve_5_6_e, -curve_24_6_e, -curve_22_24_e, curve_22_5_e])
        cl_6_7_24_e = gmsh.model.geo.add_curve_loop([curve_6_7_e, -curve_24_7_e, curve_24_6_e])

        cl_14_16_12_13_e = gmsh.model.geo.add_curve_loop([curve_14_16_e, -curve_12_16_e, curve_12_13_e, curve_13_14_e])
        cl_16_18_11_12_e = gmsh.model.geo.add_curve_loop([curve_16_18_e, -curve_11_18_e, curve_11_12_e, curve_12_16_e])
        cl_18_20_10_11_e = gmsh.model.geo.add_curve_loop([curve_18_20_e, -curve_10_20_e, curve_10_11_e, curve_11_18_e])
        cl_20_22_9_10_e = gmsh.model.geo.add_curve_loop([curve_20_22_e, -curve_9_22_e, curve_9_10_e, curve_10_20_e])
        cl_22_24_8_9_e = gmsh.model.geo.add_curve_loop([curve_22_24_e, -curve_8_24_e, curve_8_9_e, curve_9_22_e])
        cl_24_7_8_e = gmsh.model.geo.add_curve_loop([curve_24_7_e, curve_7_8_e, curve_8_24_e])

        cl_1_15_17_2_e = gmsh.model.geo.add_curve_loop([-curve_15_1_e, curve_15_17_e, curve_17_2_e, -curve_1_2_e])
        cl_2_17_19_3_e = gmsh.model.geo.add_curve_loop([-curve_17_2_e, curve_17_19_e, curve_19_3_e, -curve_2_3_e])
        cl_3_19_21_4_e = gmsh.model.geo.add_curve_loop([-curve_19_3_e, curve_19_21_e, curve_21_4_e, -curve_3_4_e])
        cl_4_21_23_5_e = gmsh.model.geo.add_curve_loop([-curve_21_4_e, curve_21_23_e, curve_23_5_e, -curve_4_5_e])
        cl_5_23_25_6_e = gmsh.model.geo.add_curve_loop([-curve_23_5_e, curve_23_25_e, curve_25_6_e, -curve_5_6_e])
        cl_6_25_7_e = gmsh.model.geo.add_curve_loop([curve_25_7_e, -curve_6_7_e, -curve_25_6_e])

        cl_15_13_12_17_e = gmsh.model.geo.add_curve_loop([-curve_13_15_e, -curve_12_13_e, curve_12_17_e, -curve_15_17_e])
        cl_17_12_11_19_e = gmsh.model.geo.add_curve_loop([-curve_12_17_e, -curve_11_12_e, curve_11_19_e, -curve_17_19_e])
        cl_19_11_10_21_e = gmsh.model.geo.add_curve_loop([-curve_11_19_e, -curve_10_11_e, curve_10_21_e, -curve_19_21_e])
        cl_21_10_9_23_e = gmsh.model.geo.add_curve_loop([-curve_10_21_e, -curve_9_10_e, curve_9_23_e, -curve_21_23_e])
        cl_23_9_8_25_e = gmsh.model.geo.add_curve_loop([-curve_9_23_e, -curve_8_9_e, curve_8_25_e, -curve_23_25_e])
        cl_25_12_7_e = gmsh.model.geo.add_curve_loop([-curve_7_8_e, -curve_25_7_e, -curve_8_25_e])

        cl_1_2_16_14_d = gmsh.model.geo.add_curve_loop(self.__flip([curve_1_2_d, -curve_16_2_d, -curve_14_16_d, curve_14_1_d]))
        cl_2_3_18_16_d = gmsh.model.geo.add_curve_loop(self.__flip([curve_2_3_d, -curve_18_3_d, -curve_16_18_d, curve_16_2_d]))
        cl_3_4_20_18_d = gmsh.model.geo.add_curve_loop(self.__flip([curve_3_4_d, -curve_20_4_d, -curve_18_20_d, curve_18_3_d]))
        cl_4_5_22_20_d = gmsh.model.geo.add_curve_loop(self.__flip([curve_4_5_d, -curve_22_5_d, -curve_20_22_d, curve_20_4_d]))
        cl_5_6_24_22_d = gmsh.model.geo.add_curve_loop(self.__flip([curve_5_6_d, -curve_24_6_d, -curve_22_24_d, curve_22_5_d]))
        cl_6_7_24_d = gmsh.model.geo.add_curve_loop(self.__flip([curve_24_6_d, curve_6_7_d, -curve_24_7_d]))

        cl_14_16_12_13_d = gmsh.model.geo.add_curve_loop(self.__flip([curve_14_16_d, -curve_12_16_d, curve_12_13_d, curve_13_14_d]))
        cl_16_18_11_12_d = gmsh.model.geo.add_curve_loop(self.__flip([curve_16_18_d, -curve_11_18_d, curve_11_12_d, curve_12_16_d]))
        cl_18_20_10_11_d = gmsh.model.geo.add_curve_loop(self.__flip([curve_18_20_d, -curve_10_20_d, curve_10_11_d, curve_11_18_d]))
        cl_20_22_9_10_d = gmsh.model.geo.add_curve_loop(self.__flip([curve_20_22_d, -curve_9_22_d, curve_9_10_d, curve_10_20_d]))
        cl_22_24_8_9_d = gmsh.model.geo.add_curve_loop(self.__flip([curve_22_24_d, -curve_8_24_d, curve_8_9_d, curve_9_22_d]))
        cl_24_7_8_d = gmsh.model.geo.add_curve_loop(self.__flip([curve_8_24_d, curve_24_7_d, curve_7_8_d]))

        cl_1_15_17_2_d = gmsh.model.geo.add_curve_loop(self.__flip([-curve_15_1_d, curve_15_17_d, curve_17_2_d, -curve_1_2_d]))
        cl_2_17_19_3_d = gmsh.model.geo.add_curve_loop(self.__flip([-curve_17_2_d, curve_17_19_d, curve_19_3_d, -curve_2_3_d]))
        cl_3_19_21_4_d = gmsh.model.geo.add_curve_loop(self.__flip([-curve_19_3_d, curve_19_21_d, curve_21_4_d, -curve_3_4_d]))
        cl_4_21_23_5_d = gmsh.model.geo.add_curve_loop(self.__flip([-curve_21_4_d, curve_21_23_d, curve_23_5_d, -curve_4_5_d]))
        cl_5_23_25_6_d = gmsh.model.geo.add_curve_loop(self.__flip([-curve_23_5_d, curve_23_25_d, curve_25_6_d, -curve_5_6_d]))
        cl_6_25_7_d = gmsh.model.geo.add_curve_loop(self.__flip([-curve_25_6_d, curve_25_7_d, -curve_6_7_d]))

        cl_15_13_12_17_d = gmsh.model.geo.add_curve_loop(self.__flip([-curve_13_15_d, -curve_12_13_d, curve_12_17_d, -curve_15_17_d]))
        cl_17_12_11_19_d = gmsh.model.geo.add_curve_loop(self.__flip([-curve_12_17_d, -curve_11_12_d, curve_11_19_d, -curve_17_19_d]))
        cl_19_11_10_21_d = gmsh.model.geo.add_curve_loop(self.__flip([-curve_11_19_d, -curve_10_11_d, curve_10_21_d, -curve_19_21_d]))
        cl_21_10_9_23_d = gmsh.model.geo.add_curve_loop(self.__flip([-curve_10_21_d, -curve_9_10_d, curve_9_23_d, -curve_21_23_d]))
        cl_23_9_8_25_d = gmsh.model.geo.add_curve_loop(self.__flip([-curve_9_23_d, -curve_8_9_d, curve_8_25_d, -curve_23_25_d]))
        cl_25_12_7_d = gmsh.model.geo.add_curve_loop(self.__flip([-curve_8_25_d, -curve_7_8_d, -curve_25_7_d]))

        cl_26e_1e_29_28 = gmsh.model.geo.add_curve_loop([curve_26_1_e, -curve_29_1_e, -curve_28_29, curve_28_26_e])
        cl_1e_14e_30_29 = gmsh.model.geo.add_curve_loop([-curve_14_1_e, -curve_30_14_e, -curve_29_30, curve_29_1_e])
        cl_14e_13e_31_30 = gmsh.model.geo.add_curve_loop([-curve_13_14_e, -curve_31_13_e, -curve_30_31, curve_30_14_e])
        cl_31_13e_27e_32 = gmsh.model.geo.add_curve_loop([curve_13_27_e, -curve_32_27_e, -curve_31_32, curve_31_13_e])

        cl_26d_1d_29_28 = gmsh.model.geo.add_curve_loop([curve_26d_28, curve_28_29, curve_29_1_d, -curve_26_1_d])
        cl_1d_14d_30_29 = gmsh.model.geo.add_curve_loop([curve_29_30, curve_30_14_d, curve_14_1_d, -curve_29_1_d])
        cl_14d_13d_31_30 = gmsh.model.geo.add_curve_loop([curve_30_31, curve_31_13_d, curve_13_14_d, -curve_30_14_d])
        cl_31_13d_27d_32 = gmsh.model.geo.add_curve_loop([curve_31_32, curve_32_27_d, -curve_13_27_d, -curve_31_13_d])

        cl_26e_33_34_1e = gmsh.model.geo.add_curve_loop([curve_26e_33, curve_33_34, -curve_1e_34, -curve_26_1_e])
        cl_1e_34_35_15e = gmsh.model.geo.add_curve_loop([curve_1e_34, curve_34_35, -curve_15e_35, curve_15_1_e])
        cl_15e_35_36_13e = gmsh.model.geo.add_curve_loop([curve_15e_35, curve_35_36, -curve_13e_36, curve_13_15_e])
        cl_13e_36_37_27e = gmsh.model.geo.add_curve_loop([curve_13e_36, curve_36_37, -curve_27e_37, -curve_13_27_e])

        cl_26d_33_34_1d = gmsh.model.geo.add_curve_loop(self.__flip([-curve_33_26_d, curve_33_34, -curve_1d_34, -curve_26_1_d]))
        cl_1d_34_35_15d = gmsh.model.geo.add_curve_loop(self.__flip([curve_1d_34, curve_34_35, -curve_15d_35, curve_15_1_d]))
        cl_15d_35_36_13d = gmsh.model.geo.add_curve_loop(self.__flip([curve_15d_35, curve_35_36, -curve_13d_36, curve_13_15_d]))
        cl_13d_36_37_27d = gmsh.model.geo.add_curve_loop(self.__flip([curve_13d_36, curve_36_37, -curve_27d_37, -curve_13_27_d]))

        cl_28_26e_41e_38 = gmsh.model.geo.add_curve_loop(self.__flip([curve_28_26_e, curve_26_41_e, -curve_38_41e, -curve_28_38]))
        cl_26e_33_39_41e = gmsh.model.geo.add_curve_loop(self.__flip([curve_26e_33, curve_33_39, -curve_41e_39, -curve_26_41_e]))
        cl_26d_33_39_41d = gmsh.model.geo.add_curve_loop(self.__flip([curve_26d_28, curve_28_38, curve_38_41d, -curve_26_41_d]))
        cl_28_26d_41d_38 = gmsh.model.geo.add_curve_loop(self.__flip([curve_33_26_d, curve_26_41_d, curve_41d_39, -curve_33_39]))

        cl_38_41e_42 = gmsh.model.geo.add_curve_loop(self.__flip([curve_38_41e, curve_41e_42, -curve_38_42]))
        cl_41e_39_42 = gmsh.model.geo.add_curve_loop(self.__flip([curve_41e_39, curve_39_42, -curve_41e_42]))
        cl_41d_38_42 = gmsh.model.geo.add_curve_loop(self.__flip([-curve_38_41d, curve_38_42, -curve_41d_42]))
        cl_39_41d_42 = gmsh.model.geo.add_curve_loop([curve_39_42, -curve_41d_42, curve_41d_39])

        cl_27_47_43_e = gmsh.model.geo.add_curve_loop([curve_27_47_e, -curve_43_47_e, curve_43_27_e])
        cl_27e_43e_45_32 = gmsh.model.geo.add_curve_loop([-curve_43_27_e, -curve_45_43e, -curve_32_45, curve_32_27_e])
        cl_32_45_43d_27d = gmsh.model.geo.add_curve_loop([curve_32_45, curve_45_43d, curve_43_27_d, -curve_32_27_d])
        cl_43_47_27_d = gmsh.model.geo.add_curve_loop([curve_43_47_d, -curve_27_47_d, -curve_43_27_d])
        cl_43_47_49_e = gmsh.model.geo.add_curve_loop([curve_43_47_e, curve_47_49_e, curve_49_43_e])
        cl_43e_49e_51_45 = gmsh.model.geo.add_curve_loop([-curve_49_43_e, curve_49e_51, -curve_45_51, curve_45_43e])
        cl_45_51_49d_43d = gmsh.model.geo.add_curve_loop([curve_45_51, -curve_49d_51, curve_49_43_d, -curve_45_43d])
        cl_49_47_43_d = gmsh.model.geo.add_curve_loop([-curve_47_49_d, -curve_43_47_d, -curve_49_43_d])

        cl_27_47_44_e = gmsh.model.geo.add_curve_loop(self.__flip([curve_44_27_e, curve_27_47_e, -curve_44_47_e]))
        cl_27e_44e_46_37 = gmsh.model.geo.add_curve_loop(self.__flip([-curve_44_27_e, -curve_46_44e, -curve_37_46, -curve_27e_37]))
        cl_37_46_44d_27d = gmsh.model.geo.add_curve_loop(self.__flip([curve_37_46, curve_46_44d, curve_44_27_d, curve_27d_37]))
        cl_44_47_27_d = gmsh.model.geo.add_curve_loop(self.__flip([-curve_44_27_d, curve_44_47_d, -curve_27_47_d]))
        cl_44_47_49_e = gmsh.model.geo.add_curve_loop(self.__flip([curve_49_44_e, curve_44_47_e, curve_47_49_e]))
        cl_44e_49e_51_46 = gmsh.model.geo.add_curve_loop(self.__flip([-curve_49_44_e, curve_49e_51, -curve_46_51, curve_46_44e]))
        cl_46_51_49d_44d = gmsh.model.geo.add_curve_loop(self.__flip([curve_46_51, -curve_49d_51, curve_49_44_d, -curve_46_44d]))
        cl_49_47_44_d = gmsh.model.geo.add_curve_loop(self.__flip([-curve_49_44_d, -curve_47_49_d, -curve_44_47_d]))

        #------------------------------------------#
        # Surfaces                                 #
        #------------------------------------------#
        s_1_2_16_14_e = gmsh.model.geo.add_surface_filling([cl_1_2_16_14_e])
        s_2_3_18_16_e = gmsh.model.geo.add_surface_filling([cl_2_3_18_16_e])
        s_3_4_20_18_e = gmsh.model.geo.add_surface_filling([cl_3_4_20_18_e])
        s_4_5_22_20_e = gmsh.model.geo.add_surface_filling([cl_4_5_22_20_e])
        s_5_6_24_22_e = gmsh.model.geo.add_surface_filling([cl_5_6_24_22_e])
        s_6_7_24_e = gmsh.model.geo.add_surface_filling([cl_6_7_24_e])

        s_14_16_12_13_e = gmsh.model.geo.add_surface_filling([cl_14_16_12_13_e])
        s_16_18_11_12_e = gmsh.model.geo.add_surface_filling([cl_16_18_11_12_e])
        s_18_20_10_11_e = gmsh.model.geo.add_surface_filling([cl_18_20_10_11_e])
        s_20_22_9_10_e = gmsh.model.geo.add_surface_filling([cl_20_22_9_10_e])
        s_22_24_8_9_e = gmsh.model.geo.add_surface_filling([cl_22_24_8_9_e])
        s_24_7_8_e = gmsh.model.geo.add_surface_filling([cl_24_7_8_e])

        s_1_15_17_2_e = gmsh.model.geo.add_surface_filling([cl_1_15_17_2_e])
        s_2_17_19_3_e = gmsh.model.geo.add_surface_filling([cl_2_17_19_3_e])
        s_3_19_21_4_e = gmsh.model.geo.add_surface_filling([cl_3_19_21_4_e])
        s_4_21_23_5_e = gmsh.model.geo.add_surface_filling([cl_4_21_23_5_e])
        s_5_23_25_6_e = gmsh.model.geo.add_surface_filling([cl_5_23_25_6_e])
        s_6_25_7_e = gmsh.model.geo.add_surface_filling([cl_6_25_7_e])

        s_15_13_12_17_e = gmsh.model.geo.add_surface_filling([cl_15_13_12_17_e])
        s_17_12_11_19_e = gmsh.model.geo.add_surface_filling([cl_17_12_11_19_e])
        s_19_11_10_21_e = gmsh.model.geo.add_surface_filling([cl_19_11_10_21_e])
        s_21_10_9_23_e = gmsh.model.geo.add_surface_filling([cl_21_10_9_23_e])
        s_23_9_8_25_e = gmsh.model.geo.add_surface_filling([cl_23_9_8_25_e])
        s_25_12_7_e = gmsh.model.geo.add_surface_filling([cl_25_12_7_e])

        s_1_2_16_14_d = gmsh.model.geo.add_surface_filling([cl_1_2_16_14_d])
        s_2_3_18_16_d = gmsh.model.geo.add_surface_filling([cl_2_3_18_16_d])
        s_3_4_20_18_d = gmsh.model.geo.add_surface_filling([cl_3_4_20_18_d])
        s_4_5_22_20_d = gmsh.model.geo.add_surface_filling([cl_4_5_22_20_d])
        s_5_6_24_22_d = gmsh.model.geo.add_surface_filling([cl_5_6_24_22_d])
        s_6_7_24_d = gmsh.model.geo.add_surface_filling([cl_6_7_24_d])

        s_14_16_12_13_d = gmsh.model.geo.add_surface_filling([cl_14_16_12_13_d])
        s_16_18_11_12_d = gmsh.model.geo.add_surface_filling([cl_16_18_11_12_d])
        s_18_20_10_11_d = gmsh.model.geo.add_surface_filling([cl_18_20_10_11_d])
        s_20_22_9_10_d = gmsh.model.geo.add_surface_filling([cl_20_22_9_10_d])
        s_22_24_8_9_d = gmsh.model.geo.add_surface_filling([cl_22_24_8_9_d])
        s_24_7_8_d = gmsh.model.geo.add_surface_filling([cl_24_7_8_d])

        s_1_15_17_2_d = gmsh.model.geo.add_surface_filling([cl_1_15_17_2_d])
        s_2_17_19_3_d = gmsh.model.geo.add_surface_filling([cl_2_17_19_3_d])
        s_3_19_21_4_d = gmsh.model.geo.add_surface_filling([cl_3_19_21_4_d])
        s_4_21_23_5_d = gmsh.model.geo.add_surface_filling([cl_4_21_23_5_d])
        s_5_23_25_6_d = gmsh.model.geo.add_surface_filling([cl_5_23_25_6_d])
        s_6_25_7_d = gmsh.model.geo.add_surface_filling([cl_6_25_7_d])

        s_15_13_12_17_d = gmsh.model.geo.add_surface_filling([cl_15_13_12_17_d])
        s_17_12_11_19_d = gmsh.model.geo.add_surface_filling([cl_17_12_11_19_d])
        s_19_11_10_21_d = gmsh.model.geo.add_surface_filling([cl_19_11_10_21_d])
        s_21_10_9_23_d = gmsh.model.geo.add_surface_filling([cl_21_10_9_23_d])
        s_23_9_8_25_d = gmsh.model.geo.add_surface_filling([cl_23_9_8_25_d])
        s_25_12_7_d = gmsh.model.geo.add_surface_filling([cl_25_12_7_d])

        s_26e_1e_29_28 = gmsh.model.geo.add_surface_filling([cl_26e_1e_29_28])
        s_1e_14e_30_29 = gmsh.model.geo.add_surface_filling([cl_1e_14e_30_29])
        s_14e_13e_31_30 = gmsh.model.geo.add_surface_filling([cl_14e_13e_31_30])
        s_31_13e_27e_32 = gmsh.model.geo.add_surface_filling([cl_31_13e_27e_32])

        s_26d_1d_29_28 = gmsh.model.geo.add_surface_filling([cl_26d_1d_29_28])
        s_1d_14d_30_29 = gmsh.model.geo.add_surface_filling([cl_1d_14d_30_29])
        s_14d_13d_31_30 = gmsh.model.geo.add_surface_filling([cl_14d_13d_31_30])
        s_31_13d_27d_32 = gmsh.model.geo.add_surface_filling([cl_31_13d_27d_32])

        s_26e_33_34_1e = gmsh.model.geo.add_surface_filling([cl_26e_33_34_1e])
        s_1e_34_35_15e = gmsh.model.geo.add_surface_filling([cl_1e_34_35_15e])
        s_15e_35_36_13e = gmsh.model.geo.add_surface_filling([cl_15e_35_36_13e])
        s_13e_36_37_27e = gmsh.model.geo.add_surface_filling([cl_13e_36_37_27e])

        s_26d_33_34_1d = gmsh.model.geo.add_surface_filling([cl_26d_33_34_1d])
        s_1d_34_35_15d = gmsh.model.geo.add_surface_filling([cl_1d_34_35_15d])
        s_15d_35_36_13d = gmsh.model.geo.add_surface_filling([cl_15d_35_36_13d])
        s_13d_36_37_27d = gmsh.model.geo.add_surface_filling([cl_13d_36_37_27d])
        
        s_28_26e_41e_38 = gmsh.model.geo.add_surface_filling([cl_28_26e_41e_38])
        s_26e_33_39_41e = gmsh.model.geo.add_surface_filling([cl_26e_33_39_41e])
        s_26d_33_39_41d = gmsh.model.geo.add_surface_filling([cl_26d_33_39_41d])
        s_28_26d_41d_38 = gmsh.model.geo.add_surface_filling([cl_28_26d_41d_38])

        s_38_41e_42 = gmsh.model.geo.add_surface_filling([cl_38_41e_42])
        s_41e_39_42 = gmsh.model.geo.add_surface_filling([cl_41e_39_42])
        s_41d_38_42 = gmsh.model.geo.add_surface_filling([cl_41d_38_42])
        s_39_41d_42 = gmsh.model.geo.add_surface_filling([cl_39_41d_42])

        s_27_47_43_e = gmsh.model.geo.add_surface_filling([cl_27_47_43_e])
        s_27e_43e_45_32 = gmsh.model.geo.add_surface_filling([cl_27e_43e_45_32])
        s_32_45_43d_27d = gmsh.model.geo.add_surface_filling([cl_32_45_43d_27d])
        s_43_47_27_d = gmsh.model.geo.add_surface_filling([cl_43_47_27_d])
        s_43_47_49_e = gmsh.model.geo.add_surface_filling([cl_43_47_49_e])
        s_43e_49e_51_45 = gmsh.model.geo.add_surface_filling([cl_43e_49e_51_45])
        s_45_51_49d_43d = gmsh.model.geo.add_surface_filling([cl_45_51_49d_43d])
        s_49_47_43_d = gmsh.model.geo.add_surface_filling([cl_49_47_43_d])

        s_27_47_44_e = gmsh.model.geo.add_surface_filling([cl_27_47_44_e])
        s_27e_44e_46_37 = gmsh.model.geo.add_surface_filling([cl_27e_44e_46_37])
        s_37_46_44d_27d = gmsh.model.geo.add_surface_filling([cl_37_46_44d_27d])
        s_44_47_27_d = gmsh.model.geo.add_surface_filling([cl_44_47_27_d])
        s_44_47_49_e = gmsh.model.geo.add_surface_filling([cl_44_47_49_e])
        s_44e_49e_51_46 = gmsh.model.geo.add_surface_filling([cl_44e_49e_51_46])
        s_46_51_49d_44d = gmsh.model.geo.add_surface_filling([cl_46_51_49d_44d])
        s_49_47_44_d = gmsh.model.geo.add_surface_filling([cl_49_47_44_d])

        #------------------------------------------#
        # Synchronize                              #
        #------------------------------------------#
        gmsh.model.geo.synchronize()

        #------------------------------------------#
        # Transfinite                              #
        #------------------------------------------#
        gmsh.model.mesh.set_transfinite_curve(curve_1_2_e, refinement.wing.sections[0].nodes, refinement.wing.sections[0].ref_type, refinement.wing.sections[0].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_2_3_e, refinement.wing.sections[1].nodes, refinement.wing.sections[1].ref_type, -refinement.wing.sections[1].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_3_4_e, refinement.wing.sections[2].nodes, refinement.wing.sections[2].ref_type, refinement.wing.sections[2].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_4_5_e, refinement.wing.sections[3].nodes, refinement.wing.sections[3].ref_type, refinement.wing.sections[3].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_5_6_e, refinement.wing.sections[4].nodes, refinement.wing.sections[4].ref_type, -refinement.wing.sections[4].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_6_7_e, refinement.wing.sections[5].nodes, refinement.wing.sections[5].ref_type, -refinement.wing.sections[5].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_7_8_e, refinement.wing.sections[5].nodes, refinement.wing.sections[5].ref_type, refinement.wing.sections[5].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_8_9_e, refinement.wing.sections[4].nodes, refinement.wing.sections[4].ref_type, refinement.wing.sections[4].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_9_10_e, refinement.wing.sections[3].nodes, refinement.wing.sections[3].ref_type, -refinement.wing.sections[3].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_10_11_e, refinement.wing.sections[2].nodes, refinement.wing.sections[2].ref_type, -refinement.wing.sections[2].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_11_12_e, refinement.wing.sections[1].nodes, refinement.wing.sections[1].ref_type, refinement.wing.sections[1].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_12_13_e, refinement.wing.sections[0].nodes, refinement.wing.sections[0].ref_type, -refinement.wing.sections[0].coef)

        gmsh.model.mesh.set_transfinite_curve(curve_14_16_e, refinement.wing.sections[0].nodes, refinement.wing.sections[0].ref_type, refinement.wing.sections[0].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_16_18_e, refinement.wing.sections[1].nodes, refinement.wing.sections[1].ref_type, -refinement.wing.sections[1].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_18_20_e, refinement.wing.sections[2].nodes, refinement.wing.sections[2].ref_type, refinement.wing.sections[2].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_20_22_e, refinement.wing.sections[3].nodes, refinement.wing.sections[3].ref_type, refinement.wing.sections[3].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_22_24_e, refinement.wing.sections[4].nodes, refinement.wing.sections[4].ref_type, -refinement.wing.sections[4].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_24_7_e, refinement.wing.sections[5].nodes, refinement.wing.sections[5].ref_type, -refinement.wing.sections[5].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_15_17_e, refinement.wing.sections[0].nodes, refinement.wing.sections[0].ref_type, refinement.wing.sections[0].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_17_19_e, refinement.wing.sections[1].nodes, refinement.wing.sections[1].ref_type, -refinement.wing.sections[1].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_19_21_e, refinement.wing.sections[2].nodes, refinement.wing.sections[2].ref_type, refinement.wing.sections[2].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_21_23_e, refinement.wing.sections[3].nodes, refinement.wing.sections[3].ref_type, refinement.wing.sections[3].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_23_25_e, refinement.wing.sections[4].nodes, refinement.wing.sections[4].ref_type, -refinement.wing.sections[4].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_25_7_e, refinement.wing.sections[5].nodes, refinement.wing.sections[5].ref_type, -refinement.wing.sections[5].coef)

        gmsh.model.mesh.set_transfinite_curve(curve_14_1_e, refinement.wing.n_chord_le, 'Progression', - refinement.wing.coef_le)
        gmsh.model.mesh.set_transfinite_curve(curve_16_2_e, refinement.wing.n_chord_le, 'Progression', - refinement.wing.coef_le)
        gmsh.model.mesh.set_transfinite_curve(curve_18_3_e, refinement.wing.n_chord_le, 'Progression', - refinement.wing.coef_le)
        gmsh.model.mesh.set_transfinite_curve(curve_20_4_e, refinement.wing.n_chord_le, 'Progression', - refinement.wing.coef_le)
        gmsh.model.mesh.set_transfinite_curve(curve_22_5_e, refinement.wing.n_chord_le, 'Progression', - refinement.wing.coef_le)
        gmsh.model.mesh.set_transfinite_curve(curve_24_6_e, refinement.wing.n_chord_le, 'Progression', 1.0) # - refinement.wing.coef_le)

        gmsh.model.mesh.set_transfinite_curve(curve_13_14_e, refinement.wing.n_chord_te, 'Progression', refinement.wing.coef_te)
        gmsh.model.mesh.set_transfinite_curve(curve_12_16_e, refinement.wing.n_chord_te, 'Progression', refinement.wing.coef_te)
        gmsh.model.mesh.set_transfinite_curve(curve_11_18_e, refinement.wing.n_chord_te, 'Progression', refinement.wing.coef_te)
        gmsh.model.mesh.set_transfinite_curve(curve_10_20_e, refinement.wing.n_chord_te, 'Progression', refinement.wing.coef_te)
        gmsh.model.mesh.set_transfinite_curve(curve_9_22_e, refinement.wing.n_chord_te, 'Progression', refinement.wing.coef_te)
        gmsh.model.mesh.set_transfinite_curve(curve_8_24_e, refinement.wing.n_chord_te, 'Progression', 1.0) # refinement.wing.coef_te)

        gmsh.model.mesh.set_transfinite_curve(curve_15_1_e, refinement.wing.n_chord_le, 'Progression', - refinement.wing.coef_le)
        gmsh.model.mesh.set_transfinite_curve(curve_17_2_e, refinement.wing.n_chord_le, 'Progression', - refinement.wing.coef_le)
        gmsh.model.mesh.set_transfinite_curve(curve_19_3_e, refinement.wing.n_chord_le, 'Progression', - refinement.wing.coef_le)
        gmsh.model.mesh.set_transfinite_curve(curve_21_4_e, refinement.wing.n_chord_le, 'Progression', - refinement.wing.coef_le)
        gmsh.model.mesh.set_transfinite_curve(curve_23_5_e, refinement.wing.n_chord_le, 'Progression', - refinement.wing.coef_le)
        gmsh.model.mesh.set_transfinite_curve(curve_25_6_e, refinement.wing.n_chord_le, 'Progression', 1.0) # - refinement.wing.coef_le)

        gmsh.model.mesh.set_transfinite_curve(curve_13_15_e, refinement.wing.n_chord_te, 'Progression', refinement.wing.coef_te)
        gmsh.model.mesh.set_transfinite_curve(curve_12_17_e, refinement.wing.n_chord_te, 'Progression', refinement.wing.coef_te)
        gmsh.model.mesh.set_transfinite_curve(curve_11_19_e, refinement.wing.n_chord_te, 'Progression', refinement.wing.coef_te)
        gmsh.model.mesh.set_transfinite_curve(curve_10_21_e, refinement.wing.n_chord_te, 'Progression', refinement.wing.coef_te)
        gmsh.model.mesh.set_transfinite_curve(curve_9_23_e, refinement.wing.n_chord_te, 'Progression', refinement.wing.coef_te)
        gmsh.model.mesh.set_transfinite_curve(curve_8_25_e, refinement.wing.n_chord_te, 'Progression', 1.0) # refinement.wing.coef_te)

        gmsh.model.mesh.set_transfinite_surface(s_1_2_16_14_e)
        gmsh.model.mesh.set_transfinite_surface(s_2_3_18_16_e)
        gmsh.model.mesh.set_transfinite_surface(s_3_4_20_18_e)
        gmsh.model.mesh.set_transfinite_surface(s_4_5_22_20_e)
        gmsh.model.mesh.set_transfinite_surface(s_5_6_24_22_e)
        gmsh.model.mesh.set_transfinite_surface(s_6_7_24_e)

        gmsh.model.mesh.set_transfinite_surface(s_14_16_12_13_e)
        gmsh.model.mesh.set_transfinite_surface(s_16_18_11_12_e)
        gmsh.model.mesh.set_transfinite_surface(s_18_20_10_11_e)
        gmsh.model.mesh.set_transfinite_surface(s_20_22_9_10_e)
        gmsh.model.mesh.set_transfinite_surface(s_22_24_8_9_e)
        gmsh.model.mesh.set_transfinite_surface(s_24_7_8_e)

        gmsh.model.mesh.set_transfinite_surface(s_1_15_17_2_e)
        gmsh.model.mesh.set_transfinite_surface(s_2_17_19_3_e)
        gmsh.model.mesh.set_transfinite_surface(s_3_19_21_4_e)
        gmsh.model.mesh.set_transfinite_surface(s_4_21_23_5_e)
        gmsh.model.mesh.set_transfinite_surface(s_5_23_25_6_e)
        gmsh.model.mesh.set_transfinite_surface(s_6_25_7_e)

        gmsh.model.mesh.set_transfinite_surface(s_15_13_12_17_e)
        gmsh.model.mesh.set_transfinite_surface(s_17_12_11_19_e)
        gmsh.model.mesh.set_transfinite_surface(s_19_11_10_21_e)
        gmsh.model.mesh.set_transfinite_surface(s_21_10_9_23_e)
        gmsh.model.mesh.set_transfinite_surface(s_23_9_8_25_e)
        gmsh.model.mesh.set_transfinite_surface(s_25_12_7_e)

        gmsh.model.mesh.set_transfinite_curve(curve_1_2_d, refinement.wing.sections[0].nodes, refinement.wing.sections[0].ref_type, refinement.wing.sections[0].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_2_3_d, refinement.wing.sections[1].nodes, refinement.wing.sections[1].ref_type, -refinement.wing.sections[1].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_3_4_d, refinement.wing.sections[2].nodes, refinement.wing.sections[2].ref_type, refinement.wing.sections[2].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_4_5_d, refinement.wing.sections[3].nodes, refinement.wing.sections[3].ref_type, refinement.wing.sections[3].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_5_6_d, refinement.wing.sections[4].nodes, refinement.wing.sections[4].ref_type, -refinement.wing.sections[4].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_6_7_d, refinement.wing.sections[5].nodes, refinement.wing.sections[5].ref_type, -refinement.wing.sections[5].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_7_8_d, refinement.wing.sections[5].nodes, refinement.wing.sections[5].ref_type, refinement.wing.sections[5].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_8_9_d, refinement.wing.sections[4].nodes, refinement.wing.sections[4].ref_type, refinement.wing.sections[4].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_9_10_d, refinement.wing.sections[3].nodes, refinement.wing.sections[3].ref_type, -refinement.wing.sections[3].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_10_11_d, refinement.wing.sections[2].nodes, refinement.wing.sections[2].ref_type, -refinement.wing.sections[2].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_11_12_d, refinement.wing.sections[1].nodes, refinement.wing.sections[1].ref_type, refinement.wing.sections[1].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_12_13_d, refinement.wing.sections[0].nodes, refinement.wing.sections[0].ref_type, -refinement.wing.sections[0].coef)

        gmsh.model.mesh.set_transfinite_curve(curve_14_16_d, refinement.wing.sections[0].nodes, refinement.wing.sections[0].ref_type, refinement.wing.sections[0].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_16_18_d, refinement.wing.sections[1].nodes, refinement.wing.sections[1].ref_type, -refinement.wing.sections[1].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_18_20_d, refinement.wing.sections[2].nodes, refinement.wing.sections[2].ref_type, refinement.wing.sections[2].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_20_22_d, refinement.wing.sections[3].nodes, refinement.wing.sections[3].ref_type, refinement.wing.sections[3].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_22_24_d, refinement.wing.sections[4].nodes, refinement.wing.sections[4].ref_type, -refinement.wing.sections[4].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_24_7_d, refinement.wing.sections[5].nodes, refinement.wing.sections[5].ref_type, -refinement.wing.sections[5].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_15_17_d, refinement.wing.sections[0].nodes, refinement.wing.sections[0].ref_type, refinement.wing.sections[0].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_17_19_d, refinement.wing.sections[1].nodes, refinement.wing.sections[1].ref_type, -refinement.wing.sections[1].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_19_21_d, refinement.wing.sections[2].nodes, refinement.wing.sections[2].ref_type, refinement.wing.sections[2].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_21_23_d, refinement.wing.sections[3].nodes, refinement.wing.sections[3].ref_type, refinement.wing.sections[3].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_23_25_d, refinement.wing.sections[4].nodes, refinement.wing.sections[4].ref_type, -refinement.wing.sections[4].coef)
        gmsh.model.mesh.set_transfinite_curve(curve_25_7_d, refinement.wing.sections[5].nodes, refinement.wing.sections[5].ref_type, -refinement.wing.sections[5].coef)

        gmsh.model.mesh.set_transfinite_curve(curve_14_1_d, refinement.wing.n_chord_le, 'Progression', - refinement.wing.coef_le)
        gmsh.model.mesh.set_transfinite_curve(curve_16_2_d, refinement.wing.n_chord_le, 'Progression', - refinement.wing.coef_le)
        gmsh.model.mesh.set_transfinite_curve(curve_18_3_d, refinement.wing.n_chord_le, 'Progression', - refinement.wing.coef_le)
        gmsh.model.mesh.set_transfinite_curve(curve_20_4_d, refinement.wing.n_chord_le, 'Progression', - refinement.wing.coef_le)
        gmsh.model.mesh.set_transfinite_curve(curve_22_5_d, refinement.wing.n_chord_le, 'Progression', - refinement.wing.coef_le)
        gmsh.model.mesh.set_transfinite_curve(curve_24_6_d, refinement.wing.n_chord_le, 'Progression', 1.0) # - refinement.wing.coef_le)

        gmsh.model.mesh.set_transfinite_curve(curve_13_14_d, refinement.wing.n_chord_te, 'Progression', refinement.wing.coef_te)
        gmsh.model.mesh.set_transfinite_curve(curve_12_16_d, refinement.wing.n_chord_te, 'Progression', refinement.wing.coef_te)
        gmsh.model.mesh.set_transfinite_curve(curve_11_18_d, refinement.wing.n_chord_te, 'Progression', refinement.wing.coef_te)
        gmsh.model.mesh.set_transfinite_curve(curve_10_20_d, refinement.wing.n_chord_te, 'Progression', refinement.wing.coef_te)
        gmsh.model.mesh.set_transfinite_curve(curve_9_22_d, refinement.wing.n_chord_te, 'Progression', refinement.wing.coef_te)
        gmsh.model.mesh.set_transfinite_curve(curve_8_24_d, refinement.wing.n_chord_te, 'Progression', 1.0) # refinement.wing.coef_te)

        gmsh.model.mesh.set_transfinite_curve(curve_15_1_d, refinement.wing.n_chord_le, 'Progression', - refinement.wing.coef_le)
        gmsh.model.mesh.set_transfinite_curve(curve_17_2_d, refinement.wing.n_chord_le, 'Progression', - refinement.wing.coef_le)
        gmsh.model.mesh.set_transfinite_curve(curve_19_3_d, refinement.wing.n_chord_le, 'Progression', - refinement.wing.coef_le)
        gmsh.model.mesh.set_transfinite_curve(curve_21_4_d, refinement.wing.n_chord_le, 'Progression', - refinement.wing.coef_le)
        gmsh.model.mesh.set_transfinite_curve(curve_23_5_d, refinement.wing.n_chord_le, 'Progression', - refinement.wing.coef_le)
        gmsh.model.mesh.set_transfinite_curve(curve_25_6_d, refinement.wing.n_chord_le, 'Progression', 1.0) # - refinement.wing.coef_le)

        gmsh.model.mesh.set_transfinite_curve(curve_13_15_d, refinement.wing.n_chord_te, 'Progression', refinement.wing.coef_te)
        gmsh.model.mesh.set_transfinite_curve(curve_12_17_d, refinement.wing.n_chord_te, 'Progression', refinement.wing.coef_te)
        gmsh.model.mesh.set_transfinite_curve(curve_11_19_d, refinement.wing.n_chord_te, 'Progression', refinement.wing.coef_te)
        gmsh.model.mesh.set_transfinite_curve(curve_10_21_d, refinement.wing.n_chord_te, 'Progression', refinement.wing.coef_te)
        gmsh.model.mesh.set_transfinite_curve(curve_9_23_d, refinement.wing.n_chord_te, 'Progression', refinement.wing.coef_te)
        gmsh.model.mesh.set_transfinite_curve(curve_8_25_d, refinement.wing.n_chord_te, 'Progression', 1.0) # refinement.wing.coef_te)

        ################################

        gmsh.model.mesh.set_transfinite_curve(curve_45_43e, ceil(refinement.body.n_cross_body / 2) + 1, 'Progression', 1.0)
        gmsh.model.mesh.set_transfinite_curve(curve_45_43d, ceil(refinement.body.n_cross_body / 2) + 1, 'Progression', 1.0)
        gmsh.model.mesh.set_transfinite_curve(curve_49e_51, ceil(refinement.body.n_cross_body / 2) + 1, 'Progression', 1.0)
        gmsh.model.mesh.set_transfinite_curve(curve_49d_51, ceil(refinement.body.n_cross_body / 2) + 1, 'Progression', 1.0)
        gmsh.model.mesh.set_transfinite_curve(curve_46_44e, ceil(refinement.body.n_cross_body / 2) + 1, 'Progression', 1.0)
        gmsh.model.mesh.set_transfinite_curve(curve_46_44d, ceil(refinement.body.n_cross_body / 2) + 1, 'Progression', 1.0)

        gmsh.model.mesh.set_transfinite_curve(curve_37_46, refinement.tail.n_1, 'Progression', refinement.tail.coef_edge_le)
        gmsh.model.mesh.set_transfinite_curve(curve_32_45, refinement.tail.n_1, 'Progression', refinement.tail.coef_edge_le)
        gmsh.model.mesh.set_transfinite_curve(curve_43_27_e, refinement.tail.n_1, 'Progression', -refinement.tail.coef_edge_le)
        gmsh.model.mesh.set_transfinite_curve(curve_43_27_d, refinement.tail.n_1, 'Progression', -refinement.tail.coef_edge_le)
        gmsh.model.mesh.set_transfinite_curve(curve_44_27_e, refinement.tail.n_1, 'Progression', -refinement.tail.coef_edge_le)
        gmsh.model.mesh.set_transfinite_curve(curve_44_27_d, refinement.tail.n_1, 'Progression', -refinement.tail.coef_edge_le)

        gmsh.model.mesh.set_transfinite_curve(curve_49_43_e, refinement.tail.n_2, 'Progression', refinement.tail.coef_edge_te)
        gmsh.model.mesh.set_transfinite_curve(curve_49_43_d, refinement.tail.n_2, 'Progression', refinement.tail.coef_edge_te)
        gmsh.model.mesh.set_transfinite_curve(curve_49_44_e, refinement.tail.n_2, 'Progression', refinement.tail.coef_edge_te)
        gmsh.model.mesh.set_transfinite_curve(curve_49_44_d, refinement.tail.n_2, 'Progression', refinement.tail.coef_edge_te)
        gmsh.model.mesh.set_transfinite_curve(curve_45_51, refinement.tail.n_2, 'Progression', -refinement.tail.coef_edge_te)
        gmsh.model.mesh.set_transfinite_curve(curve_46_51, refinement.tail.n_2, 'Progression', -refinement.tail.coef_edge_te)

        gmsh.model.mesh.set_transfinite_curve(curve_43_47_e, refinement.tail.n_edge, 'Progression', refinement.tail.coef_tip)
        gmsh.model.mesh.set_transfinite_curve(curve_43_47_d, refinement.tail.n_edge, 'Progression', refinement.tail.coef_tip)
        gmsh.model.mesh.set_transfinite_curve(curve_44_47_e, refinement.tail.n_edge, 'Progression', refinement.tail.coef_tip)
        gmsh.model.mesh.set_transfinite_curve(curve_44_47_d, refinement.tail.n_edge, 'Progression', refinement.tail.coef_tip)
        gmsh.model.mesh.set_transfinite_curve(curve_27_47_e, refinement.tail.n_edge, 'Progression', -refinement.tail.coef_tip)
        gmsh.model.mesh.set_transfinite_curve(curve_27_47_d, refinement.tail.n_edge, 'Progression', -refinement.tail.coef_tip)
        gmsh.model.mesh.set_transfinite_curve(curve_47_49_e, refinement.tail.n_edge, 'Progression', refinement.tail.coef_tip)
        gmsh.model.mesh.set_transfinite_curve(curve_47_49_d, refinement.tail.n_edge, 'Progression', refinement.tail.coef_tip)

        gmsh.model.mesh.set_transfinite_surface(s_27_47_44_e)
        gmsh.model.mesh.set_transfinite_surface(s_27e_44e_46_37)
        gmsh.model.mesh.set_transfinite_surface(s_37_46_44d_27d)
        gmsh.model.mesh.set_transfinite_surface(s_44_47_27_d)
        gmsh.model.mesh.set_transfinite_surface(s_44_47_49_e)
        gmsh.model.mesh.set_transfinite_surface(s_44e_49e_51_46)
        gmsh.model.mesh.set_transfinite_surface(s_46_51_49d_44d)
        gmsh.model.mesh.set_transfinite_surface(s_49_47_44_d)

        gmsh.model.mesh.set_transfinite_surface(s_27_47_43_e)
        gmsh.model.mesh.set_transfinite_surface(s_27e_43e_45_32)
        gmsh.model.mesh.set_transfinite_surface(s_32_45_43d_27d)
        gmsh.model.mesh.set_transfinite_surface(s_43_47_27_d)
        gmsh.model.mesh.set_transfinite_surface(s_43_47_49_e)
        gmsh.model.mesh.set_transfinite_surface(s_43e_49e_51_45)
        gmsh.model.mesh.set_transfinite_surface(s_45_51_49d_43d)
        gmsh.model.mesh.set_transfinite_surface(s_49_47_43_d)

        gmsh.model.mesh.set_recombine(2, s_27_47_44_e)
        gmsh.model.mesh.set_recombine(2, s_27e_44e_46_37)
        gmsh.model.mesh.set_recombine(2, s_37_46_44d_27d)
        gmsh.model.mesh.set_recombine(2, s_44_47_27_d)
        gmsh.model.mesh.set_recombine(2, s_44_47_49_e)
        gmsh.model.mesh.set_recombine(2, s_44e_49e_51_46)
        gmsh.model.mesh.set_recombine(2, s_46_51_49d_44d)
        gmsh.model.mesh.set_recombine(2, s_49_47_44_d)

        gmsh.model.mesh.set_recombine(2, s_27_47_43_e)
        gmsh.model.mesh.set_recombine(2, s_27e_43e_45_32)
        gmsh.model.mesh.set_recombine(2, s_32_45_43d_27d)
        gmsh.model.mesh.set_recombine(2, s_43_47_27_d)
        gmsh.model.mesh.set_recombine(2, s_43_47_49_e)
        gmsh.model.mesh.set_recombine(2, s_43e_49e_51_45)
        gmsh.model.mesh.set_recombine(2, s_45_51_49d_43d)
        gmsh.model.mesh.set_recombine(2, s_49_47_43_d)

        gmsh.model.mesh.set_transfinite_surface(s_1_2_16_14_d)
        gmsh.model.mesh.set_transfinite_surface(s_2_3_18_16_d)
        gmsh.model.mesh.set_transfinite_surface(s_3_4_20_18_d)
        gmsh.model.mesh.set_transfinite_surface(s_4_5_22_20_d)
        gmsh.model.mesh.set_transfinite_surface(s_5_6_24_22_d)
        gmsh.model.mesh.set_transfinite_surface(s_6_7_24_d)

        gmsh.model.mesh.set_transfinite_surface(s_14_16_12_13_d)
        gmsh.model.mesh.set_transfinite_surface(s_16_18_11_12_d)
        gmsh.model.mesh.set_transfinite_surface(s_18_20_10_11_d)
        gmsh.model.mesh.set_transfinite_surface(s_20_22_9_10_d)
        gmsh.model.mesh.set_transfinite_surface(s_22_24_8_9_d)
        gmsh.model.mesh.set_transfinite_surface(s_24_7_8_d)

        gmsh.model.mesh.set_transfinite_surface(s_1_15_17_2_d)
        gmsh.model.mesh.set_transfinite_surface(s_2_17_19_3_d)
        gmsh.model.mesh.set_transfinite_surface(s_3_19_21_4_d)
        gmsh.model.mesh.set_transfinite_surface(s_4_21_23_5_d)
        gmsh.model.mesh.set_transfinite_surface(s_5_23_25_6_d)
        gmsh.model.mesh.set_transfinite_surface(s_6_25_7_d)

        gmsh.model.mesh.set_transfinite_surface(s_15_13_12_17_d)
        gmsh.model.mesh.set_transfinite_surface(s_17_12_11_19_d)
        gmsh.model.mesh.set_transfinite_surface(s_19_11_10_21_d)
        gmsh.model.mesh.set_transfinite_surface(s_21_10_9_23_d)
        gmsh.model.mesh.set_transfinite_surface(s_23_9_8_25_d)
        gmsh.model.mesh.set_transfinite_surface(s_25_12_7_d)

        gmsh.model.mesh.set_transfinite_curve(curve_29_30, refinement.wing.n_chord_le, 'Progression', refinement.wing.coef_le)
        gmsh.model.mesh.set_transfinite_curve(curve_30_31, refinement.wing.n_chord_te, 'Progression', -refinement.wing.coef_te)
        gmsh.model.mesh.set_transfinite_curve(curve_34_35, refinement.wing.n_chord_le, 'Progression', refinement.wing.coef_le)
        gmsh.model.mesh.set_transfinite_curve(curve_35_36, refinement.wing.n_chord_te, 'Progression', -refinement.wing.coef_te)
        
        gmsh.model.mesh.set_transfinite_curve(curve_28_26_e, ceil(refinement.body.n_cross_body / 2) + 1, 'Progression', -refinement.body.coef_cross_body)
        gmsh.model.mesh.set_transfinite_curve(curve_26d_28, ceil(refinement.body.n_cross_body / 2) + 1, 'Progression', refinement.body.coef_cross_body)
        gmsh.model.mesh.set_transfinite_curve(curve_29_1_e, ceil(refinement.body.n_cross_body / 2) + 1, 'Progression', -refinement.body.coef_cross_body)
        gmsh.model.mesh.set_transfinite_curve(curve_29_1_d, ceil(refinement.body.n_cross_body / 2) + 1, 'Progression', -refinement.body.coef_cross_body)
        gmsh.model.mesh.set_transfinite_curve(curve_30_14_e, ceil(refinement.body.n_cross_body / 2) + 1, 'Progression', -refinement.body.coef_cross_body)
        gmsh.model.mesh.set_transfinite_curve(curve_30_14_d, ceil(refinement.body.n_cross_body / 2) + 1, 'Progression', -refinement.body.coef_cross_body)
        gmsh.model.mesh.set_transfinite_curve(curve_31_13_e, ceil(refinement.body.n_cross_body / 2) + 1, 'Progression', -refinement.body.coef_cross_body)
        gmsh.model.mesh.set_transfinite_curve(curve_31_13_d, ceil(refinement.body.n_cross_body / 2) + 1, 'Progression', -refinement.body.coef_cross_body)
        gmsh.model.mesh.set_transfinite_curve(curve_32_27_e, ceil(refinement.body.n_cross_body / 2) + 1, 'Progression', -refinement.body.coef_cross_body)
        gmsh.model.mesh.set_transfinite_curve(curve_32_27_d, ceil(refinement.body.n_cross_body / 2) + 1, 'Progression', -refinement.body.coef_cross_body)
        gmsh.model.mesh.set_transfinite_curve(curve_1e_34, ceil(refinement.body.n_cross_body / 2) + 1, 'Progression', refinement.body.coef_cross_body)
        
        gmsh.model.mesh.set_transfinite_curve(curve_26e_33, ceil(refinement.body.n_cross_body / 2) + 1, 'Progression', refinement.body.coef_cross_body)
        gmsh.model.mesh.set_transfinite_curve(curve_33_26_d, ceil(refinement.body.n_cross_body / 2) + 1, 'Progression', -refinement.body.coef_cross_body)
        gmsh.model.mesh.set_transfinite_curve(curve_1d_34, ceil(refinement.body.n_cross_body / 2) + 1, 'Progression', refinement.body.coef_cross_body)
        gmsh.model.mesh.set_transfinite_curve(curve_15e_35, ceil(refinement.body.n_cross_body / 2) + 1, 'Progression', refinement.body.coef_cross_body)
        gmsh.model.mesh.set_transfinite_curve(curve_15d_35, ceil(refinement.body.n_cross_body / 2) + 1, 'Progression', refinement.body.coef_cross_body)
        gmsh.model.mesh.set_transfinite_curve(curve_13e_36, ceil(refinement.body.n_cross_body / 2) + 1, 'Progression', refinement.body.coef_cross_body)
        gmsh.model.mesh.set_transfinite_curve(curve_13d_36, ceil(refinement.body.n_cross_body / 2) + 1, 'Progression', refinement.body.coef_cross_body)
        gmsh.model.mesh.set_transfinite_curve(curve_27e_37, ceil(refinement.body.n_cross_body / 2) + 1, 'Progression', refinement.body.coef_cross_body)
        gmsh.model.mesh.set_transfinite_curve(curve_27d_37, ceil(refinement.body.n_cross_body / 2) + 1, 'Progression', refinement.body.coef_cross_body)
        gmsh.model.mesh.set_transfinite_curve(curve_32_27_d, ceil(refinement.body.n_cross_body / 2) + 1, 'Progression', -refinement.body.coef_cross_body)

        gmsh.model.mesh.set_transfinite_curve(curve_31_32, refinement.body.n_tail, 'Progression', refinement.body.coef_tail)
        gmsh.model.mesh.set_transfinite_curve(curve_36_37, refinement.body.n_tail, 'Progression', refinement.body.coef_tail)
        gmsh.model.mesh.set_transfinite_curve(curve_13_27_e, refinement.body.n_tail, 'Progression', refinement.body.coef_tail)
        gmsh.model.mesh.set_transfinite_curve(curve_13_27_d, refinement.body.n_tail, 'Progression', refinement.body.coef_tail)

        gmsh.model.mesh.set_transfinite_curve(curve_28_29, refinement.body.n_head, 'Progression', -refinement.body.coef_head)
        gmsh.model.mesh.set_transfinite_curve(curve_33_34, refinement.body.n_head, 'Progression', -refinement.body.coef_head)
        gmsh.model.mesh.set_transfinite_curve(curve_26_1_e, refinement.body.n_head, 'Progression', -refinement.body.coef_head)
        gmsh.model.mesh.set_transfinite_curve(curve_26_1_d, refinement.body.n_head, 'Progression', -refinement.body.coef_head)

        gmsh.model.mesh.set_transfinite_curve(curve_38_41e, ceil(refinement.body.n_cross_body / 2) + 1)
        gmsh.model.mesh.set_transfinite_curve(curve_38_41d, ceil(refinement.body.n_cross_body / 2) + 1)
        gmsh.model.mesh.set_transfinite_curve(curve_41e_39, ceil(refinement.body.n_cross_body / 2) + 1)
        gmsh.model.mesh.set_transfinite_curve(curve_41d_39, ceil(refinement.body.n_cross_body / 2) + 1)

        gmsh.model.mesh.set_transfinite_curve(curve_28_38, refinement.head.n_1, 'Progression', -refinement.head.coef_1)
        gmsh.model.mesh.set_transfinite_curve(curve_26_41_e, refinement.head.n_1, 'Progression', -refinement.head.coef_1)
        gmsh.model.mesh.set_transfinite_curve(curve_33_39, refinement.head.n_1, 'Progression', -refinement.head.coef_1)
        gmsh.model.mesh.set_transfinite_curve(curve_26_41_d, refinement.head.n_1, 'Progression', -refinement.head.coef_1)

        gmsh.model.mesh.set_transfinite_curve(curve_38_42, refinement.head.n_2, 'Progression', -refinement.head.coef_2)
        gmsh.model.mesh.set_transfinite_curve(curve_41e_42, refinement.head.n_2, 'Progression', -refinement.head.coef_2)
        gmsh.model.mesh.set_transfinite_curve(curve_39_42, refinement.head.n_2, 'Progression', -refinement.head.coef_2)
        gmsh.model.mesh.set_transfinite_curve(curve_41d_42, refinement.head.n_2, 'Progression', -refinement.head.coef_2)

        gmsh.model.mesh.set_transfinite_surface(s_1e_14e_30_29)
        gmsh.model.mesh.set_transfinite_surface(s_14e_13e_31_30)
        gmsh.model.mesh.set_transfinite_surface(s_1d_14d_30_29)
        gmsh.model.mesh.set_transfinite_surface(s_14d_13d_31_30)
        gmsh.model.mesh.set_transfinite_surface(s_31_13e_27e_32)
        gmsh.model.mesh.set_transfinite_surface(s_31_13d_27d_32)
        gmsh.model.mesh.set_transfinite_surface(s_26e_1e_29_28)
        gmsh.model.mesh.set_transfinite_surface(s_26d_1d_29_28)

        gmsh.model.mesh.set_transfinite_surface(s_26e_33_34_1e)
        gmsh.model.mesh.set_transfinite_surface(s_1e_34_35_15e)
        gmsh.model.mesh.set_transfinite_surface(s_15e_35_36_13e)
        gmsh.model.mesh.set_transfinite_surface(s_13e_36_37_27e)

        gmsh.model.mesh.set_transfinite_surface(s_26d_33_34_1d)
        gmsh.model.mesh.set_transfinite_surface(s_1d_34_35_15d)
        gmsh.model.mesh.set_transfinite_surface(s_15d_35_36_13d)
        gmsh.model.mesh.set_transfinite_surface(s_13d_36_37_27d)

        gmsh.model.mesh.set_transfinite_surface(s_28_26e_41e_38)
        gmsh.model.mesh.set_transfinite_surface(s_26e_33_39_41e)
        gmsh.model.mesh.set_transfinite_surface(s_26d_33_39_41d)
        gmsh.model.mesh.set_transfinite_surface(s_28_26d_41d_38)

        gmsh.model.mesh.set_transfinite_surface(s_38_41e_42)
        gmsh.model.mesh.set_transfinite_surface(s_41e_39_42)
        gmsh.model.mesh.set_transfinite_surface(s_41d_38_42)
        gmsh.model.mesh.set_transfinite_surface(s_39_41d_42)

        #------------------------------------------#
        # Quads                                    #
        #------------------------------------------#
        gmsh.model.mesh.set_recombine(2, s_1_2_16_14_e)
        gmsh.model.mesh.set_recombine(2, s_2_3_18_16_e)
        gmsh.model.mesh.set_recombine(2, s_3_4_20_18_e)
        gmsh.model.mesh.set_recombine(2, s_4_5_22_20_e)
        gmsh.model.mesh.set_recombine(2, s_5_6_24_22_e)
        gmsh.model.mesh.set_recombine(2, s_6_7_24_e)

        gmsh.model.mesh.set_recombine(2, s_14_16_12_13_e)
        gmsh.model.mesh.set_recombine(2, s_16_18_11_12_e)
        gmsh.model.mesh.set_recombine(2, s_18_20_10_11_e)
        gmsh.model.mesh.set_recombine(2, s_20_22_9_10_e)
        gmsh.model.mesh.set_recombine(2, s_22_24_8_9_e)
        gmsh.model.mesh.set_recombine(2, s_24_7_8_e)

        gmsh.model.mesh.set_recombine(2, s_1_15_17_2_e)
        gmsh.model.mesh.set_recombine(2, s_2_17_19_3_e)
        gmsh.model.mesh.set_recombine(2, s_3_19_21_4_e)
        gmsh.model.mesh.set_recombine(2, s_4_21_23_5_e)
        gmsh.model.mesh.set_recombine(2, s_5_23_25_6_e)
        gmsh.model.mesh.set_recombine(2, s_6_25_7_e)

        gmsh.model.mesh.set_recombine(2, s_15_13_12_17_e)
        gmsh.model.mesh.set_recombine(2, s_17_12_11_19_e)
        gmsh.model.mesh.set_recombine(2, s_19_11_10_21_e)
        gmsh.model.mesh.set_recombine(2, s_21_10_9_23_e)
        gmsh.model.mesh.set_recombine(2, s_23_9_8_25_e)
        gmsh.model.mesh.set_recombine(2, s_25_12_7_e)

        gmsh.model.mesh.set_recombine(2, s_1_2_16_14_d)
        gmsh.model.mesh.set_recombine(2, s_2_3_18_16_d)
        gmsh.model.mesh.set_recombine(2, s_3_4_20_18_d)
        gmsh.model.mesh.set_recombine(2, s_4_5_22_20_d)
        gmsh.model.mesh.set_recombine(2, s_5_6_24_22_d)
        gmsh.model.mesh.set_recombine(2, s_6_7_24_d)

        gmsh.model.mesh.set_recombine(2, s_14_16_12_13_d)
        gmsh.model.mesh.set_recombine(2, s_16_18_11_12_d)
        gmsh.model.mesh.set_recombine(2, s_18_20_10_11_d)
        gmsh.model.mesh.set_recombine(2, s_20_22_9_10_d)
        gmsh.model.mesh.set_recombine(2, s_22_24_8_9_d)
        gmsh.model.mesh.set_recombine(2, s_24_7_8_d)

        gmsh.model.mesh.set_recombine(2, s_1_15_17_2_d)
        gmsh.model.mesh.set_recombine(2, s_2_17_19_3_d)
        gmsh.model.mesh.set_recombine(2, s_3_19_21_4_d)
        gmsh.model.mesh.set_recombine(2, s_4_21_23_5_d)
        gmsh.model.mesh.set_recombine(2, s_5_23_25_6_d)
        gmsh.model.mesh.set_recombine(2, s_6_25_7_d)

        gmsh.model.mesh.set_recombine(2, s_15_13_12_17_d)
        gmsh.model.mesh.set_recombine(2, s_17_12_11_19_d)
        gmsh.model.mesh.set_recombine(2, s_19_11_10_21_d)
        gmsh.model.mesh.set_recombine(2, s_21_10_9_23_d)
        gmsh.model.mesh.set_recombine(2, s_23_9_8_25_d)
        gmsh.model.mesh.set_recombine(2, s_25_12_7_d)

        gmsh.model.mesh.set_recombine(2, s_26e_1e_29_28)
        gmsh.model.mesh.set_recombine(2, s_26d_1d_29_28)
        gmsh.model.mesh.set_recombine(2, s_1e_14e_30_29)
        gmsh.model.mesh.set_recombine(2, s_14e_13e_31_30)
        gmsh.model.mesh.set_recombine(2, s_1d_14d_30_29)
        gmsh.model.mesh.set_recombine(2, s_14d_13d_31_30)
        gmsh.model.mesh.set_recombine(2, s_31_13e_27e_32)
        gmsh.model.mesh.set_recombine(2, s_31_13d_27d_32)

        gmsh.model.mesh.set_recombine(2, s_26e_33_34_1e)
        gmsh.model.mesh.set_recombine(2, s_1e_34_35_15e)
        gmsh.model.mesh.set_recombine(2, s_15e_35_36_13e)
        gmsh.model.mesh.set_recombine(2, s_13e_36_37_27e)
        gmsh.model.mesh.set_recombine(2, s_26d_33_34_1d)
        gmsh.model.mesh.set_recombine(2, s_1d_34_35_15d)
        gmsh.model.mesh.set_recombine(2, s_15d_35_36_13d)
        gmsh.model.mesh.set_recombine(2, s_13d_36_37_27d)

        gmsh.model.mesh.set_recombine(2, s_28_26e_41e_38)
        gmsh.model.mesh.set_recombine(2, s_26e_33_39_41e)
        gmsh.model.mesh.set_recombine(2, s_26d_33_39_41d)
        gmsh.model.mesh.set_recombine(2, s_28_26d_41d_38)

        gmsh.model.mesh.set_recombine(2, s_38_41e_42)
        gmsh.model.mesh.set_recombine(2, s_41e_39_42)
        gmsh.model.mesh.set_recombine(2, s_41d_38_42)
        gmsh.model.mesh.set_recombine(2, s_39_41d_42)

        #------------------------------------------#
        # Create                                   #
        #------------------------------------------#
        gmsh.model.mesh.generate(2)

        #------------------------------------------#
        # View                                     #
        #------------------------------------------#
        # if "-nopopup" not in sys.argv:
        #     gmsh.fltk.initialize()
        #     while gmsh.fltk.isAvailable():
        #         gmsh.fltk.wait()
        
        #------------------------------------------#
        # Data                                     #
        #------------------------------------------#

        # Vertices
        data = gmsh.model.mesh.get_nodes()
        vertices = data[1].reshape((data[0].size, 3))

        # Faces
        gmsh.model.mesh.create_faces()
        data = gmsh.model.mesh.get_all_faces(4)
        faces_4 = data[1].reshape((data[0].size, 4)).astype(int32) - 1
        data = gmsh.model.mesh.get_all_faces(3)
        faces_3 = data[1].reshape((data[0].size, 3)).astype(int32) - 1

        # Trailing edge
        trailing_edge_1_e = gmsh.model.add_physical_group(1, [curve_7_8_e])
        trailing_edge_2_e = gmsh.model.add_physical_group(1, [curve_8_9_e])
        trailing_edge_3_e = gmsh.model.add_physical_group(1, [curve_9_10_e])
        trailing_edge_4_e = gmsh.model.add_physical_group(1, [curve_10_11_e])
        trailing_edge_5_e = gmsh.model.add_physical_group(1, [curve_11_12_e])
        trailing_edge_6_e = gmsh.model.add_physical_group(1, [curve_12_13_e])

        trailing_edge_1_d = gmsh.model.add_physical_group(1, [curve_7_8_d])
        trailing_edge_2_d = gmsh.model.add_physical_group(1, [curve_8_9_d])
        trailing_edge_3_d = gmsh.model.add_physical_group(1, [curve_9_10_d])
        trailing_edge_4_d = gmsh.model.add_physical_group(1, [curve_10_11_d])
        trailing_edge_5_d = gmsh.model.add_physical_group(1, [curve_11_12_d])
        trailing_edge_6_d = gmsh.model.add_physical_group(1, [curve_12_13_d])

        trailing_edge_7_e = gmsh.model.add_physical_group(1, [curve_47_49_e])
        trailing_edge_8_e = gmsh.model.add_physical_group(1, [curve_49e_51])

        trailing_edge_7_d = gmsh.model.add_physical_group(1, [curve_47_49_d])
        trailing_edge_8_d = gmsh.model.add_physical_group(1, [curve_49d_51])


        trailing_edge_1_e = gmsh.model.mesh.get_nodes_for_physical_group(1, trailing_edge_1_e)[0] - 1
        trailing_edge_2_e = gmsh.model.mesh.get_nodes_for_physical_group(1, trailing_edge_2_e)[0] - 1
        trailing_edge_3_e = gmsh.model.mesh.get_nodes_for_physical_group(1, trailing_edge_3_e)[0] - 1
        trailing_edge_4_e = gmsh.model.mesh.get_nodes_for_physical_group(1, trailing_edge_4_e)[0] - 1
        trailing_edge_5_e = gmsh.model.mesh.get_nodes_for_physical_group(1, trailing_edge_5_e)[0] - 1
        trailing_edge_6_e = gmsh.model.mesh.get_nodes_for_physical_group(1, trailing_edge_6_e)[0] - 1
        trailing_edge_7_e = gmsh.model.mesh.get_nodes_for_physical_group(1, trailing_edge_7_e)[0] - 1
        trailing_edge_8_e = gmsh.model.mesh.get_nodes_for_physical_group(1, trailing_edge_8_e)[0] - 1

        trailing_edge_1_d = gmsh.model.mesh.get_nodes_for_physical_group(1, trailing_edge_1_d)[0] - 1
        trailing_edge_2_d = gmsh.model.mesh.get_nodes_for_physical_group(1, trailing_edge_2_d)[0] - 1
        trailing_edge_3_d = gmsh.model.mesh.get_nodes_for_physical_group(1, trailing_edge_3_d)[0] - 1
        trailing_edge_4_d = gmsh.model.mesh.get_nodes_for_physical_group(1, trailing_edge_4_d)[0] - 1
        trailing_edge_5_d = gmsh.model.mesh.get_nodes_for_physical_group(1, trailing_edge_5_d)[0] - 1
        trailing_edge_6_d = gmsh.model.mesh.get_nodes_for_physical_group(1, trailing_edge_6_d)[0] - 1
        trailing_edge_7_d = gmsh.model.mesh.get_nodes_for_physical_group(1, trailing_edge_7_d)[0] - 1
        trailing_edge_8_d = gmsh.model.mesh.get_nodes_for_physical_group(1, trailing_edge_8_d)[0] - 1

        #------------------------------------------#
        # End                                      #
        #------------------------------------------#
        gmsh.finalize()

        return [
            vertices,
            faces_3,
            faces_4,
            [
                trailing_edge_1_e,
                trailing_edge_2_e,
                trailing_edge_3_e,
                trailing_edge_4_e,
                trailing_edge_5_e,
                trailing_edge_6_e,
                trailing_edge_7_e,
                trailing_edge_8_e,
                trailing_edge_1_d,
                trailing_edge_2_d,
                trailing_edge_3_d,
                trailing_edge_4_d,
                trailing_edge_5_d,
                trailing_edge_6_d,
                trailing_edge_7_d,
                trailing_edge_8_d,
            ]
        ]

    def __correct_vertices_ids(self, vertices: ndarray, faces3: ndarray, faces4: ndarray, trailing_edge_list: List[ndarray]):
    
        # Saída
        vertices_out = []
        faces_out = []
        trailing_edge_out = []

        # Encontre os ids dos vértices utilizados na malha
        vertices_ids = []

        for id in range(vertices.shape[0]):

            is_in_f3 = id in faces3[:, 0] or id in faces3[:, 1] or id in faces3[:, 2]
            is_in_f4 = id in faces4[:, 0] or id in faces4[:, 1] or id in faces4[:, 2] or id in faces4[:, 3]

            if is_in_f3 or is_in_f4:
                vertices_ids.append(id)
        
        vertices_ids = asarray(vertices_ids)

        # Corrige os valores dos vértices
        for id in vertices_ids:
            vertices_out.append(vertices[id, :])

        # Corrige os valores das faces
        for face in faces4:
            id1 = int(argwhere(face[0] == vertices_ids)[0])
            id2 = int(argwhere(face[1] == vertices_ids)[0])
            id3 = int(argwhere(face[2] == vertices_ids)[0])
            id4 = int(argwhere(face[3] == vertices_ids)[0])
            faces_out.append([4, id1, id2, id3, id4])
        
        for face in faces3:
            id1 = int(argwhere(face[0] == vertices_ids)[0])
            id2 = int(argwhere(face[1] == vertices_ids)[0])
            id3 = int(argwhere(face[2] == vertices_ids)[0])
            faces_out.append([3, id1, id2, id3, -1])
        
        # Corrige os valores do bordo de fuga
        for points in trailing_edge_list:

            d1 = norm(vertices[points[0], :] - vertices[points[2], :])
            d2 = norm(vertices[points[0], :] - vertices[points[-1], :])

            if d1 < d2:
                points_ordered = points[2:]
            else:
                points_ordered = flip(points[2:])
            
            new_points = [points[0]]
            for i in range(len(points_ordered)):
                new_points.append(points_ordered[i])
            new_points.append(points[1])
            
            for i in range(len(new_points) - 1):
                id1 = int(argwhere(new_points[i] == vertices_ids)[0])
                id2 = int(argwhere(new_points[i + 1] == vertices_ids)[0])
                trailing_edge_out.append([id1, id2])
        
        # Converte para numpy array
        vertices_out = asarray(vertices_out)
        faces_out = asarray(faces_out)
        trailing_edge_out = asarray(trailing_edge_out)
        
        return [vertices_out, faces_out, trailing_edge_out]
