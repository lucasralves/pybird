import numpy as np
from scipy.integrate import simpson
import matplotlib.pyplot as plt

# plt.rcParams['text.usetex'] = True

ZERO_ERROR = 1e-8

def vel_wing_2():

    def func(x0, y0, b, tau0):
        y = np.linspace(-b / 2, b / 2, num=200)
        func_1 = (tau0 / (4 * np.pi * (x0 + ZERO_ERROR))) * np.sqrt(1 - np.power(2 * y / b, 2)) / np.power(1 + np.power((y - y0) / (x0 + ZERO_ERROR), 2), 3 / 2)
        out = simpson(func_1, y)
        return out
    
    b = 2
    
    x0 = np.linspace(0.75 * 0.3, 20, num=100)

    v1 = np.zeros_like(x0)
    v2 = np.zeros_like(x0)
    v3 = np.zeros_like(x0)

    for i in range(len(x0)):
        v1[i] = func(x0[i], .0, b, 0.1)
        v2[i] = func(x0[i], .0, b, 0.5)
        v3[i] = func(x0[i], .0, b, 1.)
    
    eps = 0.3
    v4 = eps / (eps + x0)
    
    plt.figure()
    plt.plot(x0, v1, label=r'\Gamma_{0} = 0.1')
    plt.plot(x0, v2, label=r'\Gamma_{0} = 0.5')
    plt.plot(x0, v3, label=r'\Gamma_{0} = 1.0')
    plt.plot(x0, v4, label=r'v4')
    plt.legend()
    plt.grid()
    plt.show()

def vel_wing():

    def func(x0, y0, b, tau0):
        y = np.linspace(-b / 2, b / 2, num=200)
        func_1 = (tau0 / (4 * np.pi * (x0 + ZERO_ERROR))) * np.sqrt(1 - np.power(2 * y / b, 2)) / np.power(1 + np.power((y - y0) / (x0 + ZERO_ERROR), 2), 3 / 2)
        out = simpson(func_1, y)
        return out
    
    tau0 = 1
    b = 2
    
    y0 = np.linspace(-b / 2, b / 2, num=20)
    x0 = np.linspace(0.1, 10, num=100)

    X0, Y0 = np.meshgrid(x0, y0)

    v = np.zeros_like(X0)

    for i in range(len(x0)):
        for j in range(len(y0)):
            v[j, i] = func(X0[j, i], Y0[j, i], b, tau0)
    
    plt.figure()
    plt.imshow(v, extent=(x0[0], x0[len(x0) - 1], y0[0], y0[len(y0) - 1]), interpolation='quadric')
    plt.colorbar()
    plt.axis('equal')
    # plt.show()
    


def vel_wake():

    tau0 = 1
    b = 2

    xn, yn = 20, 30

    x = np.linspace(0, 10, num=xn)
    y = np.linspace(-b/2, b/2, num=yn)

    x0 = 0.5 * (x[1:] + x[:-1])
    y0 = 0.5 * (y[1:] + y[:-1])

    vel = np.zeros((yn - 1, xn - 1))

    # Loop pelos pontos
    for i in range(yn - 1):
        y0_val = y0[i]
        for j in range(xn - 1):

            # Loop para integrar
            int_y = 0.5 * (np.linspace(-b/2, b/2, num=100)[1:] + np.linspace(-b/2, b/2, num=100)[:-1])
            int_x = 0.5 * (np.linspace(0, x0[j], num=int(x0[j] / 1e-2) + 1)[1:] + np.linspace(0, x0[j], num=int(x0[j] / 1e-2) + 1)[:-1])
            dl, dy = int_x[1] - int_x[0], int_y[1] - int_y[0]
            fy = 0
            for k in range(len(int_y)):
                fx = 0
                for l in range(len(int_x)):
                    fx = fx + dl * (y0_val - int_y[k]) / (( (y0_val - int_y[k]) ** 2 + int_x[l] ** 2 ) ** (1.5))
                fy = fy + dy * fx * (y0_val - int_y[k]) / ((1 - 4 * int_y[k] * int_y[k] / (b * b)) ** 0.5)
            fy = (tau0 / (np.pi * b * b)) * fy
        
            vel[i, j] = fy + tau0 / (2 * b)
    
    X0, Y0 = np.meshgrid(x0, y0)

    plt.figure()
    plt.imshow(vel, extent=(x0[0], x0[len(x0) - 1], y0[0], y0[len(y0) - 1]), interpolation='quadric')
    plt.colorbar()
    plt.axis('equal')
    # plt.show()

    return


if __name__ == '__main__':

    # vel_wake()
    vel_wing_2()
    # plt.show()