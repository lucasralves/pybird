import ctypes
from typing import List
import numpy as np

from py.models import FaceModel

def solve(vertices: np.ndarray,
          faces: List[FaceModel],
          trailing_edge: np.ndarray,
          freestream: float,
          alpha: float,
          beta: float,
          delta_t: float,
          wake_length: float):

    # Input
    n_v = vertices.shape[0]

    n_te = trailing_edge.shape[0]
    n_w = int(wake_length / (freestream * delta_t))

    n_f4, n_f3 = 0, 0
    faces3, faces4 = [], []

    for face in faces:
        if face.n == 4:
            n_f4 += 1
            faces4.append(face.vertices)
        else:
            n_f3 += 1
            faces3.append(face.vertices)

    faces3 = np.asarray(faces3)
    faces4 = np.asarray(faces4)

    vertices = vertices.reshape(vertices.size).astype(np.double)
    faces4 = faces4.reshape(faces4.size).astype(np.int32)
    faces3 = faces3.reshape(faces3.size).astype(np.int32)
    trailing_edge = trailing_edge.reshape(trailing_edge.size).astype(np.int32)
    wake_points = np.empty(6 * n_w * n_te, dtype=np.double)

    # Output
    source = np.empty(n_v, dtype=np.double)
    doublet = np.empty(n_v, dtype=np.double)
    vel_x = np.empty(n_v, dtype=np.double)
    vel_y = np.empty(n_v, dtype=np.double)
    vel_z = np.empty(n_v, dtype=np.double)
    cp = np.empty(n_v, dtype=np.double)
    transpiration = np.empty(n_v, dtype=np.double)

    # Library
    lib = ctypes.CDLL('./bin/libsolver.so')

    lib.main.argtypes = [
        ctypes.c_int,                       # n_v
        ctypes.c_int,                       # n_f3
        ctypes.c_int,                       # n_f4
        ctypes.c_int,                       # n_te
        ctypes.c_int,                       # n_w
        ctypes.c_double,                    # delta_t
        ctypes.POINTER(ctypes.c_double),    # vertices
        ctypes.POINTER(ctypes.c_int),       # faces3
        ctypes.POINTER(ctypes.c_int),       # faces4
        ctypes.POINTER(ctypes.c_int),       # trailing edge
        ctypes.POINTER(ctypes.c_double),    # trailing edge points
        ctypes.c_double,                    # freestream
        ctypes.c_double,                    # alpha
        ctypes.c_double,                    # beta
        ctypes.POINTER(ctypes.c_double),    # source
        ctypes.POINTER(ctypes.c_double),    # doublet
        ctypes.POINTER(ctypes.c_double),    # vel_x
        ctypes.POINTER(ctypes.c_double),    # vel_y
        ctypes.POINTER(ctypes.c_double),    # vel_z
        ctypes.POINTER(ctypes.c_double),    # cp
        ctypes.POINTER(ctypes.c_double),    # transpiration
    ]

    lib.main.restype = None

    lib.main(
        n_v,
        n_f3,
        n_f4,
        n_te,
        n_w,
        delta_t,
        np.ctypeslib.as_ctypes(vertices),
        np.ctypeslib.as_ctypes(faces3),
        np.ctypeslib.as_ctypes(faces4),
        np.ctypeslib.as_ctypes(trailing_edge),
        np.ctypeslib.as_ctypes(wake_points),
        float(freestream),
        float(alpha),
        float(beta),
        np.ctypeslib.as_ctypes(source),
        np.ctypeslib.as_ctypes(doublet),
        np.ctypeslib.as_ctypes(vel_x),
        np.ctypeslib.as_ctypes(vel_y),
        np.ctypeslib.as_ctypes(vel_z),
        np.ctypeslib.as_ctypes(cp),
        np.ctypeslib.as_ctypes(transpiration)
    )

    # Reshape wake
    wake = np.empty((n_te, n_w, 2, 3), dtype=np.double)

    for i in range(n_te):

        index1 = i * 6 * n_w
        index2 = i * 6 * n_w + n_w
        index3 = i * 6 * n_w + 2 * n_w

        wake[i, :, 0, 0] = wake_points[index1:index1 + n_w]
        wake[i, :, 0, 1] = wake_points[index2:index2 + n_w]
        wake[i, :, 0, 2] = wake_points[index3:index3 + n_w]

        index1 = i * 6 * n_w + 3 * n_w
        index2 = i * 6 * n_w + 3 * n_w + n_w
        index3 = i * 6 * n_w + 3 * n_w + 2 * n_w

        wake[i, :, 1, 0] = wake_points[index1:index1 + n_w]
        wake[i, :, 1, 1] = wake_points[index2:index2 + n_w]
        wake[i, :, 1, 2] = wake_points[index3:index3 + n_w]
    
    # import matplotlib.pyplot as plt

    # ax = plt.figure().add_subplot(projection='3d')

    # for i in range(2):
    #     for j in range(n_w):
    #         if i == 0:
    #             color = 'k'
    #             alpha = 0.5
    #         elif i == 1:
    #             color = 'r'
    #             alpha = 0.5
    #         else:
    #             color = 'g'
    #             alpha = 0.5
    #         ax.scatter(wake[i, j, 0, 0], wake[i, j, 0, 1], wake[i, j, 0, 2], color=color, alpha=alpha)
    #         ax.scatter(wake[i, j, 1, 0], wake[i, j, 1, 1], wake[i, j, 1, 2], color=color, alpha=alpha)
    
    # plt.show()

    return [
        source,
        doublet,
        vel_x,
        vel_y,
        vel_z,
        cp,
        transpiration,
        wake,
    ]
