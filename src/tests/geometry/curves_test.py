import sys
sys.path.append('./src')

import pybird

import numpy as np
import matplotlib.pyplot as plt


if __name__ == '__main__':
    model = pybird.model('1')

    #---------------------------#
    model.geo.data.theta1e = 0
    model.geo.data.theta2e = 0
    model.geo.data.theta3e = 10

    model.geo.data.theta4e = 0
    model.geo.data.theta5e = 20

    model.geo.data.theta6e = 0
    model.geo.data.theta7e = 20

    #---------------------------#
    model.geo.data.theta1d = 0
    model.geo.data.theta2d = 0
    model.geo.data.theta3d = 10

    model.geo.data.theta4d = 0
    model.geo.data.theta5d = 20

    model.geo.data.theta6d = 0
    model.geo.data.theta7d = 20

    #---------------------------#
    model.geo.data.rootAirfoil = np.loadtxt('./data/foil.txt')
    model.geo.data.middleAirfoil = np.loadtxt('./data/foil.txt')
    model.geo.data.tipAirfoil = np.loadtxt('./data/foil.txt')

    #---------------------------#
    model.geo.wing_params.update()

    #---------------------------#
    model.geo.data.theta8 = 10
    model.geo.data.theta9 = 10

    #---------------------------#
    model.geo.tail_params.update()

    #---------------------------#
    p0e = model.geo.data.l0 * model.geo.data.y0
    p1e = p0e
    p2e = model.geo.data.l1 * model.geo.wing_params.y1e + p1e
    p3e = model.geo.data.l2 * model.geo.wing_params.yBase2e + p2e

    x1e = model.geo.wing_params.x1e
    y1e = model.geo.wing_params.y1e
    z1e = model.geo.wing_params.z1e

    xBase2e = model.geo.wing_params.xBase2e
    yBase2e = model.geo.wing_params.yBase2e
    zBase2e = model.geo.wing_params.zBase2e

    xTip2e = model.geo.wing_params.xTip2e
    yTip2e = model.geo.wing_params.yTip2e
    zTip2e = model.geo.wing_params.zTip2e

    x3e = model.geo.wing_params.x3e
    y3e = model.geo.wing_params.y3e
    z3e = model.geo.wing_params.z3e

    #---------------------------#
    # Figure
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    ax.quiver(p1e[0], p1e[1], p1e[2], x1e[0], x1e[1], x1e[2], length=0.1, color='k')
    ax.quiver(p1e[0], p1e[1], p1e[2], y1e[0], y1e[1], y1e[2], length=0.1, color='k')
    ax.quiver(p1e[0], p1e[1], p1e[2], z1e[0], z1e[1], z1e[2], length=0.1, color='k')

    ax.quiver(p2e[0], p2e[1], p2e[2], xBase2e[0], xBase2e[1], xBase2e[2], length=0.1, color='k')
    ax.quiver(p2e[0], p2e[1], p2e[2], yBase2e[0], yBase2e[1], yBase2e[2], length=0.1, color='k')
    ax.quiver(p2e[0], p2e[1], p2e[2], zBase2e[0], zBase2e[1], zBase2e[2], length=0.1, color='k')

    ax.quiver(p2e[0], p2e[1], p2e[2], xTip2e[0], xTip2e[1], xTip2e[2], length=0.1, color='k')
    ax.quiver(p2e[0], p2e[1], p2e[2], yTip2e[0], yTip2e[1], yTip2e[2], length=0.1, color='k')
    ax.quiver(p2e[0], p2e[1], p2e[2], zTip2e[0], zTip2e[1], zTip2e[2], length=0.1, color='k')

    ax.quiver(p3e[0], p3e[1], p3e[2], x3e[0], x3e[1], x3e[2], length=0.1, color='k')
    ax.quiver(p3e[0], p3e[1], p3e[2], y3e[0], y3e[1], y3e[2], length=0.1, color='k')
    ax.quiver(p3e[0], p3e[1], p3e[2], z3e[0], z3e[1], z3e[2], length=0.1, color='k')

    ax.plot(model.geo.wing_params.curve1e[:, 0], model.geo.wing_params.curve1e[:, 1], model.geo.wing_params.curve1e[:, 2], color='C0')
    ax.plot(model.geo.wing_params.curve2e[:, 0], model.geo.wing_params.curve2e[:, 1], model.geo.wing_params.curve2e[:, 2], color='C0')
    ax.plot(model.geo.wing_params.curve3e[:, 0], model.geo.wing_params.curve3e[:, 1], model.geo.wing_params.curve3e[:, 2], color='C0')
    ax.plot(model.geo.wing_params.curve4e[:, 0], model.geo.wing_params.curve4e[:, 1], model.geo.wing_params.curve4e[:, 2], color='C0')
    ax.plot(model.geo.wing_params.curve5e[:, 0], model.geo.wing_params.curve5e[:, 1], model.geo.wing_params.curve5e[:, 2], color='C0')
    ax.plot(model.geo.wing_params.curve6e[:, 0], model.geo.wing_params.curve6e[:, 1], model.geo.wing_params.curve6e[:, 2], color='C0')

    ax.plot(model.geo.wing_params.curve7e[:, 0], model.geo.wing_params.curve7e[:, 1], model.geo.wing_params.curve7e[:, 2], color='red')
    ax.plot(model.geo.wing_params.curve8e[:, 0], model.geo.wing_params.curve8e[:, 1], model.geo.wing_params.curve8e[:, 2], color='red')

    ax.plot(model.geo.wing_params.curve9e[:, 0], model.geo.wing_params.curve9e[:, 1], model.geo.wing_params.curve9e[:, 2], color='red')
    ax.plot(model.geo.wing_params.curve10e[:, 0], model.geo.wing_params.curve10e[:, 1], model.geo.wing_params.curve10e[:, 2], color='red')

    ax.plot(model.geo.wing_params.curve11e[:, 0], model.geo.wing_params.curve11e[:, 1], model.geo.wing_params.curve11e[:, 2], color='red')
    ax.plot(model.geo.wing_params.curve12e[:, 0], model.geo.wing_params.curve12e[:, 1], model.geo.wing_params.curve12e[:, 2], color='red')

    ax.plot(model.geo.wing_params.curve13e[:, 0], model.geo.wing_params.curve13e[:, 1], model.geo.wing_params.curve13e[:, 2], color='red')
    ax.plot(model.geo.wing_params.curve14e[:, 0], model.geo.wing_params.curve14e[:, 1], model.geo.wing_params.curve14e[:, 2], color='red')

    #-----------------------------------#
    ax.plot(model.geo.wing_params.curve1d[:, 0], model.geo.wing_params.curve1d[:, 1], model.geo.wing_params.curve1d[:, 2], color='C0')
    ax.plot(model.geo.wing_params.curve2d[:, 0], model.geo.wing_params.curve2d[:, 1], model.geo.wing_params.curve2d[:, 2], color='C0')
    ax.plot(model.geo.wing_params.curve3d[:, 0], model.geo.wing_params.curve3d[:, 1], model.geo.wing_params.curve3d[:, 2], color='C0')
    ax.plot(model.geo.wing_params.curve4d[:, 0], model.geo.wing_params.curve4d[:, 1], model.geo.wing_params.curve4d[:, 2], color='C0')
    ax.plot(model.geo.wing_params.curve5d[:, 0], model.geo.wing_params.curve5d[:, 1], model.geo.wing_params.curve5d[:, 2], color='C0')
    ax.plot(model.geo.wing_params.curve6d[:, 0], model.geo.wing_params.curve6d[:, 1], model.geo.wing_params.curve6d[:, 2], color='C0')

    ax.plot(model.geo.wing_params.curve7d[:, 0], model.geo.wing_params.curve7d[:, 1], model.geo.wing_params.curve7d[:, 2], color='red')
    ax.plot(model.geo.wing_params.curve8d[:, 0], model.geo.wing_params.curve8d[:, 1], model.geo.wing_params.curve8d[:, 2], color='red')

    ax.plot(model.geo.wing_params.curve9d[:, 0], model.geo.wing_params.curve9d[:, 1], model.geo.wing_params.curve9d[:, 2], color='red')
    ax.plot(model.geo.wing_params.curve10d[:, 0], model.geo.wing_params.curve10d[:, 1], model.geo.wing_params.curve10d[:, 2], color='red')

    ax.plot(model.geo.wing_params.curve11d[:, 0], model.geo.wing_params.curve11d[:, 1], model.geo.wing_params.curve11d[:, 2], color='red')
    ax.plot(model.geo.wing_params.curve12d[:, 0], model.geo.wing_params.curve12d[:, 1], model.geo.wing_params.curve12d[:, 2], color='red')

    ax.plot(model.geo.wing_params.curve13d[:, 0], model.geo.wing_params.curve13d[:, 1], model.geo.wing_params.curve13d[:, 2], color='red')
    ax.plot(model.geo.wing_params.curve14d[:, 0], model.geo.wing_params.curve14d[:, 1], model.geo.wing_params.curve14d[:, 2], color='red')

    #-----------------------------------#
    ax.plot(model.geo.body_params.curve15e[:, 0], model.geo.body_params.curve15e[:, 1], model.geo.body_params.curve15e[:, 2], color='green')
    ax.plot(model.geo.body_params.curve15d[:, 0], model.geo.body_params.curve15d[:, 1], model.geo.body_params.curve15d[:, 2], color='green')
    ax.plot(model.geo.body_params.curve16e[:, 0], model.geo.body_params.curve16e[:, 1], model.geo.body_params.curve16e[:, 2], color='green')
    ax.plot(model.geo.body_params.curve16d[:, 0], model.geo.body_params.curve16d[:, 1], model.geo.body_params.curve16d[:, 2], color='green')
    ax.plot(model.geo.body_params.curve17[:, 0], model.geo.body_params.curve17[:, 1], model.geo.body_params.curve17[:, 2], color='green')
    ax.plot(model.geo.body_params.curve18[:, 0], model.geo.body_params.curve18[:, 1], model.geo.body_params.curve18[:, 2], color='green')
    ax.plot(model.geo.body_params.curve19[:, 0], model.geo.body_params.curve19[:, 1], model.geo.body_params.curve19[:, 2], color='green')
    ax.plot(model.geo.body_params.curve20[:, 0], model.geo.body_params.curve20[:, 1], model.geo.body_params.curve20[:, 2], color='green')
    ax.plot(model.geo.body_params.curve21[:, 0], model.geo.body_params.curve21[:, 1], model.geo.body_params.curve21[:, 2], color='green')
    ax.plot(model.geo.body_params.curve22[:, 0], model.geo.body_params.curve22[:, 1], model.geo.body_params.curve22[:, 2], color='green')
    ax.plot(model.geo.body_params.curve23e[:, 0], model.geo.body_params.curve23e[:, 1], model.geo.body_params.curve23e[:, 2], color='green')
    ax.plot(model.geo.body_params.curve24e[:, 0], model.geo.body_params.curve24e[:, 1], model.geo.body_params.curve24e[:, 2], color='green')
    ax.plot(model.geo.body_params.curve25e[:, 0], model.geo.body_params.curve25e[:, 1], model.geo.body_params.curve25e[:, 2], color='green')
    ax.plot(model.geo.body_params.curve26e[:, 0], model.geo.body_params.curve26e[:, 1], model.geo.body_params.curve26e[:, 2], color='green')
    ax.plot(model.geo.body_params.curve23d[:, 0], model.geo.body_params.curve23d[:, 1], model.geo.body_params.curve23d[:, 2], color='green')
    ax.plot(model.geo.body_params.curve24d[:, 0], model.geo.body_params.curve24d[:, 1], model.geo.body_params.curve24d[:, 2], color='green')
    ax.plot(model.geo.body_params.curve25d[:, 0], model.geo.body_params.curve25d[:, 1], model.geo.body_params.curve25d[:, 2], color='green')
    ax.plot(model.geo.body_params.curve26d[:, 0], model.geo.body_params.curve26d[:, 1], model.geo.body_params.curve26d[:, 2], color='green')
    ax.plot(model.geo.body_params.curve27[:, 0], model.geo.body_params.curve27[:, 1], model.geo.body_params.curve27[:, 2], color='green')
    ax.plot(model.geo.body_params.curve28[:, 0], model.geo.body_params.curve28[:, 1], model.geo.body_params.curve28[:, 2], color='green')
    ax.plot(model.geo.body_params.curve29[:, 0], model.geo.body_params.curve29[:, 1], model.geo.body_params.curve29[:, 2], color='green')
    ax.plot(model.geo.body_params.curve30[:, 0], model.geo.body_params.curve30[:, 1], model.geo.body_params.curve30[:, 2], color='green')
    ax.plot(model.geo.body_params.curve31[:, 0], model.geo.body_params.curve31[:, 1], model.geo.body_params.curve31[:, 2], color='green')
    ax.plot(model.geo.body_params.curve32[:, 0], model.geo.body_params.curve32[:, 1], model.geo.body_params.curve32[:, 2], color='green')
    ax.plot(model.geo.body_params.curve33[:, 0], model.geo.body_params.curve33[:, 1], model.geo.body_params.curve33[:, 2], color='green')
    ax.plot(model.geo.body_params.curve34[:, 0], model.geo.body_params.curve34[:, 1], model.geo.body_params.curve34[:, 2], color='green')

    ax.plot(model.geo.tail_params.curve35e[:, 0], model.geo.tail_params.curve35e[:, 1], model.geo.tail_params.curve35e[:, 2], color='orange')
    ax.plot(model.geo.tail_params.curve35d[:, 0], model.geo.tail_params.curve35d[:, 1], model.geo.tail_params.curve35d[:, 2], color='orange')
    ax.plot(model.geo.tail_params.curve36e[:, 0], model.geo.tail_params.curve36e[:, 1], model.geo.tail_params.curve36e[:, 2], color='orange')
    ax.plot(model.geo.tail_params.curve36d[:, 0], model.geo.tail_params.curve36d[:, 1], model.geo.tail_params.curve36d[:, 2], color='orange')
    ax.plot(model.geo.tail_params.curve37[:, 0], model.geo.tail_params.curve37[:, 1], model.geo.tail_params.curve37[:, 2], color='orange')
    ax.plot(model.geo.tail_params.curve38[:, 0], model.geo.tail_params.curve38[:, 1], model.geo.tail_params.curve38[:, 2], color='orange')
    
    ax.plot(model.geo.head_params.curve39e[:, 0], model.geo.head_params.curve39e[:, 1], model.geo.head_params.curve39e[:, 2], color='orange')
    ax.plot(model.geo.head_params.curve39d[:, 0], model.geo.head_params.curve39d[:, 1], model.geo.head_params.curve39d[:, 2], color='orange')
    ax.plot(model.geo.head_params.curve40d[:, 0], model.geo.head_params.curve40d[:, 1], model.geo.head_params.curve40d[:, 2], color='orange')
    ax.plot(model.geo.head_params.curve40e[:, 0], model.geo.head_params.curve40e[:, 1], model.geo.head_params.curve40e[:, 2], color='orange')
    ax.plot(model.geo.head_params.curve41[:, 0], model.geo.head_params.curve41[:, 1], model.geo.head_params.curve41[:, 2], color='orange')
    ax.plot(model.geo.head_params.curve42[:, 0], model.geo.head_params.curve42[:, 1], model.geo.head_params.curve42[:, 2], color='orange')
    ax.plot(model.geo.head_params.curve43[:, 0], model.geo.head_params.curve43[:, 1], model.geo.head_params.curve43[:, 2], color='orange')
    ax.plot(model.geo.head_params.curve44[:, 0], model.geo.head_params.curve44[:, 1], model.geo.head_params.curve44[:, 2], color='orange')
    ax.plot(model.geo.head_params.curve45[:, 0], model.geo.head_params.curve45[:, 1], model.geo.head_params.curve45[:, 2], color='orange')
    ax.plot(model.geo.head_params.curve46[:, 0], model.geo.head_params.curve46[:, 1], model.geo.head_params.curve46[:, 2], color='orange')
    ax.plot(model.geo.head_params.curve47[:, 0], model.geo.head_params.curve47[:, 1], model.geo.head_params.curve47[:, 2], color='orange')
    ax.plot(model.geo.head_params.curve48[:, 0], model.geo.head_params.curve48[:, 1], model.geo.head_params.curve48[:, 2], color='orange')

    #-----------------------------------#
    ax.set_xlim((-1., 1.))
    ax.set_ylim((-1., 1.))
    ax.set_zlim((-1., 1.))

    plt.show()