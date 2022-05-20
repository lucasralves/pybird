from numpy import array, copy

from pybird.helpers.type import Curve, Quaternion, Vector
from pybird.helpers import quaternion

class Data:

    def __init__(self) -> None:
        
        # Wing
        self.l0 = 0.08
        self.l1 = 0.15
        self.l2 = 0.3
        self.l3 = 0.2
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
        self.h15 = 0.03
        self.h16 = 0.06
        self.h17 = 0.1
        self.h18 = 0.1
        self.delta7 = .1
        self.delta8 = .1
        self.delta9 = .1
        self.delta10 = .1
        self.delta11 = .1
        self.delta12 = .1
        self.delta13 = .1
        self.delta14 = .1
        self.delta15 = .1
        self.delta16 = .1
        self.delta17 = .1
        self.delta18 = .1
        self.delta19 = .1
        self.delta20 = .1
        self.delta21 = .1
        self.delta22 = .1
        self.delta23 = .1
        self.delta24 = .1
        self.delta25 = .1
        self.delta26 = .1
        self.delta27 = .1
        self.delta28 = .1
        self.delta29 = .1
        self.delta30 = .1
        self.delta31 = .1
        self.delta32 = .1
        self.delta33 = .1
        self.delta34 = .1
        self.delta35 = .1
        self.delta36 = .1
        self.delta37 = .1
        self.delta38 = .1
        self.delta39 = .5
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

        # Tail
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
        if -70 < value < 70: self.__theta0 = value
    
    #-------------------------------------#
    @property
    def theta1e(self) -> float:
        return self.__theta1e
    
    @theta1e.setter
    def theta1e(self, value: float) -> None:
        if -70 < value < 70: self.__theta1e = value
    
    #-------------------------------------#
    @property
    def theta2e(self) -> float:
        return self.__theta2e
    
    @theta2e.setter
    def theta2e(self, value: float) -> None:
        if -20 < value < 20: self.__theta2e = value
    
    #-------------------------------------#
    @property
    def theta3e(self) -> float:
        return self.__theta3e
    
    @theta3e.setter
    def theta3e(self, value: float) -> None:
        if -45 < value < 45: self.__theta3e = value
    
    #-------------------------------------#
    @property
    def theta4e(self) -> float:
        return self.__theta4e
    
    @theta4e.setter
    def theta4e(self, value: float) -> None:
        if -45 < value < 45: self.__theta4e = value
    
    #-------------------------------------#
    @property
    def theta5e(self) -> float:
        return self.__theta5e
    
    @theta5e.setter
    def theta5e(self, value: float) -> None:
        if 0 <= value < 45: self.__theta5e = value
    
    #-------------------------------------#
    @property
    def theta6e(self) -> float:
        return self.__theta6e
    
    @theta6e.setter
    def theta6e(self, value: float) -> None:
        if -45 < value < 60: self.__theta6e = value
    
    #-------------------------------------#
    @property
    def theta7e(self) -> float:
        return self.__theta7e
    
    @theta7e.setter
    def theta7e(self, value: float) -> None:
        if -45 < value < 60: self.__theta7e = value
    
    #-------------------------------------#
    @property
    def theta1d(self) -> float:
        return self.__theta1d
    
    @theta1d.setter
    def theta1d(self, value: float) -> None:
        if -70 < value < 70: self.__theta1d = value
    
    #-------------------------------------#
    @property
    def theta2d(self) -> float:
        return self.__theta2d
    
    @theta2d.setter
    def theta2d(self, value: float) -> None:
        if -20 < value < 20: self.__theta2d = value
    
    #-------------------------------------#
    @property
    def theta3d(self) -> float:
        return self.__theta3d
    
    @theta3d.setter
    def theta3d(self, value: float) -> None:
        if -45 < value < 45: self.__theta3d = value
    
    #-------------------------------------#
    @property
    def theta4d(self) -> float:
        return self.__theta4d
    
    @theta4d.setter
    def theta4d(self, value: float) -> None:
        if -45 < value < 45: self.__theta4d = value
    
    #-------------------------------------#
    @property
    def theta5d(self) -> float:
        return self.__theta5d
    
    @theta5d.setter
    def theta5d(self, value: float) -> None:
        if 0 <= value < 45: self.__theta5d = value
    
    #-------------------------------------#
    @property
    def theta6d(self) -> float:
        return self.__theta6d
    
    @theta6d.setter
    def theta6d(self, value: float) -> None:
        if -45 < value < 60: self.__theta6d = value
    
    #-------------------------------------#
    @property
    def theta7d(self) -> float:
        return self.__theta7d
    
    @theta7d.setter
    def theta7d(self, value: float) -> None:
        if -45 < value < 60: self.__theta7d = value
    
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
        if 0 <= value < 60: self.__theta8 = value
    
    #-------------------------------------#
    @property
    def theta9(self) -> float:
        return self.__theta9
    
    @theta9.setter
    def theta9(self, value: float) -> None:
        if 0 <= value < 60: self.__theta9 = value
    
    #-------------------------------------#
    @property
    def theta10(self) -> float:
        return self.__theta10
    
    @theta10.setter
    def theta10(self, value: float) -> None:
        if 0 <= value < 60: self.__theta10 = value