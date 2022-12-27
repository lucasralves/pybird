"""
    Solver
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
            n_chord_le=4, # 15
            n_chord_te=4, # 12
            coef_le=1.5,
            coef_te=1.5,
            sections=[
                pybird.WingSectionsRefinementModel(5, 'Progression', 1.1),
                pybird.WingSectionsRefinementModel(5, 'Progression', 1.1),
                pybird.WingSectionsRefinementModel(3, 'Progression', 1.0),
                pybird.WingSectionsRefinementModel(5, 'Progression', 1.1),
                pybird.WingSectionsRefinementModel(7, 'Progression', 1.1),
                pybird.WingSectionsRefinementModel(5, 'Progression', 1.1),
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
            coef_edge_le=1.5,
            coef_edge_te=1.2,
            coef_tip=1.05,
            n_1=10,
            n_2=5,
            n_edge=7,
        ),
    )

    model.mesh.build(ref)

    model.solver.solve(1.0, wake_length=0.05, time_step=0.05)

    model.view.gen_vtp_file('test', show_wake=True)