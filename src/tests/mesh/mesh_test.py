import sys
sys.path.append('./src')

import pybird

import numpy as np
import matplotlib.pyplot as plt


if __name__ == '__main__':
    model = pybird.model('1')

    #--------------------------------#
    model.geo.data.theta1e = 10
    model.geo.data.theta2e = 0
    model.geo.data.theta3e = 0

    model.geo.data.theta4e = 0
    model.geo.data.theta5e = 0

    model.geo.data.theta6e = 30
    model.geo.data.theta7e = 0

    #--------------------------------#
    model.geo.data.theta1d = 10
    model.geo.data.theta2d = 0
    model.geo.data.theta3d = 0

    model.geo.data.theta4d = 0
    model.geo.data.theta5d = 0

    model.geo.data.theta6d = 30
    model.geo.data.theta7d = 0

    #--------------------------------#
    model.geo.data.rootAirfoil = np.loadtxt('./data/foil.txt')
    model.geo.data.middleAirfoil = np.loadtxt('./data/foil.txt')
    model.geo.data.tipAirfoil = np.loadtxt('./data/foil.txt')
    model.geo.data.tailAirfoil = np.loadtxt('./data/foil.txt')

    #--------------------------------#
    model.geo.wing_params.update()
    model.geo.tail_params.update()

    #---------------------------#
    model.geo.data.theta8 = 0
    model.geo.data.theta9 = 0
    model.geo.data.theta10 = 0

    #---------------------------#
    model.geo.tail_params.update()

    #---------------------------#
    # Mesh
    model.mesh.build(0.05, 0.5)

    #---------------------------#
    # View
    model.view.mesh()