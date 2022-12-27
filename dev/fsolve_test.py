from scipy.optimize import fsolve
import numpy as np


# def f(x):
#     return np.array([
#         x[0] + x[1] + x[2] - 3,
#         x[0] * x[0] + x[1] * x[1] + x[2] * x[2] - 5,
#         np.exp(x[0]) + x[0] * x[1] - x[0] * x[2] - 1,
#     ])

# def jac(x):
#     return np.array([
#         [1, 1, 1],
#         [2 * x[0], 2 * x[1], 2 * x[2]],
#         [np.exp(x[0]) + x[1] - x[2], x[0], -x[0]],
#     ])

# sol = fsolve(f, np.random.random(3), fprime=jac)

a = np.empty(3, dtype=np.double)
a[:] = 1

print(a)

# print(sol)
# print(f(sol))