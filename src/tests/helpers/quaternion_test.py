import sys
sys.path.append('./src')

import numpy as np

from pybird.helpers import quaternion
from pybird.helpers import type

if __name__ == '__main__':
    v = np.array([1, 0, 0])

    axis = np.array([0, 1, 0])
    angle = 90

    q = quaternion.fromAxisAngle(axis, angle)
    q_conj = quaternion.conjugate(q)

    print(q)
    print(q_conj)

    print(quaternion.multiply(q, q_conj))

    print(quaternion.rotate(q, v))