import sys
sys.path.append('./src')

import pybird


if __name__ == '__main__':
    pybird.init()
    pybird.load('./examples/data/data.case')

    pybird.model.name = 'large soaring wing'
    pybird.model.description = 'example'

    # wing
    pybird.model.geo.wing.thetaRootZ = 1.0

    pybird.model.geo.wing.l0 = 0.025
    pybird.model.geo.wing.l1 = 0.08
    pybird.model.geo.wing.l2 = 0.08
    pybird.model.geo.wing.l3 = 0.12

    # pybird.model.geo.wing.theta2_d = 20.0
    # pybird.model.geo.wing.theta6_d = 40.0

    # pybird.model.geo.wing.theta2_e = 20.0
    # pybird.model.geo.wing.theta6_e = 40.0

    # pybird.model.geo.tail.theta8 = 10.0
    # pybird.model.geo.tail.theta9 = 10.0

    # pybird.model.geo.wing.theta3_d = 10.
    # pybird.model.geo.wing.theta4_d = 20.
    # pybird.model.geo.wing.theta7_d = 20.
    # pybird.model.geo.wing.theta3_e = 10.
    # pybird.model.geo.wing.theta4_e = 20.
    # pybird.model.geo.wing.theta7_e = 20.

    pybird.model.geo.wing.h1 = 0.01
    pybird.model.geo.wing.h4 = 0.02
    pybird.model.geo.wing.delta4 = 0.2
    pybird.model.geo.wing.delta5 = 0.5
    pybird.model.geo.wing.h6 = 0.12

    # body
    pybird.model.geo.body.h12 = 0.018

    # tail
    pybird.model.geo.tail.h20 = 0.06
    pybird.model.geo.tail.h21 = 0.04
    pybird.model.geo.tail.h22 = 0.07

    # save
    pybird.save('./examples/data/large_soaring_wing.case')

    # mesh
    ref = pybird.refinement.model(
        wing=pybird.refinement.wing(
            coef_le=1.5,
            coef_te=1.5,
        ),
        body=pybird.refinement.body(),
        head=pybird.refinement.head(),
        tail=pybird.refinement.tail(
            coef_edge_le=1.5,
            coef_edge_te=1.5,
            coef_tip=1.0,
        ),
    )

    pybird.build(ref, view=False)

    pybird.gen_vtk('./examples/large_soaring_wing')
