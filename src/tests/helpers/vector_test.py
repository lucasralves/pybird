import sys
sys.path.append('./src')

import numpy as np

from pybird.helpers import vector
from pybird.helpers import type

if __name__ == '__main__':

    e1 = np.array([1, 0, 0])
    e2 = np.array([0, 1, 0])
    e3 = np.array([0, 0, 1])

    v = 1 * e1 + 2 * e2 + 3 * e3

    print([v, vector.unary(v)])
    
    print(vector.dot(v, e1))
    print(vector.dot(v, e2))
    print(vector.dot(v, e3))

    print(vector.cross(e1, e2))
    print(vector.cross(e2, e3))
    print(vector.cross(e2, -e2))
    print(vector.cross(e2, e2))