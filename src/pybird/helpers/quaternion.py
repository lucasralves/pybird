from math import sin, cos, pi
from numpy import array

from pybird.helpers.type import Quaternion, Vector
from pybird.helpers import vector


def fromAxisAngle(axis: Vector, angle: float) -> Quaternion:
    a = 0.5 * angle * pi / 180
    s, c = sin(a), cos(a)
    return array([s * axis[0], s * axis[1], s * axis[2], c])

def multiply(a: Quaternion, b: Quaternion) -> Quaternion:
    s1, v1 = a[3], a[:3]
    s2, v2 = b[3], b[:3]

    s = s1 * s2 - vector.dot(v1, v2)
    v = s1 * v2 + s2 * v1 + vector.cross(v1, v2)

    return array([v[0], v[1], v[2], s])

def conjugate(a: Quaternion) -> Quaternion:
    return array([-a[0], -a[1], -a[2], a[3]])

def rotate(q: Quaternion, v: Vector) -> Vector:
    q_conj = conjugate(q)
    p = array([v[0], v[1], v[2], 0])
    return multiply(multiply(q, p), q_conj)[:3]