from json import loads, dumps
from math import cos, pi, sin
from numpy import argmax, flip, loadtxt
from scipy.spatial.transform import Rotation as R

from pybird.geometry.utilities.constants import default_data, wing_axis, wing_side
from pybird.geometry.utilities.final_parameters import FinalParameters

class Geometry:
    
    def __init__(self) -> None:
        self.data = default_data
        self.params = FinalParameters(default_data)
        self.filename: str = None
        return

    def load(self, file: str) -> None:
        """load a .geo file"""
        file_opended = open(file)
        self.data = loads(file_opended.read())
        self.params = FinalParameters(self.data)
        file_opended.close()
        self.filename = file
        return
    
    def save(self, file: str) -> None:
        """save a .geo file"""
        file_opended = open(file, 'w')
        file_opended.write(dumps(self.data, indent=4))
        file_opended.close()
        return
    
    def addTailFoil(self, file: str) -> None:
        """The points must be in anticlockwise and must start and end at the same point."""

        p_top = self.params.p8
        p_bottom = self.params.p12

        foil = loadtxt(file)

        index_max = argmax(foil[:, 1])
        index_min = argmax(foil[:, 1])

        if self.data['tail_shape'] == 'Square':
            p_end = self.params.p20_square
        elif self.data['tail_shape'] == 'V':
            p_end = self.params.p20_V
        elif self.data['tail_shape'] == 'Pointed':
            p_end = self.params.p20_pointed
        else:
            p_end = self.params.p20_rounded
        
        top_curve = foil[:index_max + 1, :]
        bottom_curve = flip(foil[index_min:, :], 0)

        v_top = p_end - p_top

        return
    
    def removeWingRotations(self) -> None:
        self.data['x1_left'] = [1., .0, .0]
        self.data['y1_left'] = [.0, 1., .0]
        self.data['z1_left'] = [.0, .0, 1.]
        self.data['x2_base_left'] = [1., .0, .0]
        self.data['x2_tip_left'] = [1., .0, .0]
        self.data['y2_left'] = [.0, 1., .0]
        self.data['z2_base_left'] = [.0, .0, 1.]
        self.data['z2_tip_left'] = [.0, .0, 1.]
        self.data['x3_left'] = [1., .0, .0]
        self.data['y3_left'] = [.0, 1., .0]
        self.data['z3_left'] = [.0, .0, 1.]

        self.data['x1_right'] = [1., .0, .0]
        self.data['y1_right'] = [.0, 1., .0]
        self.data['z1_right'] = [.0, .0, 1.]
        self.data['x2_base_right'] = [1., .0, .0]
        self.data['x2_tip_right'] = [1., .0, .0]
        self.data['y2_right'] = [.0, 1., .0]
        self.data['z2_base_right'] = [.0, .0, 1.]
        self.data['z2_tip_right'] = [.0, .0, 1.]
        self.data['x3_right'] = [1., .0, .0]
        self.data['y3_right'] = [.0, 1., .0]
        self.data['z3_right'] = [.0, .0, 1.]

        self.params.updateData(self.data)
        return
    
    def removeTailRotations(self) -> None:

        self.data['x4'] = [-1., .0, .0]
        self.data['y4'] = [.0, -1., .0]
        self.data['z4'] = [.0, .0, 1.]

        self.params.updateData(self.data)
        return
    
    def addRotation(self, axis: str, angle: float, side: str = 'left') -> None:

        if axis in ['x4', 'y4', 'z4']:
            angle_rad = angle * pi / 180
            s, c = sin(angle_rad / 2), cos(angle_rad / 2)
            axis_vec = self.data[axis]

            rot = R.from_quat([axis_vec[0] * s, axis_vec[1] * s, axis_vec[2] * s, c])

            self.data['x4'] = rot.apply(self.data['x4']).tolist()
            self.data['y4'] = rot.apply(self.data['y4']).tolist()
            self.data['z4'] = rot.apply(self.data['z4']).tolist()

            self.params.updateData(self.data)

            return
        
        if not (axis in wing_axis): raise 'incorrect wing axis'
        if not (side in wing_side): raise 'incorrect wing side'

        # Sign correction for left or right wing
        if '1' in axis:
            sign = -1 if axis == 'y1' else 1
        elif '2' in axis:
            sign = -1
        elif '3' in axis:
            sign = -1 if axis == 'x3' else 1
        
        mult = 1 if side == 'left' else 1 if 'y' in axis else -1
        sign = mult * sign

        # Create rotattion
        if '2' in axis:
            if axis == 'y2':
                key = '{}_{}'.format(axis, side)
            else:
                key = '{}_tip_{}'.format(axis, side)
        else:
            key = '{}_{}'.format(axis, side)
        
        angle_rad = angle * pi / 180
        s, c = sin(angle_rad / 2), cos(angle_rad / 2)
        axis_vec = self.data[key]
        
        rot = R.from_quat([sign * axis_vec[0] * s, sign * axis_vec[1] * s, sign * axis_vec[2] * s, c])

        # Wing incidence angle
        if axis == 'y1':
            self.data['inci_angle_{}'.format(side)] = self.data['inci_angle_{}'.format(side)] + angle_rad
        
        # Apply rotation
        if '1' in axis:
            self.data['x1_{}'.format(side)] = rot.apply(self.data['x1_{}'.format(side)]).tolist()
            self.data['y1_{}'.format(side)] = rot.apply(self.data['y1_{}'.format(side)]).tolist()
            self.data['z1_{}'.format(side)] = rot.apply(self.data['z1_{}'.format(side)]).tolist()

        if '2' in axis or '1' in axis:
            if '1' in axis or not ('y' in axis):
                self.data['x2_base_{}'.format(side)] = rot.apply(self.data['x2_base_{}'.format(side)]).tolist()
                self.data['x2_tip_{}'.format(side)] = rot.apply(self.data['x2_tip_{}'.format(side)]).tolist()
                self.data['y2_{}'.format(side)] = rot.apply(self.data['y2_{}'.format(side)]).tolist()
                self.data['z2_base_{}'.format(side)] = rot.apply(self.data['z2_base_{}'.format(side)]).tolist()
                self.data['z2_tip_{}'.format(side)] = rot.apply(self.data['z2_tip_{}'.format(side)]).tolist()
            else:
                self.data['x2_tip_{}'.format(side)] = rot.apply(self.data['x2_tip_{}'.format(side)]).tolist()
                self.data['z2_tip_{}'.format(side)] = rot.apply(self.data['z2_tip_{}'.format(side)]).tolist()


        if '3' in axis or '2' in axis or '1' in axis:
            self.data['x3_{}'.format(side)] = rot.apply(self.data['x3_{}'.format(side)]).tolist()
            self.data['y3_{}'.format(side)] = rot.apply(self.data['y3_{}'.format(side)]).tolist()
            self.data['z3_{}'.format(side)] = rot.apply(self.data['z3_{}'.format(side)]).tolist()
        
        self.params.updateData(self.data)
        return
    
    def updateValue(self, key: str, value: float) -> None:
        if not key in self.data: raise 'key not found'
        self.data[key] = value
        self.params.updateData(self.data)
        return
    
    def sumToValue(self, key: str, value: float) -> None:
        if not key in self.data: raise 'key not found'
        self.data[key] = self.data[key] + value
        self.params.updateData(self.data)
        return