import sys

sys.path.append('./src')

import pybird

import numpy as np

if __name__ == '__main__':
    
    #--------------------------------#
    # Create model
    model = pybird.model('owl')

    #--------------------------------#
    # Wing
    model.geo.setValue('l0', 0.07)
    model.geo.setValue('l1', 0.2)
    model.geo.setValue('l2', 0.2)
    model.geo.setValue('l3', 0.1)
    model.geo.setValue('h1', 0.05)
    model.geo.setValue('h4', 0.07)
    model.geo.setValue('h5', 0.3)
    model.geo.setValue('h6', 0.3)
    model.geo.setValue('h7', 0.3)
    model.geo.setValue('delta3', 0.2)
    model.geo.setValue('delta4', 0.8)
    model.geo.setValue('delta6', 0.1)
    model.geo.setValue('rootAirfoil', np.loadtxt('./example/data/root_ref.txt'))
    model.geo.setValue('middleAirfoil', np.loadtxt('./example/data/middle_ref.txt'))
    model.geo.setValue('tipAirfoil', np.loadtxt('./example/data/tip_ref.txt'))
    
    #--------------------------------#
    # Body
    model.geo.setValue('h8', 0.12)
    model.geo.setValue('h9', 0.035)
    model.geo.setValue('h10', 0.05)
    model.geo.setValue('h12', 0.05)
    model.geo.setValue('h13', 0.04)
    model.geo.setValue('h14', 0.03)
    model.geo.setValue('h15', 0.04)
    model.geo.setValue('h16', 0.05)

    #--------------------------------#
    # Tail
    model.geo.setValue('tailAirfoil', np.loadtxt('./example/data/tip_ref.txt'))
    model.geo.setValue('tailShape', '3')
    model.geo.setValue('h19', 0.4)
    model.geo.setValue('h20', 0.15)
    model.geo.setValue('delta47', 1.1)
    model.geo.setValue('delta48', 0.2)

    #--------------------------------#
    # Head
    model.geo.setValue('h22', 0.05)
    model.geo.setValue('h23', 0.02)
    model.geo.setValue('h24', 0.05)

    #--------------------------------#
    # Mesh
    model.mesh.build(
        size=0.05,
        refinement=pybird.inputs.Refinement(
            coeff_wing_le=2,
            coeff_wing_te=2,
            coeff_tail_le=3,
            coeff_tail_te=3,
            coeff_head=3,
        ),
    )

    #--------------------------------#
    # View
    model.view.mesh()