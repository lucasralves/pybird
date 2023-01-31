import sys
sys.path.append('./src')

import pybird


if __name__ == '__main__':
    pybird.init()
    pybird.load('./examples/data/data.case')

    ref = pybird.RefinementModel(
        wing=pybird.WingRefinementModel(),
        body=pybird.BodyRefinementModel(),
        head=pybird.HeadRefinementModel(),
        tail=pybird.TailRefinementModel(
            coef_edge_le=1.5,
        ),
    )

    pybird.build(ref)

    pybird.gen_vtk('./examples/file')
