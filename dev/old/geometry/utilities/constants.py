from typing import List


Vector = List[float]

wing_axis = ['x1', 'y1', 'z1', 'y2', 'z2', 'x3', 'z3']

wing_side = ['left', 'right']

default_data = {
    # Base axis
    'x0': [1., .0, .0],
    'y0': [.0, 1., .0],
    'z0': [.0, .0, 1.],

    # Wing incidence angle
    'inci_angle_left': .0,
    'inci_angle_right': .0,

    # Wing axis
    'x1_left': [1., .0, .0],
    'y1_left': [.0, 1., .0],
    'z1_left': [.0, .0, 1.],
    'x2_base_left': [1., .0, .0],
    'x2_tip_left': [1., .0, .0],
    'y2_left': [.0, 1., .0],
    'z2_base_left': [.0, .0, 1.],
    'z2_tip_left': [.0, .0, 1.],
    'x3_left': [1., .0, .0],
    'y3_left': [.0, 1., .0],
    'z3_left': [.0, .0, 1.],

    'x1_right': [1., .0, .0],
    'y1_right': [.0, 1., .0],
    'z1_right': [.0, .0, 1.],
    'x2_base_right': [1., .0, .0],
    'x2_tip_right': [1., .0, .0],
    'y2_right': [.0, 1., .0],
    'z2_base_right': [.0, .0, 1.],
    'z2_tip_right': [.0, .0, 1.],
    'x3_right': [1., .0, .0],
    'y3_right': [.0, 1., .0],
    'z3_right': [.0, .0, 1.],

    # Body
    'l1': 0.1,
    'l2': 0.1,
    'l3': 0.1,
    'l4': 0.1,
    'l5': 0.1,
    'l6': 0.5,
    'l7': 0.1,
    'l8': 0.1,
    'l9': 0.1,
    'l10': 0.1,
    'l11': 0.1,
    'l12': 0.1,

    'delta0': .0,
    'delta1': .0,
    'delta2': .0,
    'delta3': .0,
    'delta4': .0,
    'delta5': .0,
    'delta6': .0,
    'delta7': .0,
    'delta8': .0,
    'delta9': .0,
    'delta10': .0,
    'delta11': .0,
    'delta12': .0,
    'delta13': .0,
    'delta14': .0,
    'delta15': .0,
    'delta16': .0,
    'delta17': .0,
    'delta18': .0,
    'delta19': .0,
    'delta20': .0,
    'delta21': .0,
    'delta22': .0,
    'delta23': .0,
    'delta24': .0,
    'delta25': .0,
    'delta26': .0,
    'delta27': .0,
    'delta28': .0,
    'delta29': .0,
    'delta30': .0,
    'delta31': .0,
    'delta32': .0,
    'delta33': .0,
    'delta34': .0,
    'delta35': .0,
    'delta36': .0,
    'delta37': .0,
    'delta38': .0,
    'delta39': .0,
    'delta40': .0,
    'delta41': .0,
    'delta42': .0,
    'delta43': .0,
    'delta44': .0,
    'delta45': .0,
    'delta46': .0,
    'delta47': .0,
    'delta48': .0,

    # Wing
    'l13': 0.1,
    'l14': 0.2,
    'l15': 0.2,

    'delta49': .025,
    'delta50': .3,
    'delta51': .0,
    'delta52': .5,
    'delta53': .0,
    'delta54': .0,
    'delta55': .0,
    'delta56': .0,
    'delta57': .0,
    'delta58': .0,
    'delta59': .0,

    # Tail
    'x4': [-1, 0, 0],
    'y4': [0, -1, 0],
    'z4': [0, 0, 1],
    'tail_shape': 'Rounded',
    'l16': 0.25,
    'l17': 0.6,
    'l18': 0.1,

    # Head
    'l19': 0.15,
    'l20': 0.15,
}