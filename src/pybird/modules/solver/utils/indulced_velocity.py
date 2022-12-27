from ctypes import CDLL, c_int, c_double, POINTER
from typing import List
from numpy import ndarray, empty, double, int32
from numpy.ctypeslib import as_ctypes

def get_Aij_and_Bi_coefs(nf: int,
                         faces: ndarray,
                         p_avg: ndarray,
                         p_ctrl: ndarray,
                         e1: ndarray,
                         e2: ndarray,
                         e3: ndarray,
                         p1: ndarray,
                         p2: ndarray,
                         p3: ndarray,
                         p4: ndarray,
                         areas: ndarray,
                         max_distances: ndarray,
                         scale: ndarray,
                         freestream: ndarray,
                         source: ndarray,
                         Aij: ndarray,
                         Bi: ndarray) -> None:

    Aij_x = empty(nf * nf, dtype=double)
    Aij_y = empty(nf * nf, dtype=double)
    Aij_z = empty(nf * nf, dtype=double)
    
    Bi_x = empty(nf, dtype=double)
    Bi_y = empty(nf, dtype=double)
    Bi_z = empty(nf, dtype=double)

    n_sides = empty(nf, dtype=int32)

    n_sides[:] = faces[:, 0]

    lib = CDLL('./src/pybird/modules/solver/bin/lib.so')

    lib.get_Aij_and_Bi_coefs.argtypes = [
        c_int,                      # n_v
        POINTER(c_int),             # n_sides
        POINTER(c_double),          # p_avg
        POINTER(c_double),          # p_ctrl
        POINTER(c_double),          # e1
        POINTER(c_double),          # e2
        POINTER(c_double),          # e3
        POINTER(c_double),          # p1
        POINTER(c_double),          # p2
        POINTER(c_double),          # p3
        POINTER(c_double),          # p4
        POINTER(c_double),          # areas
        POINTER(c_double),          # max_distances
        POINTER(c_double),          # scale
        POINTER(c_double),          # freestream
        POINTER(c_double),          # source
        POINTER(c_double),          # Aij_x
        POINTER(c_double),          # Aij_y
        POINTER(c_double),          # Aij_z
        POINTER(c_double),          # Bi_x
        POINTER(c_double),          # Bi_y
        POINTER(c_double),          # Bi_z
    ]

    lib.get_Aij_and_Bi_coefs.restype = None

    lib.get_Aij_and_Bi_coefs(
        nf,
        as_ctypes(n_sides),
        as_ctypes(p_avg.reshape(p_avg.size)),
        as_ctypes(p_ctrl.reshape(p_ctrl.size)),
        as_ctypes(e1.reshape(e1.size)),
        as_ctypes(e2.reshape(e2.size)),
        as_ctypes(e3.reshape(e3.size)),
        as_ctypes(p1.reshape(p1.size)),
        as_ctypes(p2.reshape(p2.size)),
        as_ctypes(p3.reshape(p3.size)),
        as_ctypes(p4.reshape(p4.size)),
        as_ctypes(areas),
        as_ctypes(max_distances),
        as_ctypes(scale),
        as_ctypes(freestream),
        as_ctypes(source),
        as_ctypes(Aij_x),
        as_ctypes(Aij_y),
        as_ctypes(Aij_z),
        as_ctypes(Bi_x),
        as_ctypes(Bi_y),
        as_ctypes(Bi_z),
    )

    Aij_x = Aij_x.reshape((nf, nf))
    Aij_y = Aij_y.reshape((nf, nf))
    Aij_z = Aij_z.reshape((nf, nf))

    Aij[:, :, 0] = Aij_x[:, :]
    Aij[:, :, 1] = Aij_y[:, :]
    Aij[:, :, 2] = Aij_z[:, :]

    Bi[:, 0] = Bi_x[:]
    Bi[:, 1] = Bi_y[:]
    Bi[:, 2] = Bi_z[:]

    return

