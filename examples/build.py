import sys
sys.path.append('./src')

import pybird


if __name__ == '__main__':
    pybird.init()
    pybird.load('./examples/data/data.case')

    ref = pybird.refinement.model(
        wing=pybird.refinement.wing(),
        body=pybird.refinement.body(),
        head=pybird.refinement.head(),
        tail=pybird.refinement.tail(
            coef_edge_le=1.5,
        ),
    )

    pybird.build(ref, view=True)

    pybird.gen_vtk('./examples/file')
