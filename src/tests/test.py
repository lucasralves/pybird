import sys
sys.path.append('./src')

from pybird.helpers import curve
from pybird.helpers import vector

from typing import List
import numpy as np
import matplotlib.pyplot as plt



if __name__ == '__main__':

    v1 = np.array([1, 0, 0])
    v2 = vector.unary(np.array([1, 1, 1]))
    v3 = np.array([0, 0, 0])

    curve1 = curve.circle([v1, vector.unary(v2), v3], 100)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.plot(curve1[:, 0], curve1[:, 1], curve1[:, 2])
    ax.quiver(v3[0], v3[1], v3[2], v1[0], v1[1], v1[2])
    ax.quiver(v3[0], v3[1], v3[2], v2[0], v2[1], v2[2])

    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    ax.set_zlim([0, 1])
    plt.show()