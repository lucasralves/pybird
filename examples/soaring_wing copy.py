import sys
sys.path.append('./src')

import pybird


if __name__ == '__main__':
    pybird.init()
    pybird.load('./examples/data/data.case')

    pybird.model.name = 'soaring wing'
    pybird.model.description = 'example'

    # wing
    pybird.model.geo.wing.thetaRootZ = 1.0

    pybird.model.geo.wing.l1 = 0.14
    pybird.model.geo.wing.l2 = 0.14
    pybird.model.geo.wing.l3 = 0.18

    pybird.model.geo.wing.theta7_e = 15.0
    pybird.model.geo.wing.theta7_d = 15.0

    pybird.model.geo.wing.h1 = 0.03
    pybird.model.geo.wing.h4 = 0.01
    pybird.model.geo.wing.delta5 = 0.2

    # tail
    pybird.model.geo.tail.shape = pybird.TailShape.pointed
    pybird.model.geo.tail.h20 = 0.05
    pybird.model.geo.tail.h21 = 0.02
    pybird.model.geo.tail.h22 = 0.035

    # save
    pybird.save('./examples/data/soaring_wing.case')

    # mesh
    ref = pybird.refinement.model(
        wing=pybird.refinement.wing(),
        body=pybird.refinement.body(),
        head=pybird.refinement.head(),
        tail=pybird.refinement.tail(),
    )

    pybird.build(ref, view=True)

    pybird.gen_vtk('./examples/soaring_wing')
