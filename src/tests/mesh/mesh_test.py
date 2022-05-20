import sys
sys.path.append('./src')

import pybird
from pybird.helpers import vector

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import transforms


if __name__ == '__main__':
    model = pybird.model('1')

    #--------------------------------#
    model.geo.data.theta1e = 25
    model.geo.data.theta2e = 0
    model.geo.data.theta3e = 10

    model.geo.data.theta4e = 20
    model.geo.data.theta5e = 20

    model.geo.data.theta6e = 40
    model.geo.data.theta7e = 20

    #--------------------------------#
    model.geo.data.theta1d = 20
    model.geo.data.theta2d = 0
    model.geo.data.theta3d = 10

    model.geo.data.theta4d = 0
    model.geo.data.theta5d = 20

    model.geo.data.theta6d = 40
    model.geo.data.theta7d = 20

    #--------------------------------#
    model.geo.data.rootAirfoil = np.loadtxt('./data/foil.txt')
    model.geo.data.middleAirfoil = np.loadtxt('./data/foil.txt')
    model.geo.data.tipAirfoil = np.loadtxt('./data/foil.txt')

    #--------------------------------#
    model.geo.wing_params.update()

    #---------------------------#
    model.geo.data.theta8 = 10
    model.geo.data.theta9 = 10
    model.geo.data.theta10 = 10

    #---------------------------#
    model.geo.tail_params.update()

    # Mesh
    model.mesh.build(0.02, 0.5)