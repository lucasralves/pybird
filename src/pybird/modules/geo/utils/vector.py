from math import acos, fabs, pi
from typing import List
from numpy import cross, deg2rad, dot, zeros, ndarray
from numpy.linalg import norm
from scipy.spatial.transform import Rotation as R

def unary(a: ndarray) -> ndarray:
    """Returns a unary vector"""
    lenght = norm(a)
    if -1e-8 < lenght < 1e-8:
        return zeros(len(a))
    
    return a / lenght

def angle(a: ndarray, b: ndarray) -> List:
    """Returns the angle between two Points and the vector responsible to rotate a to b"""
    a = unary(a)
    b = unary(b)
    val = dot(a, b)
    if val > 1: val = 1
    if val < -1: val = -1
    theta = acos(val) * 180 / pi
    axis = unary(cross(a, b))
    return [theta, axis]

def rot(a: ndarray, theta: float, axis: ndarray) -> ndarray:
    r = R.from_rotvec(deg2rad(theta) * axis)
    return r.apply(a)