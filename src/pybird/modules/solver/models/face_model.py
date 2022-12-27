import ctypes
from numpy import ndarray

class Vec3D(ctypes.Structure):
    _fields_=[
        ("x", ctypes.c_double),
        ("y", ctypes.c_double),
        ("z", ctypes.c_double)
    ]

class Vec2D(ctypes.Structure):
    _fields_=[
        ("x", ctypes.c_double),
        ("y", ctypes.c_double)
    ]

class FaceModel(ctypes.Structure):
    _fields_=[
        ("n", ctypes.c_int),
        ("v1", ctypes.c_int),
        ("v2", ctypes.c_int),
        ("v3", ctypes.c_int),
        ("v4", ctypes.c_int),
        ("p_avg", Vec3D),
        ("p_ctrl", Vec3D),
        ("e1", Vec3D),
        ("e2", Vec3D),
        ("e3", Vec3D),
        ("p1", Vec2D),
        ("p2", Vec2D),
        ("p3", Vec2D),
        ("p4", Vec2D),
        ("area", ctypes.c_double),
        ("max_distance", ctypes.c_double),
    ]

def numpy2Vec3D(a: ndarray) -> Vec3D:
    return Vec3D(a[0], a[1], a[2])

def numpy2Vec2D(a: ndarray) -> Vec2D:
    return Vec2D(a[0], a[1])