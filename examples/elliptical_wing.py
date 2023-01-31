import sys
sys.path.append('./src')

import pybird


if __name__ == '__main__':
    pybird.init()
    pybird.load('./examples/data/data.case')

    pybird.model.name = 'elliptical wing'
    pybird.model.description = 'example'

    # wing
    pybird.model.geo.wing.thetaRootZ = 1.0

    pybird.model.geo.wing.l0 = 0.025
    pybird.model.geo.wing.l1 = 0.05
    pybird.model.geo.wing.l2 = 0.05
    pybird.model.geo.wing.l3 = 0.08

    # pybird.model.geo.wing.theta3_d = 10.
    # pybird.model.geo.wing.theta4_d = 20.
    # pybird.model.geo.wing.theta7_d = 20.

    pybird.model.geo.wing.h1 = 0.0
    pybird.model.geo.wing.h4 = 0.015
    pybird.model.geo.wing.delta4 = 0.2
    pybird.model.geo.wing.delta5 = 0.7
    pybird.model.geo.wing.h6 = 0.12

    # body
    pybird.model.geo.body.h12 = 0.018

    # tail
    pybird.model.geo.tail.h20 = 0.06
    pybird.model.geo.tail.h22 = 0.08

    # save
    pybird.save('./examples/data/elliptical_wing.case')

    # mesh
    ref = pybird.refinement.model(
        wing=pybird.refinement.wing(),
        body=pybird.refinement.body(),
        head=pybird.refinement.head(),
        tail=pybird.refinement.tail(),
    )

    pybird.build(ref, view=False)

    pybird.gen_vtk('./examples/elliptical_wing')
