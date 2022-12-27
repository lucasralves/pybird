import numpy as np
import matplotlib.pyplot as plt

v1 = np.array([-1.47e-02, -5.82e-03, 0.00e+00])
v2 = np.array([-6.59e-03, -1.38e-02, 0.00e+00])
v3 = np.array([1.51e-02, 7.98e-03, 0.00e+00])
v4 = np.array([6.18e-03, 1.16e-02, 0.00e+00])

p1 = np.array([-1.20e-17, -1.23e-17, 1.00e-08])
p2 = np.array([3.58e-02, 3.29e-02, 7.29e-04])
p3 = np.array([5.44e-02, 2.95e-02, 7.98e-04])

ax = plt.figure().add_subplot(projection='3d')

ax.scatter(v1[0], v1[1], v1[2], color='k')
ax.scatter(v2[0], v2[1], v2[2], color='k')
ax.scatter(v3[0], v3[1], v3[2], color='k')
ax.scatter(v4[0], v4[1], v4[2], color='k')

ax.scatter(p1[0], p1[1], p1[2], color='r')
ax.scatter(p2[0], p2[1], p2[2], color='g')
ax.scatter(p3[0], p3[1], p3[2], color='b')

ax.scatter(0.05, 0.0, 0.0, color='w')
ax.scatter(-0.05, 0.0, 0.0, color='w')
ax.scatter(0.0, 0.05, 0.0, color='w')
ax.scatter(0.0, -0.05, 0.0, color='w')
ax.scatter(0.0, 0.0, 0.05, color='w')
ax.scatter(0.0, 0.0, -0.05, color='w')

plt.show()