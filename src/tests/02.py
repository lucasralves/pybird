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
            n_chord_le=10,
            n_chord_te=10,
            coef_le=1.5,
            coef_te=1.5,
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
            n_cross_body=6,
            coef_cross_body=1.2,
            n_head=4,
            coef_head=1.1,
            n_tail=4,
            coef_tail=1.1,
        ),
        head=pybird.HeadRefinementModel(
            n_1=5,
            n_2=5,
        ),
        tail=pybird.TailRefinementModel(
            coef_edge_le=1.2,
            coef_edge_te=1.2,
            coef_tip=1.05,
            n_1=15,
            n_2=5,
            n_edge=7,
        ),
    )

    model.mesh.build(ref)
    model.view.gen_vtp_file('test')