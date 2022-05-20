from numpy import array
from pybird.helpers.type import Vector


def norm(a: Vector) -> float:
    return (a[0] * a[0] + a[1] * a[1] + a[2] * a[2]) ** 0.5

def unary(a: Vector) -> Vector:
    return a / norm(a)

def dot(a: Vector, b: Vector) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

def cross(a: Vector, b: Vector) -> float:
    return array([
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0]
    ])