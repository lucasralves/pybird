from __future__ import annotations
from json import dumps, load
from numpy import array, asarray, copy

from pybird.helpers.type import Curve, Quaternion, Vector
from pybird.helpers import quaternion

class Data:

    @staticmethod
    def fromJson(filename: str) -> Data:
        file = open(filename)
        params = load(file)
        file.close()

        data = Data()

        data.l0 = params['l0']
        data.l1 = params['l1']
        data.l2 = params['l2']
        data.l3 = params['l3']
        data.thetaInc = params['thetaInc']
        data.theta0 = params['theta0']
        data.theta1e = params['theta1e']
        data.theta2e = params['theta2e']
        data.theta3e = params['theta3e']
        data.theta4e = params['theta4e']
        data.theta5e = params['theta5e']
        data.theta6e = params['theta6e']
        data.theta7e = params['theta7e']
        data.theta1d = params['theta1d']
        data.theta2d = params['theta2d']
        data.theta3d = params['theta3d']
        data.theta4d = params['theta4d']
        data.theta5d = params['theta5d']
        data.theta6d = params['theta6d']
        data.theta7d = params['theta7d']
        data.h1 = params['h1']
        data.h2 = params['h2']
        data.h3 = params['h3']
        data.h4 = params['h4']
        data.h5 = params['h5']
        data.h6 = params['h6']
        data.h7 = params['h7']
        data.delta1 = params['delta1']
        data.delta2 = params['delta2']
        data.delta3 = params['delta3']
        data.delta4 = params['delta4']
        data.delta5 = params['delta5']
        data.delta6 = params['delta6']
        data.epsilon1 = params['epsilon1']
        data.epsilon2 = params['epsilon2']
        data.epsilon3 = params['epsilon3']
        data.rootAirfoil = None if params['rootAirfoil'] is None else asarray(params['rootAirfoil'])
        data.middleAirfoil = None if params['middleAirfoil'] is None else asarray(params['middleAirfoil'])
        data.tipAirfoil = None if params['tipAirfoil'] is None else asarray(params['tipAirfoil'])
        data.delta = params['delta']

        data.h8 = params['h8']
        data.h9 = params['h9']
        data.h10 = params['h10']
        data.h11 = params['h11']
        data.h12 = params['h12']
        data.h13 = params['h13']
        data.h14 = params['h14']
        data.h15 = params['h15']
        data.h16 = params['h16']
        data.h17 = params['h17']
        data.h18 = params['h18']
        data.delta7 = params['delta7']
        data.delta8 = params['delta8']
        data.delta9 = params['delta9']
        data.delta10 = params['delta10']
        data.delta11 = params['delta11']
        data.delta12 = params['delta12']
        data.delta13 = params['delta13']
        data.delta14 = params['delta14']
        data.delta15 = params['delta15']
        data.delta16 = params['delta16']
        data.delta17 = params['delta17']
        data.delta18 = params['delta18']
        data.delta19 = params['delta19']
        data.delta20 = params['delta20']
        data.delta21 = params['delta21']
        data.delta22 = params['delta22']
        data.delta23 = params['delta23']
        data.delta24 = params['delta24']
        data.delta25 = params['delta25']
        data.delta26 = params['delta26']
        data.delta27 = params['delta27']
        data.delta28 = params['delta28']
        data.delta29 = params['delta29']
        data.delta30 = params['delta30']
        data.delta31 = params['delta31']
        data.delta32 = params['delta32']
        data.delta33 = params['delta33']
        data.delta34 = params['delta34']
        data.delta35 = params['delta35']
        data.delta36 = params['delta36']
        data.delta37 = params['delta37']
        data.delta38 = params['delta38']
        data.delta39 = params['delta39']
        data.delta40 = params['delta40']
        data.delta41 = params['delta41']
        data.delta42 = params['delta42']
        data.delta43 = params['delta43']
        data.delta44 = params['delta44']
        data.delta45 = params['delta45']
        data.delta46 = params['delta46']

        data.h19 = params['h19']
        data.h20 = params['h20']
        data.h21 = params['h21']
        data.delta47 = params['delta47']
        data.delta48 = params['delta48']
        data.theta8 = params['theta8']
        data.theta9 = params['theta9']
        data.theta10 = params['theta10']
        data.tailShape = params['tailShape']
        data.tailAirfoil = None if params['tailAirfoil'] is None else asarray(params['tailAirfoil'])

        data.h22 = params['h22']
        data.h23 = params['h23']
        data.h24 = params['h24']
        data.delta49 = params['delta49']
        data.delta50 = params['delta50']
        
        return data

    def toJson(self) -> str:
        data = {
            'l0': self.l0,
            'l1': self.l1,
            'l2': self.l2,
            'l3': self.l3,
            'thetaInc': self.thetaInc,
            'theta0': self.theta0,
            'theta1e': self.theta1e,
            'theta2e': self.theta2e,
            'theta3e': self.theta3e,
            'theta4e': self.theta4e,
            'theta5e': self.theta5e,
            'theta6e': self.theta6e,
            'theta7e': self.theta7e,
            'theta1d': self.theta1d,
            'theta2d': self.theta2d,
            'theta3d': self.theta3d,
            'theta4d': self.theta4d,
            'theta5d': self.theta5d,
            'theta6d': self.theta6d,
            'theta7d': self.theta7d,
            'h1': self.h1,
            'h2': self.h2,
            'h3': self.h3,
            'h4': self.h4,
            'h5': self.h5,
            'h6': self.h6,
            'h7': self.h7,
            'delta1': self.delta1,
            'delta2': self.delta2,
            'delta3': self.delta3,
            'delta4': self.delta4,
            'delta5': self.delta5,
            'delta6': self.delta6,
            'epsilon1': self.epsilon1,
            'epsilon2': self.epsilon2,
            'epsilon3': self.epsilon3,
            'rootAirfoil': self.rootAirfoil,
            'middleAirfoil': self.middleAirfoil,
            'tipAirfoil': self.tipAirfoil,
            'delta': self.delta,
            'h8': self.h8,
            'h9': self.h9,
            'h10': self.h10,
            'h11': self.h11,
            'h12': self.h12,
            'h13': self.h13,
            'h14': self.h14,
            'h15': self.h15,
            'h16': self.h16,
            'h17': self.h17,
            'h18': self.h18,
            'delta7': self.delta7,
            'delta8': self.delta8,
            'delta9': self.delta9,
            'delta10': self.delta10,
            'delta11': self.delta11,
            'delta12': self.delta12,
            'delta13': self.delta13,
            'delta14': self.delta14,
            'delta15': self.delta15,
            'delta16': self.delta16,
            'delta17': self.delta17,
            'delta18': self.delta18,
            'delta19': self.delta19,
            'delta20': self.delta20,
            'delta21': self.delta21,
            'delta22': self.delta22,
            'delta23': self.delta23,
            'delta24': self.delta24,
            'delta25': self.delta25,
            'delta26': self.delta26,
            'delta27': self.delta27,
            'delta28': self.delta28,
            'delta29': self.delta29,
            'delta30': self.delta30,
            'delta31': self.delta31,
            'delta32': self.delta32,
            'delta33': self.delta33,
            'delta34': self.delta34,
            'delta35': self.delta35,
            'delta36': self.delta36,
            'delta37': self.delta37,
            'delta38': self.delta38,
            'delta39': self.delta39,
            'delta40': self.delta40,
            'delta41': self.delta41,
            'delta42': self.delta42,
            'delta43': self.delta43,
            'delta44': self.delta44,
            'delta45': self.delta45,
            'delta46': self.delta46,
            'h19': self.h19,
            'h20': self.h20,
            'h21': self.h21,
            'delta47': self.delta47,
            'delta48': self.delta48,
            'theta8': self.theta8,
            'theta9': self.theta9,
            'theta10': self.theta10,
            'tailShape': self.tailShape,
            'tailAirfoil': self.tailAirfoil,
            'h22': self.h22,
            'h23': self.h23,
            'h24': self.h24,
            'delta49': self.delta49,
            'delta50': self.delta50,
        }
        json_obj = dumps(data, indent=2)
        return json_obj

    def __init__(self) -> None:
        
        # Wing
        self.l0 = 0.08
        self.l1 = 0.15
        self.l2 = 0.3
        self.l3 = 0.2
        self.thetaInc = 2.0
        self.theta0 = 2.0
        self.theta1e = .0
        self.theta2e = .0
        self.theta3e = .0
        self.theta4e = .0
        self.theta5e = .0
        self.theta6e = .0
        self.theta7e = .0
        self.theta1d = .0
        self.theta2d = .0
        self.theta3d = .0
        self.theta4d = .0
        self.theta5d = .0
        self.theta6d = .0
        self.theta7d = .0
        self.h1 = 0.05
        self.h2 = 0.02
        self.h3 = 0.02
        self.h4 = 0.2
        self.h5 = 0.4
        self.h6 = 0.3
        self.h7 = 0.3
        self.delta1 = .05
        self.delta2 = .5
        self.delta3 = .0
        self.delta4 = .1
        self.delta5 = .0
        self.delta6 = .05
        self.epsilon1 = 0.4
        self.epsilon2 = 0.2
        self.epsilon3 = 0.2
        self.rootAirfoil = None
        self.middleAirfoil = None
        self.tipAirfoil = None
        self.delta = 0.05

        # Body
        self.h8 = 0.1
        self.h9 = 0.035
        self.h10 = 0.05
        self.h11 = 0.05
        self.h12 = 0.055
        self.h13 = 0.03
        self.h14 = 0.02
        self.h15 = 0.05
        self.h16 = 0.06
        self.h17 = 0.1
        self.h18 = 0.1
        self.delta7 = .1
        self.delta8 = .1
        self.delta9 = .1
        self.delta10 = .1
        self.delta11 = .05
        self.delta12 = .05
        self.delta13 = .05
        self.delta14 = .05
        self.delta15 = .05
        self.delta16 = .05
        self.delta17 = .05
        self.delta18 = .05
        self.delta19 = .05
        self.delta20 = .05
        self.delta21 = .05
        self.delta22 = .05
        self.delta23 = .05
        self.delta24 = .05
        self.delta25 = .05
        self.delta26 = .05
        self.delta27 = .05
        self.delta28 = .05
        self.delta29 = .05
        self.delta30 = .05
        self.delta31 = .05
        self.delta32 = .05
        self.delta33 = .05
        self.delta34 = .05
        self.delta35 = .05
        self.delta36 = .05
        self.delta37 = .05
        self.delta38 = .05
        self.delta39 = .05
        self.delta40 = .5
        self.delta41 = .5
        self.delta42 = .5
        self.delta43 = .5
        self.delta44 = .5
        self.delta45 = .5
        self.delta46 = .5

        # Tail
        self.h19 = 0.4
        self.h20 = 0.2
        self.h21 = 0.15
        self.delta47 = 0.5
        self.delta48 = 0.5
        self.theta8 = .0
        self.theta9 = .0
        self.theta10 = .0
        self.tailShape = '4' # 1 = square; 2 = v; 3 = pointed; 4 = rounded
        self.tailAirfoil = None

        # Head
        self.h22 = 0.08
        self.h23 = 0.015
        self.h24 = 0.05
        self.delta49 = 0.5
        self.delta50 = 0.5

        return
    
    #########################################################
    # Constants
    #########################################################

    @property
    def x0(self) -> Vector:
        return array([1., .0, .0])
    
    @property
    def y0(self) -> Vector:
        return array([.0, 1., .0])
    
    @property
    def z0(self) -> Vector:
        return array([.0, .0, 1.])
    
    #########################################################
    # Inputs
    #########################################################

    #-------------------------------------#
    @property
    def l0(self) -> float:
        return self.__l0
    
    @l0.setter
    def l0(self, value: float) -> None:
        if 0 < value < 1: self.__l0 = value
    
    #-------------------------------------#
    @property
    def l1(self) -> float:
        return self.__l1
    
    @l1.setter
    def l1(self, value: float) -> None:
        if 0 < value < 1: self.__l1 = value
    
    #-------------------------------------#
    @property
    def l2(self) -> float:
        return self.__l2
    
    @l2.setter
    def l2(self, value: float) -> None:
        if 0 < value < 1: self.__l2 = value
    
    #-------------------------------------#
    @property
    def l3(self) -> float:
        return self.__l3
    
    @l3.setter
    def l3(self, value: float) -> None:
        if 0 < value < 1: self.__l3 = value
    
    #-------------------------------------#
    @property
    def theta0(self) -> float:
        return self.__theta0
    
    @theta0.setter
    def theta0(self, value: float) -> None:
        if -10 < value < 10: self.__theta0 = value
        if value < -10: self.__theta0 = -10
        if value > 10: self.__theta0 = 10
    
    #-------------------------------------#
    @property
    def theta1e(self) -> float:
        return self.__theta1e
    
    @theta1e.setter
    def theta1e(self, value: float) -> None:
        if -70 < value < 70: self.__theta1e = value
        if value < -70: self.__theta1e = -70
        if value > 70: self.__theta1e = 70
    
    #-------------------------------------#
    @property
    def theta2e(self) -> float:
        return self.__theta2e
    
    @theta2e.setter
    def theta2e(self, value: float) -> None:
        if -20 < value < 20: self.__theta2e = value
        if value < -20: self.__theta2e = -20
        if value > 20: self.__theta2e = 20
    
    #-------------------------------------#
    @property
    def theta3e(self) -> float:
        return self.__theta3e
    
    @theta3e.setter
    def theta3e(self, value: float) -> None:
        if -45 < value < 45: self.__theta3e = value
        if value < -45: self.__theta3e = -45
        if value > 45: self.__theta3e = 45
    
    #-------------------------------------#
    @property
    def theta4e(self) -> float:
        return self.__theta4e
    
    @theta4e.setter
    def theta4e(self, value: float) -> None:
        if -45 < value < 45: self.__theta4e = value
        if value < -45: self.__theta4e = -45
        if value > 45: self.__theta4e = 45
    
    #-------------------------------------#
    @property
    def theta5e(self) -> float:
        return self.__theta5e
    
    @theta5e.setter
    def theta5e(self, value: float) -> None:
        if 0 <= value < 45: self.__theta5e = value
        if value < 0: self.__theta5e = 0
        if value > 45: self.__theta5e = 45
    
    #-------------------------------------#
    @property
    def theta6e(self) -> float:
        return self.__theta6e
    
    @theta6e.setter
    def theta6e(self, value: float) -> None:
        if -45 < value < 60: self.__theta6e = value
        if value < -45: self.__theta6e = -45
        if value > 60: self.__theta6e = 60
    
    #-------------------------------------#
    @property
    def theta7e(self) -> float:
        return self.__theta7e
    
    @theta7e.setter
    def theta7e(self, value: float) -> None:
        if -45 < value < 60: self.__theta7e = value
        if value < -45: self.__theta7e = -45
        if value > 60: self.__theta7e = 60
    
    #-------------------------------------#
    @property
    def theta1d(self) -> float:
        return self.__theta1d
    
    @theta1d.setter
    def theta1d(self, value: float) -> None:
        if -70 < value < 70: self.__theta1d = value
        if value < -70: self.__theta1d = -70
        if value > 70: self.__theta1d = 70
    
    #-------------------------------------#
    @property
    def theta2d(self) -> float:
        return self.__theta2d
    
    @theta2d.setter
    def theta2d(self, value: float) -> None:
        if -20 < value < 20: self.__theta2d = value
        if value < -20: self.__theta2d = -20
        if value > 20: self.__theta2d = 20
    
    #-------------------------------------#
    @property
    def theta3d(self) -> float:
        return self.__theta3d
    
    @theta3d.setter
    def theta3d(self, value: float) -> None:
        if -45 < value < 45: self.__theta3d = value
        if value < -45: self.__theta3d = -45
        if value > 45: self.__theta3d = 45
    
    #-------------------------------------#
    @property
    def theta4d(self) -> float:
        return self.__theta4d
    
    @theta4d.setter
    def theta4d(self, value: float) -> None:
        if -45 < value < 45: self.__theta4d = value
        if value < -45: self.__theta4d = -45
        if value > 45: self.__theta4d = 45
    
    #-------------------------------------#
    @property
    def theta5d(self) -> float:
        return self.__theta5d
    
    @theta5d.setter
    def theta5d(self, value: float) -> None:
        if 0 <= value < 45: self.__theta5d = value
        if value < 0: self.__theta5d = 0
        if value > 45: self.__theta5d = 45
    
    #-------------------------------------#
    @property
    def theta6d(self) -> float:
        return self.__theta6d
    
    @theta6d.setter
    def theta6d(self, value: float) -> None:
        if -45 < value < 60: self.__theta6d = value
        if value < -45: self.__theta6d = -45
        if value > 60: self.__theta6d = 60
    
    #-------------------------------------#
    @property
    def theta7d(self) -> float:
        return self.__theta7d
    
    @theta7d.setter
    def theta7d(self, value: float) -> None:
        if -45 < value < 60: self.__theta7d = value
        if value < -45: self.__theta7d = -45
        if value > 60: self.__theta7d = 60
    
    #-------------------------------------#
    @property
    def h1(self) -> float:
        return self.__h1
    
    @h1.setter
    def h1(self, value: float) -> None:
        if 0 <= value < 1: self.__h1 = value
    
    #-------------------------------------#
    @property
    def h2(self) -> float:
        return self.__h2
    
    @h2.setter
    def h2(self, value: float) -> None:
        if 0 <= value < 1: self.__h2 = value
    
    #-------------------------------------#
    @property
    def h3(self) -> float:
        return self.__h3
    
    @h3.setter
    def h3(self, value: float) -> None:
        if 0 <= value < 1: self.__h3 = value
    
    #-------------------------------------#
    @property
    def h4(self) -> float:
        return self.__h4
    
    @h4.setter
    def h4(self, value: float) -> None:
        if 0 <= value < 1: self.__h4 = value
    
    #-------------------------------------#
    @property
    def h5(self) -> float:
        return self.__h5
    
    @h5.setter
    def h5(self, value: float) -> None:
        if 0 <= value < 1: self.__h5 = value
    
    #-------------------------------------#
    @property
    def h6(self) -> float:
        return self.__h6
    
    @h6.setter
    def h6(self, value: float) -> None:
        if 0 <= value < 1: self.__h6 = value
    
    #-------------------------------------#
    @property
    def h7(self) -> float:
        return self.__h7
    
    @h7.setter
    def h7(self, value: float) -> None:
        if 0 <= value < 1: self.__h7 = value
    
    #-------------------------------------#
    @property
    def delta1(self) -> float:
        return self.__delta1
    
    @delta1.setter
    def delta1(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta1 = value
    
    #-------------------------------------#
    @property
    def delta2(self) -> float:
        return self.__delta2
    
    @delta2.setter
    def delta2(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta2 = value
    
    #-------------------------------------#
    @property
    def delta3(self) -> float:
        return self.__delta3
    
    @delta3.setter
    def delta3(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta3 = value
    
    #-------------------------------------#
    @property
    def delta4(self) -> float:
        return self.__delta4
    
    @delta4.setter
    def delta4(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta4 = value
    
    #-------------------------------------#
    @property
    def delta5(self) -> float:
        return self.__delta5
    
    @delta5.setter
    def delta5(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta5 = value
    
    #-------------------------------------#
    @property
    def delta6(self) -> float:
        return self.__delta6
    
    @delta6.setter
    def delta6(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta6 = value
    
    #-------------------------------------#
    @property
    def epsilon1(self) -> float:
        return self.__epsilon1
    
    @epsilon1.setter
    def epsilon1(self, value: float) -> None:
        if 0 <= value <= 1: self.__epsilon1 = value
    
    #-------------------------------------#
    @property
    def epsilon2(self) -> float:
        return self.__epsilon2
    
    @epsilon2.setter
    def epsilon2(self, value: float) -> None:
        if 0 <= value <= 1: self.__epsilon2 = value
    
    #-------------------------------------#
    @property
    def rootAirfoil(self) -> Curve:
        return self.__rootAirfoil
    
    @rootAirfoil.setter
    def rootAirfoil(self, value: Curve) -> None:
        if value is not None and value.shape[1] == 2 and value.shape[0] >= 5:
            self.__rootAirfoil = value
        else:
            self.__rootAirfoil = None
    
    #-------------------------------------#
    @property
    def middleAirfoil(self) -> Curve:
        return self.__middleAirfoil
    
    @middleAirfoil.setter
    def middleAirfoil(self, value: Curve) -> None:
        if value is not None and value.shape[1] == 2 and value.shape[0] >= 5:
            self.__middleAirfoil = value
        else:
            self.__middleAirfoil = None
    
    #-------------------------------------#
    @property
    def tipAirfoil(self) -> Curve:
        return self.__tipAirfoil
    
    @tipAirfoil.setter
    def tipAirfoil(self, value: Curve) -> None:
        if value is not None and value.shape[1] == 2 and value.shape[0] >= 5:
            self.__tipAirfoil = value
        else:
            self.__tipAirfoil = None
    
    #-------------------------------------#
    @property
    def delta(self) -> float:
        return self.__delta
    
    @delta.setter
    def delta(self, value: float) -> None:
        if value < 0.2:
            self.__delta = value
    
    #########################################################
    # Calculated
    #########################################################

    @property
    def quaternion1e(self) -> Quaternion:
        return self.__quaternion1e
    
    def set_quaternion1e(self) -> None:

        # y1
        y1 = copy(self.y0)
        q_y = quaternion.fromAxisAngle(y1, self.theta2e)

        # x1
        x1 = quaternion.rotate(q_y, self.x0)
        q_x = quaternion.fromAxisAngle(x1, self.theta1e)

        # Add rotation
        q_yx = quaternion.multiply(q_x, q_y)

        # z1
        z1 = quaternion.rotate(q_yx, self.x0)
        q_z = quaternion.fromAxisAngle(z1, self.theta3e)

        # Add rotation
        q_yxz = quaternion.multiply(q_z, q_yx)

        self.__quaternion1e = q_yxz

    
    @property
    def x1e(self) -> Vector:
        return quaternion.rotate(self.quaternion1e, self.x0)
    
    @property
    def y1e(self) -> Vector:
        return quaternion.rotate(self.quaternion1e, self.y0)
    
    @property
    def z1e(self) -> Vector:
        return quaternion.rotate(self.quaternion1e, self.z0)
    
    #-------------------------------------#
    @property
    def quaternionBase2e(self) -> Quaternion:
        return self.__quaternionBase2e
    
    def set_quaternionBase2e(self) -> None:

        # z2
        z2 = self.z1e
        q_z = quaternion.fromAxisAngle(z2, self.theta5e)

        # Add rotation
        q_yxz_z = quaternion.multiply(q_z, self.quaternion1e)

        self.__quaternionBase2e = q_yxz_z
    
    @property
    def xBase2e(self) -> Vector:
        return quaternion.rotate(self.quaternionBase2e, self.x0)
    
    @property
    def yBase2e(self) -> Vector:
        return quaternion.rotate(self.quaternionBase2e, self.y0)
    
    @property
    def zBase2e(self) -> Vector:
        return quaternion.rotate(self.quaternionBase2e, self.z0)
    
    #-------------------------------------#
    @property
    def quaternionTip2e(self) -> Quaternion:
        return self.__quaternionTip2e
    
    def set_quaternionTip2e(self) -> None:

        # z2
        y2 = self.yBase2e
        q_y = quaternion.fromAxisAngle(y2, self.theta4e)

        # Add rotation
        q_yxz_zy = quaternion.multiply(q_y, self.quaternionBase2e)

        self.__quaternionTip2e = q_yxz_zy        
    
    @property
    def xTip2e(self) -> Vector:
        return quaternion.rotate(self.quaternionTip2e, self.x0)
    
    @property
    def yTip2e(self) -> Vector:
        return quaternion.rotate(self.quaternionTip2e, self.y0)
    
    @property
    def zTip2e(self) -> Vector:
        return quaternion.rotate(self.quaternionTip2e, self.z0)
    
    #-------------------------------------#
    @property
    def quaternion3e(self) -> Quaternion:
        return self.__quaternion3e
    
    def set_quaternion3e(self) -> None:

        # z3
        x3 = self.xTip2e
        q_x = quaternion.fromAxisAngle(x3, self.theta6e)

        # Add rotation
        q_yxz_zy_x = quaternion.multiply(q_x, self.quaternionTip2e)

        # x3
        z3 = quaternion.rotate(q_yxz_zy_x, self.z0)
        q_z = quaternion.fromAxisAngle(z3, self.theta7e)

        # Add rotation
        q_yxz_zy_xz = quaternion.multiply(q_z, q_yxz_zy_x)

        self.__quaternion3e = q_yxz_zy_xz
    
    @property
    def x3e(self) -> Vector:
        return quaternion.rotate(self.quaternion3e, self.x0)
    
    @property
    def y3e(self) -> Vector:
        return quaternion.rotate(self.quaternion3e, self.y0)
    
    @property
    def z3e(self) -> Vector:
        return quaternion.rotate(self.quaternion3e, self.z0)
    
    #-------------------------------------#
    @property
    def delta7(self) -> float:
        return self.__delta7
    
    @delta7.setter
    def delta7(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta7 = value
    
    #-------------------------------------#
    @property
    def delta8(self) -> float:
        return self.__delta8
    
    @delta.setter
    def delta8(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta8 = value
    
    #-------------------------------------#
    @property
    def delta9(self) -> float:
        return self.__delta9
    
    @delta9.setter
    def delta9(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta9 = value
    
    #-------------------------------------#
    @property
    def delta10(self) -> float:
        return self.__delta10
    
    @delta10.setter
    def delta10(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta10 = value
    
    #-------------------------------------#
    @property
    def delta11(self) -> float:
        return self.__delta11
    
    @delta11.setter
    def delta11(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta11 = value
    
    #-------------------------------------#
    @property
    def delta12(self) -> float:
        return self.__delta12
    
    @delta12.setter
    def delta12(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta12 = value
    
    #-------------------------------------#
    @property
    def delta13(self) -> float:
        return self.__delta13
    
    @delta13.setter
    def delta13(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta13 = value
    
    #-------------------------------------#
    @property
    def delta14(self) -> float:
        return self.__delta14
    
    @delta14.setter
    def delta14(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta14 = value
    
    #-------------------------------------#
    @property
    def delta15(self) -> float:
        return self.__delta15
    
    @delta15.setter
    def delta15(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta15 = value
    
    #-------------------------------------#
    @property
    def delta16(self) -> float:
        return self.__delta16
    
    @delta16.setter
    def delta16(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta16 = value
    
    #-------------------------------------#
    @property
    def delta17(self) -> float:
        return self.__delta17
    
    @delta17.setter
    def delta17(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta17 = value
    
    #-------------------------------------#
    @property
    def delta18(self) -> float:
        return self.__delta18
    
    @delta18.setter
    def delta18(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta18 = value
    
    #-------------------------------------#
    @property
    def delta19(self) -> float:
        return self.__delta19
    
    @delta19.setter
    def delta19(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta19 = value
    
    #-------------------------------------#
    @property
    def delta20(self) -> float:
        return self.__delta20
    
    @delta20.setter
    def delta20(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta20 = value
    
    #-------------------------------------#
    @property
    def delta21(self) -> float:
        return self.__delta21
    
    @delta21.setter
    def delta21(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta21 = value
    
    #-------------------------------------#
    @property
    def delta22(self) -> float:
        return self.__delta22
    
    @delta22.setter
    def delta22(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta22 = value
    
    #-------------------------------------#
    @property
    def delta23(self) -> float:
        return self.__delta23
    
    @delta23.setter
    def delta23(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta23 = value
    
    #-------------------------------------#
    @property
    def delta24(self) -> float:
        return self.__delta24
    
    @delta24.setter
    def delta24(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta24 = value
    
    #-------------------------------------#
    @property
    def delta25(self) -> float:
        return self.__delta25
    
    @delta25.setter
    def delta25(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta25 = value
    
    #-------------------------------------#
    @property
    def delta26(self) -> float:
        return self.__delta26
    
    @delta26.setter
    def delta26(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta26 = value
    
    #-------------------------------------#
    @property
    def delta27(self) -> float:
        return self.__delta27
    
    @delta27.setter
    def delta27(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta27 = value
    
    #-------------------------------------#
    @property
    def delta28(self) -> float:
        return self.__delta28
    
    @delta28.setter
    def delta28(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta28 = value
    
    #-------------------------------------#
    @property
    def delta29(self) -> float:
        return self.__delta29
    
    @delta29.setter
    def delta29(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta29 = value
    
    #-------------------------------------#
    @property
    def delta30(self) -> float:
        return self.__delta30
    
    @delta30.setter
    def delta30(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta30 = value
    
    #-------------------------------------#
    @property
    def delta31(self) -> float:
        return self.__delta31
    
    @delta31.setter
    def delta31(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta31 = value
    
    #-------------------------------------#
    @property
    def delta32(self) -> float:
        return self.__delta32
    
    @delta32.setter
    def delta32(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta32 = value
    
    #-------------------------------------#
    @property
    def delta33(self) -> float:
        return self.__delta33
    
    @delta33.setter
    def delta33(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta33 = value
    
    #-------------------------------------#
    @property
    def delta34(self) -> float:
        return self.__delta34
    
    @delta34.setter
    def delta34(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta34 = value
    
    #-------------------------------------#
    @property
    def delta35(self) -> float:
        return self.__delta35
    
    @delta35.setter
    def delta35(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta35 = value
    
    #-------------------------------------#
    @property
    def delta36(self) -> float:
        return self.__delta36
    
    @delta36.setter
    def delta36(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta36 = value
    
    #-------------------------------------#
    @property
    def delta37(self) -> float:
        return self.__delta37
    
    @delta37.setter
    def delta37(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta37 = value
    
    #-------------------------------------#
    @property
    def delta38(self) -> float:
        return self.__delta38
    
    @delta38.setter
    def delta38(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta38 = value
    
    #-------------------------------------#
    @property
    def delta39(self) -> float:
        return self.__delta39
    
    @delta39.setter
    def delta39(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta39 = value
    
    #-------------------------------------#
    @property
    def delta40(self) -> float:
        return self.__delta40
    
    @delta40.setter
    def delta40(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta40 = value
    
    #-------------------------------------#
    @property
    def delta41(self) -> float:
        return self.__delta41
    
    @delta41.setter
    def delta41(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta41 = value
    
    #-------------------------------------#
    @property
    def delta42(self) -> float:
        return self.__delta42
    
    @delta42.setter
    def delta42(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta42 = value
    
    #-------------------------------------#
    @property
    def delta43(self) -> float:
        return self.__delta43
    
    @delta43.setter
    def delta43(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta43 = value
    
    #-------------------------------------#
    @property
    def delta44(self) -> float:
        return self.__delta44
    
    @delta44.setter
    def delta44(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta44 = value
    
    #-------------------------------------#
    @property
    def delta45(self) -> float:
        return self.__delta45
    
    @delta45.setter
    def delta45(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta45 = value
    
    #-------------------------------------#
    @property
    def delta46(self) -> float:
        return self.__delta46
    
    @delta46.setter
    def delta46(self, value: float) -> None:
        if 0 <= value <= 1: self.__delta46 = value
    
    #-------------------------------------#
    @property
    def h8(self) -> float:
        return self.__h8
    
    @h8.setter
    def h8(self, value: float) -> None:
        if 0 < value < 1: self.__h8 = value
    
    #-------------------------------------#
    @property
    def h9(self) -> float:
        return self.__h9
    
    @h9.setter
    def h9(self, value: float) -> None:
        if 0 < value < 1: self.__h9 = value
    
    #-------------------------------------#
    @property
    def h10(self) -> float:
        return self.__h10
    
    @h10.setter
    def h10(self, value: float) -> None:
        if 0 < value < 1: self.__h10 = value
    
    #-------------------------------------#
    @property
    def h11(self) -> float:
        return self.__h11
    
    @h11.setter
    def h11(self, value: float) -> None:
        if 0 < value < 1: self.__h11 = value
    
    #-------------------------------------#
    @property
    def h12(self) -> float:
        return self.__h12
    
    @h12.setter
    def h12(self, value: float) -> None:
        if 0 < value < 1: self.__h12 = value
    
    #-------------------------------------#
    @property
    def h13(self) -> float:
        return self.__h13
    
    @h13.setter
    def h13(self, value: float) -> None:
        if 0 < value < 1: self.__h13 = value
    
    #-------------------------------------#
    @property
    def h14(self) -> float:
        return self.__h14
    
    @h14.setter
    def h14(self, value: float) -> None:
        if 0 < value < 1: self.__h14 = value
    
    #-------------------------------------#
    @property
    def h15(self) -> float:
        return self.__h15
    
    @h15.setter
    def h15(self, value: float) -> None:
        if 0 < value < 1: self.__h15 = value
    
    #-------------------------------------#
    @property
    def h16(self) -> float:
        return self.__h16
    
    @h16.setter
    def h16(self, value: float) -> None:
        if 0 < value < 1: self.__h16 = value
    
    #-------------------------------------#
    @property
    def h17(self) -> float:
        return self.__h17
    
    @h17.setter
    def h17(self, value: float) -> None:
        if 0 < value < 1: self.__h17 = value
    
    #-------------------------------------#
    @property
    def h18(self) -> float:
        return self.__h18
    
    @h18.setter
    def h18(self, value: float) -> None:
        if 0 < value < 1: self.__h18 = value
    
    #-------------------------------------#
    @property
    def h19(self) -> float:
        return self.__h19
    
    @h19.setter
    def h19(self, value: float) -> None:
        if 0 < value < 1: self.__h19 = value
    
    #-------------------------------------#
    @property
    def h20(self) -> float:
        return self.__h20
    
    @h20.setter
    def h20(self, value: float) -> None:
        if 0 < value < 1: self.__h20 = value
    
    #-------------------------------------#
    @property
    def h21(self) -> float:
        return self.__h21
    
    @h21.setter
    def h21(self, value: float) -> None:
        if 0 < value < 1: self.__h21 = value
    
    #-------------------------------------#
    @property
    def delta47(self) -> float:
        return self.__delta47
    
    @delta47.setter
    def delta47(self, value: float) -> None:
        if value > 0: self.__delta47 = value
    
    #-------------------------------------#
    @property
    def delta48(self) -> float:
        return self.__delta48
    
    @delta48.setter
    def delta48(self, value: float) -> None:
        if 0 < value < 1: self.__delta48 = value
    
    #-------------------------------------#
    @property
    def theta8(self) -> float:
        return self.__theta8
    
    @theta8.setter
    def theta8(self, value: float) -> None:
        if -30 <= value < 30: self.__theta8 = value
    
    #-------------------------------------#
    @property
    def theta9(self) -> float:
        return self.__theta9
    
    @theta9.setter
    def theta9(self, value: float) -> None:
        if -30 <= value < 30: self.__theta9 = value
    
    #-------------------------------------#
    @property
    def theta10(self) -> float:
        return self.__theta10
    
    @theta10.setter
    def theta10(self, value: float) -> None:
        if -30 <= value < 30: self.__theta10 = value
    
    #-------------------------------------#
    @property
    def tailAirfoil(self) -> Curve:
        return self.__tailAirfoil
    
    @tailAirfoil.setter
    def tailAirfoil(self, value: Curve) -> None:
        if value is not None and value.shape[1] == 2 and value.shape[0] >= 5:
            self.__tailAirfoil = value
        else:
            self.__tailAirfoil = None