def get_point_velocity(nf: int,
                       nte: int,
                       nw: int,
                       wake_id: int,
                       faces: ndarray,
                       p_avg: ndarray,
                       e1: ndarray,
                       e2: ndarray,
                       e3: ndarray,
                       p1: ndarray,
                       p2: ndarray,
                       p3: ndarray,
                       p4: ndarray,
                       areas: ndarray,
                       max_distances: ndarray,
                       freestream: ndarray,
                       source: ndarray,
                       doublet: ndarray,
                       wake_ids: ndarray,
                       wake_vertices: ndarray,
                       wake_areas: ndarray,
                       wake_circulation: ndarray,
                       p: ndarray,
                       skip_i: int,
                       skip_j: int) -> ndarray:

    vel = empty(3, dtype=double)

    n_sides = empty(nf, dtype=int32)
    n_sides[:] = faces[:, 0]

    lib = CDLL('./src/pybird/modules/solver/bin/lib.so')

    lib.get_point_velocity.argtypes = [
        c_int,                      # nf
        c_int,                      # nte
        c_int,                      # nw
        c_int,                      # wake_id
        POINTER(c_int),             # n_sides
        POINTER(c_double),          # p_avg
        POINTER(c_double),          # e1
        POINTER(c_double),          # e2
        POINTER(c_double),          # e3
        POINTER(c_double),          # p1
        POINTER(c_double),          # p2
        POINTER(c_double),          # p3
        POINTER(c_double),          # p4
        POINTER(c_double),          # areas
        POINTER(c_double),          # max_distances
        POINTER(c_double),          # freestream
        POINTER(c_double),          # source
        POINTER(c_double),          # doublet
        POINTER(c_int),             # wake_ids
        POINTER(c_double),          # wake_vertices
        POINTER(c_double),          # wake_areas
        POINTER(c_double),          # wake_circulation
        POINTER(c_double),          # p
        c_int,                      # skip_i
        c_int,                      # skip_j
        POINTER(c_double),          # vel
    ]

    lib.get_point_velocity.restype = None

    lib.get_point_velocity(
        nf,
        nte,
        nw,
        wake_id,
        as_ctypes(n_sides),
        as_ctypes(p_avg.reshape(-1)),
        as_ctypes(e1.reshape(-1)),
        as_ctypes(e2.reshape(-1)),
        as_ctypes(e3.reshape(-1)),
        as_ctypes(p1.reshape(-1)),
        as_ctypes(p2.reshape(-1)),
        as_ctypes(p3.reshape(-1)),
        as_ctypes(p4.reshape(-1)),
        as_ctypes(areas),
        as_ctypes(max_distances),
        as_ctypes(freestream),
        as_ctypes(source),
        as_ctypes(doublet),
        as_ctypes(wake_ids.reshape(-1)),
        as_ctypes(wake_vertices.reshape(-1)),
        as_ctypes(wake_areas.reshape(-1)),
        as_ctypes(wake_circulation.reshape(-1)),
        as_ctypes(p),
        skip_i,
        skip_j,
        as_ctypes(vel),
    )

    return vel

def get_Cij(nf: int,
            nte: int,
            nw: int,
            p_ctrl: ndarray,
            wake_ids: ndarray,
            wake_vertices: ndarray,
            Cij: ndarray) -> None:
    
    Cij_x = empty(nte * nf, dtype=double)
    Cij_y = empty(nte * nf, dtype=double)
    Cij_z = empty(nte * nf, dtype=double)

    lib = CDLL('./src/pybird/modules/solver/bin/lib.so')

    lib.get_point_velocity.argtypes = [
        c_int,                      # nf
        c_int,                      # nte
        c_int,                      # nw
        POINTER(c_double),          # p_ctrl
        POINTER(c_int),             # wake_ids
        POINTER(c_double),          # wake_vertices
        POINTER(c_double),          # Cij_x
        POINTER(c_double),          # Cij_y
        POINTER(c_double),          # Cij_z
    ]

    lib.get_Cij.restype = None

    lib.get_Cij(
        nf,
        nte,
        nw,
        as_ctypes(p_ctrl.reshape(-1)),
        as_ctypes(wake_ids.reshape(-1)),
        as_ctypes(wake_vertices.reshape(-1)),
        as_ctypes(Cij_x.reshape(-1)),
        as_ctypes(Cij_y.reshape(-1)),
        as_ctypes(Cij_z.reshape(-1)),
    )

    Cij_x = Cij_x.reshape((nte, nf))
    Cij_y = Cij_y.reshape((nte, nf))
    Cij_z = Cij_z.reshape((nte, nf))

    Cij[:, :, 0] = Cij_x[:, :]
    Cij[:, :, 1] = Cij_y[:, :]
    Cij[:, :, 2] = Cij_z[:, :]

    return