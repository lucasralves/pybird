"""
    Geometry and mesh
"""
import sys
sys.path.append('./src/')

import pybird

if __name__ == '__main__':
    
    model = pybird.create_model()
    model.verbose = True
    model.load('./src/tests/data/input/data.case')
    model.geo.build()
    
    ref = pybird.RefinementModel(
        wing=pybird.WingRefinementModel(
            n_chord_le=12,
            n_chord_te=12,
            coef_le=1.3,
            coef_te=1.3,
            sections=[
                pybird.WingSectionsRefinementModel(10, 'Progression', 1.1),
                pybird.WingSectionsRefinementModel(10, 'Progression', 1.1),
                pybird.WingSectionsRefinementModel(4, 'Progression', 1.0),
                pybird.WingSectionsRefinementModel(10, 'Progression', 1.1),
                pybird.WingSectionsRefinementModel(15, 'Progression', 1.1),
                pybird.WingSectionsRefinementModel(10, 'Progression', 1.1),
            ],
        ),
        body=pybird.BodyRefinementModel(
            n_cross_body=12,
            coef_cross_body=1.2,
            n_head=8,
            coef_head=1.1,
            n_tail=8,
            coef_tail=1.1,
        ),
        head=pybird.HeadRefinementModel(),
        tail=pybird.TailRefinementModel(
            coef_edge_le=1.2,
            coef_edge_te=1.2,
            coef_tip=1.05,
            n_1=15,
            n_2=15,
            n_edge=20,
        ),
    )

    model.mesh.build(ref)
    model.view.gen_vtp_file('test')

    print(len(model.mesh.faces))