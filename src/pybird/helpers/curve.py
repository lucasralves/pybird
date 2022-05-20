from math import acos, cos, sin
from typing import List
from numpy import linspace, zeros
from numpy import cos as nuncos
from numpy import sin as nunsin

from pybird.helpers.type import Curve, Vector
from pybird.helpers import vector

def bezier(points: List[Vector], n: int) -> Curve:

    size = len(points)    
    t = linspace(0, 1, num=n)
    curve = zeros((n, 3))

    if size == 3:
        for i in range(n):
            curve[i, :] = (1 - t[i]) * (1 - t[i]) * points[0] + 2 * (1 - t[i]) * t[i] * points[1] + t[i] * t[i] * points[2]
    elif size == 4:
        for i in range(n):
            curve[i, :] = (1 - t[i]) * (1 - t[i]) * (1 - t[i]) * points[0] + 3 * (1 - t[i]) * (1 - t[i]) * t[i] * points[1] + 3 * (1 - t[i]) * t[i] * t[i] * points[2] + t[i] * t[i] * t[i] * points[3]

    return curve

def line(points: List[Vector], n: int) -> Curve:
       
    t = linspace(0, 1, num=n)
    curve = zeros((n, 3))

    if len(points) == 2:
        for i in range(n):
            curve[i, :] = (1 - t[i]) * points[0] + t[i] * points[1]
    
    return curve

def oneQuarterCurve(points: List[Vector], n: int) -> Curve:

    r1 = points[0] - points[2]
    r2 = points[1] - points[2]

    e1 = r1 / vector.norm(r1)
    e2 = vector.cross(e1, vector.cross(r2 / vector.norm(r2), e1))

    angle_max = acos(vector.dot(r1, r2) / (vector.norm(r1) * vector.norm(r2)))
    angles = linspace(0, angle_max, num=n)

    a = vector.norm(r1)
    b = vector.norm(r2 - r1 * cos(angle_max)) / sin(angle_max)

    out = zeros((n, 3))

    for i in range(n):
        out[i, :] = a * e1 * cos(angles[i]) + b * e2 * sin(angles[i]) + points[2]

    return out

def circle(points: List[Vector], n: int) -> Curve:

    r1 = points[0] - points[2]
    r2 = points[1] - points[2]
    r = vector.norm(r1)

    e1 = vector.unary(r1)
    e2 = vector.unary(vector.cross(e1, vector.cross(r2 / vector.norm(r2), e1)))

    angle_max = acos(vector.dot(r1, r2) / (vector.norm(r1) * vector.norm(r2)))
    angles = linspace(0, angle_max, num=n)

    c = r * nuncos(angles)
    s = r * nunsin(angles)

    out = zeros((n, 3))

    for i in range(n):
        out[i, :] = c[i] * e1 + s[i] * e2 + points[2]

    return out