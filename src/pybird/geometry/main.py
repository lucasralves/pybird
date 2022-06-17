from typing import Any
from pybird.geometry.utilities.data import Data

from pybird.geometry.utilities.wing_final_params import WingFinalParams
from pybird.geometry.utilities.body_final_params import BodyFinalParams
from pybird.geometry.utilities.tail_final_params import TailFinalParams
from pybird.geometry.utilities.head_final_params import HeadFinalParams

class Geometry:
    
    def __init__(self) -> None:
        self.data = Data()
        self.wing_params = WingFinalParams(self.data)
        self.body_params = BodyFinalParams(self.data, self.wing_params)
        self.tail_params = TailFinalParams(self.data, self.body_params)
        self.head_params = HeadFinalParams(self.data, self.body_params)
    
    def __update(self) -> None:
        self.wing_params.update()
        self.body_params.update()
        self.tail_params.update()
        self.head_params.update()
    
    def save(self, filename: str) -> None:
        """Save the geometry data in given file"""

        assert '.geo' in filename, 'filename error'

        json_obj = self.data.toJson()
        file = open(filename, 'w')
        file.write(json_obj)
        file.close()
    
    def load(self, filename: str) -> None:
        """Loads the geometry from a .geo file"""

        assert '.geo' in filename, 'filename error'

        self.data = Data.fromJson(filename)
        self.wing_params = WingFinalParams(self.data)
        self.body_params = BodyFinalParams(self.data, self.wing_params)
        self.tail_params = TailFinalParams(self.data, self.body_params)
        self.head_params = HeadFinalParams(self.data, self.body_params)
    
    def setValue(self, param: str, value: Any) -> None:
        # Wing
        if param == 'l0': self.data.l0 = value
        if param == 'l1': self.data.l1 = value
        if param == 'l2': self.data.l2 = value
        if param == 'l3': self.data.l3 = value
        if param == 'thetaInc': self.data.thetaInc = value
        if param == 'theta0': self.data.theta0 = value
        if param == 'theta1e': self.data.theta1e = value
        if param == 'theta2e': self.data.theta2e = value
        if param == 'theta3e': self.data.theta3e = value
        if param == 'theta4e': self.data.theta4e = value
        if param == 'theta5e': self.data.theta5e = value
        if param == 'theta6e': self.data.theta6e = value
        if param == 'theta7e': self.data.theta7e = value
        if param == 'theta1d': self.data.theta1d = value
        if param == 'theta2d': self.data.theta2d = value
        if param == 'theta3d': self.data.theta3d = value
        if param == 'theta4d': self.data.theta4d = value
        if param == 'theta5d': self.data.theta5d = value
        if param == 'theta6d': self.data.theta6d = value
        if param == 'theta7d': self.data.theta7d = value
        if param == 'h1': self.data.h1 = value
        if param == 'h2': self.data.h2 = value
        if param == 'h3': self.data.h3 = value
        if param == 'h4': self.data.h4 = value
        if param == 'h5': self.data.h5 = value
        if param == 'h6': self.data.h6 = value
        if param == 'h7': self.data.h7 = value
        if param == 'delta1': self.data.delta1 = value
        if param == 'delta2': self.data.delta2 = value
        if param == 'delta3': self.data.delta3 = value
        if param == 'delta4': self.data.delta4 = value
        if param == 'delta5': self.data.delta5 = value
        if param == 'delta6': self.data.delta6 = value
        if param == 'epsilon1': self.data.epsilon1 = value
        if param == 'epsilon2': self.data.epsilon2 = value
        if param == 'epsilon3': self.data.epsilon3 = value
        if param == 'rootAirfoil': self.data.rootAirfoil = value
        if param == 'middleAirfoil': self.data.middleAirfoil = value
        if param == 'tipAirfoil': self.data.tipAirfoil = value
        if param == 'delta': self.data.delta = value

        # Body
        if param == 'h8': self.data.h8 = value
        if param == 'h9': self.data.h9 = value
        if param == 'h10': self.data.h10 = value
        if param == 'h11': self.data.h11 = value
        if param == 'h12': self.data.h12 = value
        if param == 'h13': self.data.h13 = value
        if param == 'h14': self.data.h14 = value
        if param == 'h15': self.data.h15 = value
        if param == 'h16': self.data.h16 = value
        if param == 'h17': self.data.h17 = value
        if param == 'h18': self.data.h18 = value
        if param == 'delta7': self.data.delta7 = value
        if param == 'delta8': self.data.delta8 = value
        if param == 'delta9': self.data.delta9 = value
        if param == 'delta10': self.data.delta10 = value
        if param == 'delta11': self.data.delta11 = value
        if param == 'delta12': self.data.delta12 = value
        if param == 'delta13': self.data.delta13 = value
        if param == 'delta14': self.data.delta14 = value
        if param == 'delta15': self.data.delta15 = value
        if param == 'delta16': self.data.delta16 = value
        if param == 'delta17': self.data.delta17 = value
        if param == 'delta18': self.data.delta18 = value
        if param == 'delta19': self.data.delta19 = value
        if param == 'delta20': self.data.delta20 = value
        if param == 'delta21': self.data.delta21 = value
        if param == 'delta22': self.data.delta22 = value
        if param == 'delta23': self.data.delta23 = value
        if param == 'delta24': self.data.delta24 = value
        if param == 'delta25': self.data.delta25 = value
        if param == 'delta26': self.data.delta26 = value
        if param == 'delta27': self.data.delta27 = value
        if param == 'delta28': self.data.delta28 = value
        if param == 'delta29': self.data.delta29 = value
        if param == 'delta30': self.data.delta30 = value
        if param == 'delta31': self.data.delta31 = value
        if param == 'delta32': self.data.delta32 = value
        if param == 'delta33': self.data.delta33 = value
        if param == 'delta34': self.data.delta34 = value
        if param == 'delta35': self.data.delta35 = value
        if param == 'delta36': self.data.delta36 = value
        if param == 'delta37': self.data.delta37 = value
        if param == 'delta38': self.data.delta38 = value
        if param == 'delta39': self.data.delta39 = value
        if param == 'delta40': self.data.delta40 = value
        if param == 'delta41': self.data.delta41 = value
        if param == 'delta42': self.data.delta42 = value
        if param == 'delta43': self.data.delta43 = value
        if param == 'delta44': self.data.delta44 = value
        if param == 'delta45': self.data.delta45 = value
        if param == 'delta46': self.data.delta46 = value

        # Tail
        if param == 'h19': self.data.h19 = value
        if param == 'h20': self.data.h20 = value
        if param == 'h21': self.data.h21 = value
        if param == 'delta47': self.data.delta47 = value
        if param == 'delta48': self.data.delta48 = value
        if param == 'theta8': self.data.theta8 = value
        if param == 'theta9': self.data.theta9 = value
        if param == 'theta10': self.data.theta10 = value
        if param == 'tailShape': self.data.tailShape = value
        if param == 'tailAirfoil': self.data.tailAirfoil = value

        # Head
        if param == 'h22': self.data.h22 = value
        if param == 'h23': self.data.h23 = value
        if param == 'h24': self.data.h24 = value
        if param == 'delta49': self.data.delta49 = value
        if param == 'delta50': self.data.delta50 = value

        # Update
        self.wing_params.update()
        self.body_params.update()
        self.head_params.update()
        self.tail_params.update()

    def addWingRotation(self, axis: str, angle: float, side: str) -> None:
        """
        Add rotation to one of the wing system 1, 2 or 3.
        
        Parameters
        ----------
        > axis: "x1", "y1", "z1", "y2", "z2", "x3" or "z3"
        > angle: rotation in degrees. Each axis has a maximum value allowed
        > side: "left", "right" or "both"
        """

        assert axis in ["x1", "y1", "z1", "y2", "z2", "x3", "z3"], "axis not found"
        assert side in ["left", "right", "both"], "side not found"

        if axis == "x1":
            if side == "left":
                self.data.theta1e = angle + self.data.theta1e
            elif side == "right":
                self.data.theta1d = angle + self.data.theta1d
            else:
                self.data.theta1e = angle + self.data.theta1e
                self.data.theta1d = angle + self.data.theta1d
        elif axis == "y1":
            if side == "left":
                self.data.theta2e = angle + self.data.theta2e
            elif side == "right":
                self.data.theta2d = angle + self.data.theta2d
            else:
                self.data.theta2e = angle + self.data.theta2e
                self.data.theta2d = angle + self.data.theta2d
        elif axis == "z1":
            if side == "left":
                self.data.theta3e = angle + self.data.theta3e
            elif side == "right":
                self.data.theta3d = angle + self.data.theta3d
            else:
                self.data.theta3e = angle + self.data.theta3e
                self.data.theta3d = angle + self.data.theta3d
        elif axis == "y2":
            if side == "left":
                self.data.theta4e = angle + self.data.theta4e
            elif side == "right":
                self.data.theta4d = angle + self.data.theta4d
            else:
                self.data.theta4e = angle + self.data.theta4e
                self.data.theta4d = angle + self.data.theta4d
        elif axis == "z2":
            if side == "left":
                self.data.theta5e = angle + self.data.theta5e
            elif side == "right":
                self.data.theta5d = angle + self.data.theta5d
            else:
                self.data.theta5e = angle + self.data.theta5e
                self.data.theta5d = angle + self.data.theta5d
        elif axis == "x3":
            if side == "left":
                self.data.theta6e = angle + self.data.theta6e
            elif side == "right":
                self.data.theta6d = angle + self.data.theta6d
            else:
                self.data.theta6e = angle + self.data.theta6e
                self.data.theta6d = angle + self.data.theta6d
        elif axis == "z3":
            if side == "left":
                self.data.theta7e = angle + self.data.theta7e
            elif side == "right":
                self.data.theta7d = angle + self.data.theta7d
            else:
                self.data.theta7e = angle + self.data.theta7e
                self.data.theta7d = angle + self.data.theta7d
    
    def addTailRotation(self, axis: str, angle: float) -> None:
        """
        Add rotation to the tail
        
        Parameters
        ----------
        > axis: "x4", "y4", "z4"
        > angle: rotation in degrees. Each axis has a maximum value allowed
        """

        assert axis in ["x4", "y4", "z4"], "axis not found"

        if axis == "x4":
            self.data.theta8 = angle + self.data.theta8
        elif axis == "y4":
            self.data.theta9 = angle + self.data.theta9
        elif axis == "z4":
            self.data.theta10 = angle + self.data.theta10