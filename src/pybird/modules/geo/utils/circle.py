from math import acos
from numpy import cross, deg2rad, dot, linspace, zeros, ndarray
from scipy.optimize import minimize
from scipy.spatial.transform import Rotation as R

from pybird.modules.geo.utils import vector

def find_center(v1: ndarray, v2: ndarray, v3: ndarray) -> ndarray:

    def func(x, *args):
        v1, v2, v3 = args

        n1 = ((v1[0] - x[0]) ** 2 + (v1[1] - x[1]) ** 2 + (v1[2] - x[2]) ** 2) ** 0.5
        n2 = ((v2[0] - x[0]) ** 2 + (v2[1] - x[1]) ** 2 + (v2[2] - x[2]) ** 2) ** 0.5
        n3 = ((v3[0] - x[0]) ** 2 + (v3[1] - x[1]) ** 2 + (v3[2] - x[2]) ** 2) ** 0.5

        return (n1 - n2) ** 2 + (n1 - n3) ** 2 + (n2 - n3) ** 2
    
    x0 = (v1 + v2 + v3) / 3
    sol = minimize(func, (x0[0], x0[1], x0[2]), args=(v1, v2, v3))

    return sol.x

def circle_arc(center: ndarray, v1: ndarray, v2: ndarray, n: int, removeEdges: bool = True) -> ndarray:

    c1 = v1 - center
    c2 = v2 - center
    radius = vector.norm(c1)
    normal = vector.unary(cross(c1, c2))

    angle = acos(dot(c1 / radius, c2 / radius))

    angles = linspace(0, angle, num=n)

    curve = zeros((n, 3))

    for i in range(n):
        rot = R.from_rotvec(angles[i] * normal)
        curve[i, :] = center + rot.apply(c1)
            
    if removeEdges:
        return curve[1:n - 1]
    else:
        return curve