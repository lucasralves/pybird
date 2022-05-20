from math import acos

from numpy import argmin, flip, zeros

from pybird.geometry.utilities.data import Data
from pybird.helpers.type import Curve, Quaternion, Vector
from pybird.helpers import quaternion
from pybird.helpers import vector
from pybird.helpers import curve


class WingFinalParams:

    def __init__(self, data: Data) -> None:
        self.__data = data
        self.update()
    
    def update(self) -> None:
        self.calcQuaternion1e()
        self.calcX1e()
        self.calcY1e()
        self.calcZ1e()

        self.calcQuaternionBase2e()
        self.calcXBase2e()
        self.calcYBase2e()
        self.calcZBase2e()

        self.calcQuaternionTip2e()
        self.calcXTip2e()
        self.calcYTip2e()
        self.calcZTip2e()

        self.calcQuaternion3e()
        self.calcX3e()
        self.calcY3e()
        self.calcZ3e()

        self.calcP0e()
        self.calcP1e()
        self.calcP3e()
        self.calcP3eLine()
        self.calcP4e()
        self.calcP5e()
        self.calcP6e()
        self.calcP7e()
        self.calcP8e()
        self.calcC1e()
        self.calcP2e()
        self.calcC2e()
        self.calcC4e()
        self.calcC3e()
        self.calcC5e()
        self.calcC6e()
        self.calcC7e()
        self.calcC8e()

        self.calcCurve1e()
        self.calcCurve2e()
        self.calcCurve3e()
        self.calcCurve4e()
        self.calcCurve5e()
        self.calcCurve6e()

        self.calcRootFoilE()
        self.calcMiddle1FoilE()
        self.calcMiddle2FoilE()
        self.calcTipFoilE()

        #-----------------------------------#
        self.calcQuaternion1d()
        self.calcX1d()
        self.calcY1d()
        self.calcZ1d()

        self.calcQuaternionBase2d()
        self.calcXBase2d()
        self.calcYBase2d()
        self.calcZBase2d()

        self.calcQuaternionTip2d()
        self.calcXTip2d()
        self.calcYTip2d()
        self.calcZTip2d()

        self.calcQuaternion3d()
        self.calcX3d()
        self.calcY3d()
        self.calcZ3d()

        self.calcP0d()
        self.calcP1d()
        self.calcP3d()
        self.calcP3dLine()
        self.calcP4d()
        self.calcP5d()
        self.calcP6d()
        self.calcP7d()
        self.calcP8d()
        self.calcC1d()
        self.calcP2d()
        self.calcC2d()
        self.calcC4d()
        self.calcC3d()
        self.calcC5d()
        self.calcC6d()
        self.calcC7d()
        self.calcC8d()

        self.calcCurve1d()
        self.calcCurve2d()
        self.calcCurve3d()
        self.calcCurve4d()
        self.calcCurve5d()
        self.calcCurve6d()

        self.calcRootFoilD()
        self.calcMiddle1FoilD()
        self.calcMiddle2FoilD()
        self.calcTipFoilD()
    
    #########################################################
    # Quaternions
    #########################################################

    #-------------------------------------#
    @property
    def quaternion1e(self) -> Quaternion:
        return self.__quaternion1e
    
    @quaternion1e.setter
    def quaternion1e(self, value: Quaternion) -> None:
        self.__quaternion1e = value
    
    def calcQuaternion1e(self) -> None:
        
        # Quaternion around -y
        q_y = quaternion.fromAxisAngle(-self.__data.y0, self.__data.theta2e)

        # Rotate x axis
        x1 = quaternion.rotate(q_y, self.__data.x0)

        # Quaternion around x
        q_x = quaternion.fromAxisAngle(x1, self.__data.theta1e)

        # Multiply rotation
        q_yx = quaternion.multiply(q_x, q_y)

        # Rotate z axis
        z1 = quaternion.rotate(q_yx, self.__data.z0)

        # Quaternion around z
        q_z = quaternion.fromAxisAngle(z1, self.__data.theta3e)

        # Multiply rotation
        q_yxz = quaternion.multiply(q_z, q_yx)

        # Save quaternion
        self.quaternion1e = q_yxz
    
    #-------------------------------------#
    @property
    def quaternionBase2e(self) -> Quaternion:
        return self.__quaternionBase2e
    
    @quaternionBase2e.setter
    def quaternionBase2e(self, value: Quaternion) -> None:
        self.__quaternionBase2e = value
    
    def calcQuaternionBase2e(self) -> None:
        
        # Quaternion around -z
        q_z = quaternion.fromAxisAngle(-self.z1e, self.__data.theta5e)

        # Multiply rotation
        q_yxz_z = quaternion.multiply(q_z, self.quaternion1e)

        # Save quaternion
        self.quaternionBase2e = q_yxz_z
    
    #-------------------------------------#
    @property
    def quaternionTip2e(self) -> Quaternion:
        return self.__quaternionTip2e
    
    @quaternionTip2e.setter
    def quaternionTip2e(self, value: Quaternion) -> None:
        self.__quaternionTip2e = value
    
    def calcQuaternionTip2e(self) -> None:
        
        # Quaternion around -y
        q_y = quaternion.fromAxisAngle(-self.yBase2e, self.__data.theta4e)

        # Multiply rotation
        q_yxz_zy = quaternion.multiply(q_y, self.quaternionBase2e)

        # Save quaternion
        self.quaternionTip2e = q_yxz_zy
    
    #-------------------------------------#
    @property
    def quaternion3e(self) -> Quaternion:
        return self.__quaternion3e
    
    @quaternion3e.setter
    def quaternion3e(self, value: Quaternion) -> None:
        self.__quaternion3e = value
    
    def calcQuaternion3e(self) -> None:
        
        # Quaternion around -x
        q_x = quaternion.fromAxisAngle(-self.xTip2e, self.__data.theta6e)

        # Multiply rotation
        q_yxz_zy_x = quaternion.multiply(q_x, self.quaternionTip2e)

        # Rotate z axis
        z3 = quaternion.rotate(q_yxz_zy_x, self.__data.z0)

        # Quaternion around z
        q_z = quaternion.fromAxisAngle(z3, self.__data.theta7e)

        # Multiply rotation
        q_yxz_zy_xz = quaternion.multiply(q_z, q_yxz_zy_x)

        # Save quaternion
        self.quaternion3e = q_yxz_zy_xz
    
    #########################################################
    # Base vectors
    #########################################################

    #-------------------------------------#
    @property
    def x1e(self) -> Vector:
        return self.__x1e
    
    @x1e.setter
    def x1e(self, value: Vector) -> None:
        self.__x1e = value
    
    def calcX1e(self) -> None:
        self.x1e = quaternion.rotate(self.quaternion1e, self.__data.x0)
    
    @property
    def y1e(self) -> Vector:
        return self.__y1e
    
    @y1e.setter
    def y1e(self, value: Vector) -> None:
        self.__y1e = value
    
    def calcY1e(self) -> None:
        self.y1e = quaternion.rotate(self.quaternion1e, self.__data.y0)
    
    @property
    def z1e(self) -> Vector:
        return self.__z1e
    
    @z1e.setter
    def z1e(self, value: Vector) -> None:
        self.__z1e = value
    
    def calcZ1e(self) -> None:
        self.z1e = quaternion.rotate(self.quaternion1e, self.__data.z0)
    
    #-------------------------------------#
    @property
    def xBase2e(self) -> Vector:
        return self.__xBase2e
    
    @xBase2e.setter
    def xBase2e(self, value: Vector) -> None:
        self.__xBase2e = value
    
    def calcXBase2e(self) -> None:
        self.xBase2e = quaternion.rotate(self.quaternionBase2e, self.__data.x0)
    
    @property
    def yBase2e(self) -> Vector:
        return self.__yBase2e
    
    @yBase2e.setter
    def yBase2e(self, value: Vector) -> None:
        self.__yBase2e = value
    
    def calcYBase2e(self) -> None:
        self.yBase2e = quaternion.rotate(self.quaternionBase2e, self.__data.y0)
    
    @property
    def zBase2e(self) -> Vector:
        return self.__zBase2e
    
    @zBase2e.setter
    def zBase2e(self, value: Vector) -> None:
        self.__zBase2e = value
    
    def calcZBase2e(self) -> None:
        self.zBase2e = quaternion.rotate(self.quaternionBase2e, self.__data.z0)
    
    #-------------------------------------#
    @property
    def xTip2e(self) -> Vector:
        return self.__xTip2e
    
    @xTip2e.setter
    def xTip2e(self, value: Vector) -> None:
        self.__xTip2e = value
    
    def calcXTip2e(self) -> None:
        self.xTip2e = quaternion.rotate(self.quaternionTip2e, self.__data.x0)
    
    @property
    def yTip2e(self) -> Vector:
        return self.__yTip2e
    
    @yTip2e.setter
    def yTip2e(self, value: Vector) -> None:
        self.__yTip2e = value
    
    def calcYTip2e(self) -> None:
        self.yTip2e = quaternion.rotate(self.quaternionTip2e, self.__data.y0)
    
    @property
    def zTip2e(self) -> Vector:
        return self.__zTip2e
    
    @zTip2e.setter
    def zTip2e(self, value: Vector) -> None:
        self.__zTip2e = value
    
    def calcZTip2e(self) -> None:
        self.zTip2e = quaternion.rotate(self.quaternionTip2e, self.__data.z0)
    
    #-------------------------------------#
    @property
    def x3e(self) -> Vector:
        return self.__x3e
    
    @x3e.setter
    def x3e(self, value: Vector) -> None:
        self.__x3e = value
    
    def calcX3e(self) -> None:
        self.x3e = quaternion.rotate(self.quaternion3e, self.__data.x0)
    
    @property
    def y3e(self) -> Vector:
        return self.__y3e
    
    @y3e.setter
    def y3e(self, value: Vector) -> None:
        self.__y3e = value
    
    def calcY3e(self) -> None:
        self.y3e = quaternion.rotate(self.quaternion3e, self.__data.y0)
    
    @property
    def z3e(self) -> Vector:
        return self.__z3e
    
    @z3e.setter
    def z3e(self, value: Vector) -> None:
        self.__z3e = value
    
    def calcZ3e(self) -> None:
        self.z3e = quaternion.rotate(self.quaternion3e, self.__data.z0)
    
    #########################################################
    # Control points
    #########################################################

    #-------------------------------------#
    @property
    def p0e(self) -> Vector:
        return self.__p0e
    
    @p0e.setter
    def p0e(self, value: Vector) -> None:
        self.__p0e = value
    
    def calcP0e(self) -> None:
        self.p0e = self.__data.l0 * self.__data.y0
    
    #-------------------------------------#
    @property
    def p1e(self) -> Vector:
        return self.__p1e
    
    @p1e.setter
    def p1e(self, value: Vector) -> None:
        self.__p1e = value
    
    def calcP1e(self) -> None:
        q_z = quaternion.fromAxisAngle(self.__data.z0, self.__data.theta0)
        q_y = quaternion.fromAxisAngle(-self.__data.y0, self.__data.theta2e)
        v = self.__data.h1 * self.__data.x0
        self.p1e = self.p0e + quaternion.rotate(q_y, quaternion.rotate(q_z, v))
    
    #-------------------------------------#
    @property
    def p3e(self) -> Vector:
        return self.__p3e
    
    @p3e.setter
    def p3e(self, value: Vector) -> None:
        self.__p3e = value
    
    def calcP3e(self) -> None:
        self.p3e = self.p0e + self.__data.l1 * self.y1e + (self.__data.l2 - self.__data.h2) * self.yBase2e + self.__data.h3 * self.xTip2e
    
    #-------------------------------------#
    @property
    def p3eLine(self) -> Vector:
        return self.__p3eLine
    
    @p3eLine.setter
    def p3eLine(self, value: Vector) -> None:
        self.__p3eLine = value
    
    def calcP3eLine(self) -> None:
        self.p3eLine = self.p0e + self.__data.l1 * self.y1e + (self.__data.l2 - self.__data.h2) * self.yBase2e + self.__data.h3 * self.xBase2e
    
    #-------------------------------------#
    @property
    def p4e(self) -> Vector:
        return self.__p4e
    
    @p4e.setter
    def p4e(self, value: Vector) -> None:
        self.__p4e = value
    
    def calcP4e(self) -> None:
        self.p4e = self.p0e + self.__data.l1 * self.y1e + self.__data.l2 * self.yBase2e + self.__data.h2 * self.y3e + self.__data.h3 * self.x3e
    
    #-------------------------------------#
    @property
    def p5e(self) -> Vector:
        return self.__p5e
    
    @p5e.setter
    def p5e(self, value: Vector) -> None:
        self.__p5e = value
    
    def calcP5e(self) -> None:
        self.p5e = self.p4e + (self.__data.l3 - self.__data.h2) * self.y3e
    
    #-------------------------------------#
    @property
    def p6e(self) -> Vector:
        return self.__p6e
    
    @p6e.setter
    def p6e(self, value: Vector) -> None:
        self.__p6e = value
    
    def calcP6e(self) -> None:
        self.p6e = self.p5e - self.__data.h4 * self.x3e + self.__data.h5 * self.y3e
    
    #-------------------------------------#
    @property
    def p7e(self) -> Vector:
        return self.__p7e
    
    @p7e.setter
    def p7e(self, value: Vector) -> None:
        self.__p7e = value
    
    def calcP7e(self) -> None:
        self.p7e = self.p0e + self.__data.l1 * self.y1e + self.__data.l2 * self.yTip2e - self.__data.h6 * vector.unary(self.xTip2e + self.x3e)
    
    #-------------------------------------#
    @property
    def p8e(self) -> Vector:
        return self.__p8e
    
    @p8e.setter
    def p8e(self, value: Vector) -> None:
        self.__p8e = value
    
    def calcP8e(self) -> None:
        q_z = quaternion.fromAxisAngle(self.__data.z0, self.__data.theta0)
        q_y = quaternion.fromAxisAngle(-self.__data.y0, self.__data.theta2e)
        v = - self.__data.h7 * self.__data.x0
        self.p8e = self.p0e + quaternion.rotate(q_y, quaternion.rotate(q_z, v))
    
    #-------------------------------------#
    @property
    def c1e(self) -> Vector:
        return self.__c1e
    
    @c1e.setter
    def c1e(self, value: Vector) -> None:
        self.__c1e = value
    
    def calcC1e(self) -> None:
        p = self.p0e + self.__data.l1 * self.y1e
        dist = vector.norm(vector.cross(p - self.p1e, p - self.p3e)) / vector.norm(self.p3e - self.p1e)
        self.c1e = self.p0e + self.__data.l1 * self.y1e + self.__data.delta1 * dist * vector.unary(self.x1e + self.xBase2e)
    
    #-------------------------------------#
    @property
    def p2e(self) -> Vector:
        return self.__p2e
    
    @p2e.setter
    def p2e(self, value: Vector) -> None:
        self.__p2e = value
    
    def calcP2e(self) -> None:
        self.p2e = 0.25 * self.p1e + 0.5 * self.c1e + 0.25 * self.p3eLine
    
    #-------------------------------------#
    @property
    def c2e(self) -> Vector:
        return self.__c2e
    
    @c2e.setter
    def c2e(self, value: Vector) -> None:
        self.__c2e = value
    
    def calcC2e(self) -> None:
        self.c2e = self.p2e + self.__data.epsilon1 * vector.dot(self.p3e - self.p2e, vector.unary(self.p3e - self.p1e)) * vector.unary(self.p3e - self.p1e)
    
    #-------------------------------------#
    @property
    def c4e(self) -> Vector:
        return self.__c4e
    
    @c4e.setter
    def c4e(self, value: Vector) -> None:
        self.__c4e = value
    
    def calcC4e(self) -> None:
        c = vector.dot(-self.yTip2e, self.y3e)
        self.c4e = self.p3e + self.__data.epsilon3 * self.__data.h2 * (1 + acos(c if -1 <= c <= 1 else 1 if c > 1 else -1)) * self.yTip2e
    
    #-------------------------------------#
    @property
    def c3e(self) -> Vector:
        return self.__c3e
    
    @c3e.setter
    def c3e(self, value: Vector) -> None:
        self.__c3e = value
    
    def calcC3e(self) -> None:
        self.c3e = self.p3e + self.__data.epsilon2 * vector.dot(self.p2e - self.p3e, vector.unary(self.p3e - self.c4e)) * vector.unary(self.p3e - self.c4e)
    
    #-------------------------------------#
    @property
    def c5e(self) -> Vector:
        return self.__c5e
    
    @c5e.setter
    def c5e(self, value: Vector) -> None:
        self.__c5e = value
    
    def calcC5e(self) -> None:
        c = vector.dot(-self.yTip2e, self.y3e)
        self.c5e = self.p4e - self.__data.epsilon3 * self.__data.h2 * (1 + acos(c if -1 <= c <= 1 else 1 if c > 1 else -1)) * self.y3e
    
    #-------------------------------------#
    @property
    def c6e(self) -> Vector:
        return self.__c6e
    
    @c6e.setter
    def c6e(self, value: Vector) -> None:
        self.__c6e = value
    
    def calcC6e(self) -> None:
        self.c6e = self.p5e + self.__data.delta2 * (vector.dot(self.y3e, self.p6e - self.p5e)) * self.y3e
    
    #-------------------------------------#
    @property
    def c7e(self) -> Vector:
        return self.__c7e
    
    @c7e.setter
    def c7e(self, value: Vector) -> None:
        self.__c7e = value
    
    def calcC7e(self) -> None:
        self.c7e = 0.5 * (self.p6e + self.p7e) + 0.5 * self.__data.delta3 * (self.p6e - self.p7e) + 0.5 * self.__data.delta4 * vector.cross(self.z3e, self.p6e - self.p7e)
    
    #-------------------------------------#
    @property
    def c8e(self) -> Vector:
        return self.__c8e
    
    @c8e.setter
    def c8e(self, value: Vector) -> None:
        self.__c8e = value
    
    def calcC8e(self) -> None:
        self.c8e = 0.5 * (self.p7e + self.p8e) + 0.5 * self.__data.delta5 * (self.p7e - self.p8e) + self.__data.delta6 * vector.norm(self.p7e - self.p8e) * vector.unary(vector.cross(self.zTip2e + self.zBase2e, self.p7e - self.p8e))

    #########################################################
    # Curves
    #########################################################

    #-------------------------------------#
    @property
    def curve1e(self) -> Curve:
        return self.__curve1e
    
    @curve1e.setter
    def curve1e(self, value: Curve) -> None:
        self.__curve1e = value
    
    def calcCurve1e(self) -> None:
        
        n = 100
        n_2 = int(0.5 * n)

        curve_aux_1 = curve.bezier([self.p1e, self.c1e, self.p3eLine], n=n)
        curve_aux_2 = curve.bezier([self.p2e, self.c2e, self.c3e, self.p3e], n=n_2)

        out = zeros((n, 3))

        for i in range(n):
            out[i, :] = curve_aux_1[i, :] if i < n_2 else curve_aux_2[i - n_2, :]
        
        self.curve1e = out
    
    #-------------------------------------#
    @property
    def curve2e(self) -> Curve:
        return self.__curve2e
    
    @curve2e.setter
    def curve2e(self, value: Curve) -> None:
        self.__curve2e = value
    
    def calcCurve2e(self) -> None:
        n = 100
        self.curve2e = curve.bezier([self.p3e, self.c4e, self.c5e, self.p4e], n=n)
    
    #-------------------------------------#
    @property
    def curve3e(self) -> Curve:
        return self.__curve3e
    
    @curve3e.setter
    def curve3e(self, value: Curve) -> None:
        self.__curve3e = value
    
    def calcCurve3e(self) -> None:
        n = 200
        self.curve3e = curve.line([self.p4e, self.p5e], n=n)
    
    #-------------------------------------#
    @property
    def curve4e(self) -> Curve:
        return self.__curve4e
    
    @curve4e.setter
    def curve4e(self, value: Curve) -> None:
        self.__curve4e = value
    
    def calcCurve4e(self) -> None:
        n = 150
        self.curve4e = curve.bezier([self.p5e, self.c6e, self.p6e], n=n)
    
    #-------------------------------------#
    @property
    def curve5e(self) -> Curve:
        return self.__curve5e
    
    @curve5e.setter
    def curve5e(self, value: Curve) -> None:
        self.__curve5e = value
    
    def calcCurve5e(self) -> None:
        n = 100
        self.curve5e = curve.bezier([self.p6e, self.c7e, self.p7e], n=n)
    
    #-------------------------------------#
    @property
    def curve6e(self) -> Curve:
        return self.__curve6e
    
    @curve6e.setter
    def curve6e(self, value: Curve) -> None:
        self.__curve6e = value
    
    def calcCurve6e(self) -> None:
        n = 100
        self.curve6e = curve.bezier([self.p7e, self.c8e, self.p8e], n=n)
    
    #########################################################
    # Airfoils
    #########################################################

    @property
    def v1e(self) -> Vector:
        return self.curve4e[self.v1eIndex]
    
    @property
    def v1eIndex(self) -> int:
        return int((1 - self.__data.delta) * len(self.curve4e[:, 0]))
    
    #-------------------------------------#
    @property
    def v2e(self) -> Vector:
        return self.curve5e[self.v2eIndex]
    
    @property
    def v2eIndex(self) -> int:
        return int(self.__data.delta * len(self.curve4e[:, 0]))
    
    #-------------------------------------#
    @property
    def v3e(self) -> Vector:
        return self.curve5e[self.v3eIndex]
    
    @property
    def v3eIndex(self) -> int:
        return int((1 - self.__data.delta) * len(self.curve5e[:, 0]))
    
    #-------------------------------------#
    @property
    def v4e(self) -> Vector:
        return self.curve6e[self.v4eIndex]
    
    @property
    def v4eIndex(self) -> int:
        return int(self.__data.delta * len(self.curve6e[:, 0]))
    
    #-------------------------------------#
    @property
    def curve7e(self) -> Curve:
        return self.__curve7e
    
    @curve7e.setter
    def curve7e(self, value: Curve) -> None:
        self.__curve7e = value
    
    @property
    def curve8e(self) -> Curve:
        return self.__curve8e
    
    @curve8e.setter
    def curve8e(self, value: Curve) -> None:
        self.__curve8e = value
    
    def calcRootFoilE(self) -> None:
        
        if self.__data.rootAirfoil is not None:

            # Top and bottom curve
            i_max = argmin(self.__data.rootAirfoil[:, 0])
            top = self.__data.rootAirfoil[:i_max + 1, :]
            bottom = self.__data.rootAirfoil[i_max:, :]

            top = flip(top, 0)

            # Section vectors
            x = self.p8e - self.p1e
            z = self.z1e * vector.norm(x)

            # Create curves
            topFoil = zeros((len(top[:, 0]), 3))
            bottomFoil = zeros((len(bottom[:, 0]), 3))

            # Fill top curve
            topFoil[:, 0] = top[:, 0] * x[0] + top[:, 1] * z[0] + self.p1e[0]
            topFoil[:, 1] = top[:, 0] * x[1] + top[:, 1] * z[1] + self.p1e[1]
            topFoil[:, 2] = top[:, 0] * x[2] + top[:, 1] * z[2] + self.p1e[2]

            # Fill bottom curve
            bottomFoil[:, 0] = bottom[:, 0] * x[0] + bottom[:, 1] * z[0] + self.p1e[0]
            bottomFoil[:, 1] = bottom[:, 0] * x[1] + bottom[:, 1] * z[1] + self.p1e[1]
            bottomFoil[:, 2] = bottom[:, 0] * x[2] + bottom[:, 1] * z[2] + self.p1e[2]

            self.curve7e = topFoil
            self.curve8e = bottomFoil
        
        else:

            self.curve7e = zeros((1, 3))
            self.curve8e = zeros((1, 3))
    
    #-------------------------------------#
    @property
    def curve9e(self) -> Curve:
        return self.__curve9e
    
    @curve9e.setter
    def curve9e(self, value: Curve) -> None:
        self.__curve9e = value
    
    @property
    def curve10e(self) -> Curve:
        return self.__curve10e
    
    @curve10e.setter
    def curve10e(self, value: Curve) -> None:
        self.__curve10e = value
    
    def calcMiddle1FoilE(self) -> None:
        
        if self.__data.middleAirfoil is not None:

            # Top and bottom curve
            i_max = argmin(self.__data.middleAirfoil[:, 0])
            top = self.__data.middleAirfoil[:i_max + 1, :]
            bottom = self.__data.middleAirfoil[i_max:, :]

            top = flip(top, 0)

            # Section vectors
            x = self.v4e - self.p3e
            z = self.zTip2e * vector.norm(x)

            # Create curves
            topFoil = zeros((len(top[:, 0]), 3))
            bottomFoil = zeros((len(bottom[:, 0]), 3))

            # Fill top curve
            topFoil[:, 0] = top[:, 0] * x[0] + top[:, 1] * z[0] + self.p3e[0]
            topFoil[:, 1] = top[:, 0] * x[1] + top[:, 1] * z[1] + self.p3e[1]
            topFoil[:, 2] = top[:, 0] * x[2] + top[:, 1] * z[2] + self.p3e[2]

            # Fill bottom curve
            bottomFoil[:, 0] = bottom[:, 0] * x[0] + bottom[:, 1] * z[0] + self.p3e[0]
            bottomFoil[:, 1] = bottom[:, 0] * x[1] + bottom[:, 1] * z[1] + self.p3e[1]
            bottomFoil[:, 2] = bottom[:, 0] * x[2] + bottom[:, 1] * z[2] + self.p3e[2]

            self.curve9e = topFoil
            self.curve10e = bottomFoil
        
        else:

            self.curve9e = zeros((1, 3))
            self.curve10e = zeros((1, 3))
    
    #-------------------------------------#
    @property
    def curve11e(self) -> Curve:
        return self.__curve11e
    
    @curve11e.setter
    def curve11e(self, value: Curve) -> None:
        self.__curve11e = value
    
    @property
    def curve12e(self) -> Curve:
        return self.__curve12e
    
    @curve12e.setter
    def curve12e(self, value: Curve) -> None:
        self.__curve12e = value
    
    def calcMiddle2FoilE(self) -> None:
        
        if self.__data.middleAirfoil is not None:

            # Top and bottom curve
            i_max = argmin(self.__data.middleAirfoil[:, 0])
            top = self.__data.middleAirfoil[:i_max + 1, :]
            bottom = self.__data.middleAirfoil[i_max:, :]

            top = flip(top, 0)

            # Section vectors
            x = self.v3e - self.p4e
            z = self.z3e * vector.norm(x)

            # Create curves
            topFoil = zeros((len(top[:, 0]), 3))
            bottomFoil = zeros((len(bottom[:, 0]), 3))

            # Fill top curve
            topFoil[:, 0] = top[:, 0] * x[0] + top[:, 1] * z[0] + self.p4e[0]
            topFoil[:, 1] = top[:, 0] * x[1] + top[:, 1] * z[1] + self.p4e[1]
            topFoil[:, 2] = top[:, 0] * x[2] + top[:, 1] * z[2] + self.p4e[2]

            # Fill bottom curve
            bottomFoil[:, 0] = bottom[:, 0] * x[0] + bottom[:, 1] * z[0] + self.p4e[0]
            bottomFoil[:, 1] = bottom[:, 0] * x[1] + bottom[:, 1] * z[1] + self.p4e[1]
            bottomFoil[:, 2] = bottom[:, 0] * x[2] + bottom[:, 1] * z[2] + self.p4e[2]

            self.curve11e = topFoil
            self.curve12e = bottomFoil
        
        else:

            self.curve11e = zeros((1, 3))
            self.curve12e = zeros((1, 3))
    
    #-------------------------------------#
    @property
    def curve13e(self) -> Curve:
        return self.__curve13e
    
    @curve13e.setter
    def curve13e(self, value: Curve) -> None:
        self.__curve13e = value
    
    @property
    def curve14e(self) -> Curve:
        return self.__curve14e
    
    @curve14e.setter
    def curve14e(self, value: Curve) -> None:
        self.__curve14e = value
    
    def calcTipFoilE(self) -> None:
        
        if self.__data.tipAirfoil is not None:

            # Top and bottom curve
            i_max = argmin(self.__data.middleAirfoil[:, 0])
            top = self.__data.middleAirfoil[:i_max + 1, :]
            bottom = self.__data.middleAirfoil[i_max:, :]

            top = flip(top, 0)

            # Section vectors
            x = self.v2e - self.v1e
            z = self.z3e * vector.norm(x)

            # Create curves
            topFoil = zeros((len(top[:, 0]), 3))
            bottomFoil = zeros((len(bottom[:, 0]), 3))

            # Fill top curve
            topFoil[:, 0] = top[:, 0] * x[0] + top[:, 1] * z[0] + self.v1e[0]
            topFoil[:, 1] = top[:, 0] * x[1] + top[:, 1] * z[1] + self.v1e[1]
            topFoil[:, 2] = top[:, 0] * x[2] + top[:, 1] * z[2] + self.v1e[2]

            # Fill bottom curve
            bottomFoil[:, 0] = bottom[:, 0] * x[0] + bottom[:, 1] * z[0] + self.v1e[0]
            bottomFoil[:, 1] = bottom[:, 0] * x[1] + bottom[:, 1] * z[1] + self.v1e[1]
            bottomFoil[:, 2] = bottom[:, 0] * x[2] + bottom[:, 1] * z[2] + self.v1e[2]

            self.curve13e = topFoil
            self.curve14e = bottomFoil
        
        else:
        
            self.curve13e = zeros((1, 3))
            self.curve14e = zeros((1, 3))
    
    #########################################################
    # Quaternions
    #########################################################

    #-------------------------------------#
    @property
    def quaternion1d(self) -> Quaternion:
        return self.__quaternion1d
    
    @quaternion1d.setter
    def quaternion1d(self, value: Quaternion) -> None:
        self.__quaternion1d = value
    
    def calcQuaternion1d(self) -> None:
        
        # Quaternion around -y
        q_y = quaternion.fromAxisAngle(-self.__data.y0, self.__data.theta2d)

        # Rotate x axis
        x1 = quaternion.rotate(q_y, self.__data.x0)

        # Quaternion around x
        q_x = quaternion.fromAxisAngle(-x1, self.__data.theta1d)

        # Multiply rotation
        q_yx = quaternion.multiply(q_x, q_y)

        # Rotate z axis
        z1 = quaternion.rotate(q_yx, self.__data.z0)

        # Quaternion around z
        q_z = quaternion.fromAxisAngle(-z1, self.__data.theta3d)

        # Multiply rotation
        q_yxz = quaternion.multiply(q_z, q_yx)

        # Save quaternion
        self.quaternion1d = q_yxz
    
    #-------------------------------------#
    @property
    def quaternionBase2d(self) -> Quaternion:
        return self.__quaternionBase2d
    
    @quaternionBase2d.setter
    def quaternionBase2d(self, value: Quaternion) -> None:
        self.__quaternionBase2d = value
    
    def calcQuaternionBase2d(self) -> None:
        
        # Quaternion around -z
        q_z = quaternion.fromAxisAngle(self.z1d, self.__data.theta5d)

        # Multiply rotation
        q_yxz_z = quaternion.multiply(q_z, self.quaternion1d)

        # Save quaternion
        self.quaternionBase2d = q_yxz_z
    
    #-------------------------------------#
    @property
    def quaternionTip2d(self) -> Quaternion:
        return self.__quaternionTip2d
    
    @quaternionTip2d.setter
    def quaternionTip2d(self, value: Quaternion) -> None:
        self.__quaternionTip2d = value
    
    def calcQuaternionTip2d(self) -> None:
        
        # Quaternion around -y
        q_y = quaternion.fromAxisAngle(-self.yBase2d, self.__data.theta4d)

        # Multiply rotation
        q_yxz_zy = quaternion.multiply(q_y, self.quaternionBase2d)

        # Save quaternion
        self.quaternionTip2d = q_yxz_zy
    
    #-------------------------------------#
    @property
    def quaternion3d(self) -> Quaternion:
        return self.__quaternion3d
    
    @quaternion3d.setter
    def quaternion3d(self, value: Quaternion) -> None:
        self.__quaternion3d = value
    
    def calcQuaternion3d(self) -> None:
        
        # Quaternion around -x
        q_x = quaternion.fromAxisAngle(self.xTip2d, self.__data.theta6d)

        # Multiply rotation
        q_yxz_zy_x = quaternion.multiply(q_x, self.quaternionTip2d)

        # Rotate z axis
        z3 = quaternion.rotate(q_yxz_zy_x, self.__data.z0)

        # Quaternion around z
        q_z = quaternion.fromAxisAngle(-z3, self.__data.theta7d)

        # Multiply rotation
        q_yxz_zy_xz = quaternion.multiply(q_z, q_yxz_zy_x)

        # Save quaternion
        self.quaternion3d = q_yxz_zy_xz
    
    #########################################################
    # Base vectors
    #########################################################

    #-------------------------------------#
    @property
    def x1d(self) -> Vector:
        return self.__x1d
    
    @x1d.setter
    def x1d(self, value: Vector) -> None:
        self.__x1d = value
    
    def calcX1d(self) -> None:
        self.x1d = quaternion.rotate(self.quaternion1d, self.__data.x0)
    
    @property
    def y1d(self) -> Vector:
        return self.__y1d
    
    @y1d.setter
    def y1d(self, value: Vector) -> None:
        self.__y1d = value
    
    def calcY1d(self) -> None:
        self.y1d = quaternion.rotate(self.quaternion1d, self.__data.y0)
    
    @property
    def z1d(self) -> Vector:
        return self.__z1d
    
    @z1d.setter
    def z1d(self, value: Vector) -> None:
        self.__z1d = value
    
    def calcZ1d(self) -> None:
        self.z1d = quaternion.rotate(self.quaternion1d, self.__data.z0)
    
    #-------------------------------------#
    @property
    def xBase2d(self) -> Vector:
        return self.__xBase2d
    
    @xBase2d.setter
    def xBase2d(self, value: Vector) -> None:
        self.__xBase2d = value
    
    def calcXBase2d(self) -> None:
        self.xBase2d = quaternion.rotate(self.quaternionBase2d, self.__data.x0)
    
    @property
    def yBase2d(self) -> Vector:
        return self.__yBase2d
    
    @yBase2d.setter
    def yBase2d(self, value: Vector) -> None:
        self.__yBase2d = value
    
    def calcYBase2d(self) -> None:
        self.yBase2d = quaternion.rotate(self.quaternionBase2d, self.__data.y0)
    
    @property
    def zBase2d(self) -> Vector:
        return self.__zBase2d
    
    @zBase2d.setter
    def zBase2d(self, value: Vector) -> None:
        self.__zBase2d = value
    
    def calcZBase2d(self) -> None:
        self.zBase2d = quaternion.rotate(self.quaternionBase2d, self.__data.z0)
    
    #-------------------------------------#
    @property
    def xTip2d(self) -> Vector:
        return self.__xTip2d
    
    @xTip2d.setter
    def xTip2d(self, value: Vector) -> None:
        self.__xTip2d = value
    
    def calcXTip2d(self) -> None:
        self.xTip2d = quaternion.rotate(self.quaternionTip2d, self.__data.x0)
    
    @property
    def yTip2d(self) -> Vector:
        return self.__yTip2d
    
    @yTip2d.setter
    def yTip2d(self, value: Vector) -> None:
        self.__yTip2d = value
    
    def calcYTip2d(self) -> None:
        self.yTip2d = quaternion.rotate(self.quaternionTip2d, self.__data.y0)
    
    @property
    def zTip2d(self) -> Vector:
        return self.__zTip2d
    
    @zTip2d.setter
    def zTip2d(self, value: Vector) -> None:
        self.__zTip2d = value
    
    def calcZTip2d(self) -> None:
        self.zTip2d = quaternion.rotate(self.quaternionTip2d, self.__data.z0)
    
    #-------------------------------------#
    @property
    def x3d(self) -> Vector:
        return self.__x3d
    
    @x3d.setter
    def x3d(self, value: Vector) -> None:
        self.__x3d = value
    
    def calcX3d(self) -> None:
        self.x3d = quaternion.rotate(self.quaternion3d, self.__data.x0)
    
    @property
    def y3d(self) -> Vector:
        return self.__y3d
    
    @y3d.setter
    def y3d(self, value: Vector) -> None:
        self.__y3d = value
    
    def calcY3d(self) -> None:
        self.y3d = quaternion.rotate(self.quaternion3d, self.__data.y0)
    
    @property
    def z3d(self) -> Vector:
        return self.__z3d
    
    @z3d.setter
    def z3d(self, value: Vector) -> None:
        self.__z3d = value
    
    def calcZ3d(self) -> None:
        self.z3d = quaternion.rotate(self.quaternion3d, self.__data.z0)
    
    #########################################################
    # Control points
    #########################################################

    #-------------------------------------#
    @property
    def p0d(self) -> Vector:
        return self.__p0d
    
    @p0d.setter
    def p0d(self, value: Vector) -> None:
        self.__p0d = value
    
    def calcP0d(self) -> None:
        self.p0d = -self.__data.l0 * self.__data.y0
    
    #-------------------------------------#
    @property
    def p1d(self) -> Vector:
        return self.__p1d
    
    @p1d.setter
    def p1d(self, value: Vector) -> None:
        self.__p1d = value
    
    def calcP1d(self) -> None:
        q_z = quaternion.fromAxisAngle(-self.__data.z0, self.__data.theta0)
        q_y = quaternion.fromAxisAngle(-self.__data.y0, self.__data.theta2d)
        v = self.__data.h1 * self.__data.x0
        self.p1d = self.p0d + quaternion.rotate(q_y, quaternion.rotate(q_z, v))
    
    #-------------------------------------#
    @property
    def p3d(self) -> Vector:
        return self.__p3d
    
    @p3d.setter
    def p3d(self, value: Vector) -> None:
        self.__p3d = value
    
    def calcP3d(self) -> None:
        self.p3d = self.p0d - self.__data.l1 * self.y1d - (self.__data.l2 - self.__data.h2) * self.yBase2d + self.__data.h3 * self.xTip2d
    
    #-------------------------------------#
    @property
    def p3dLine(self) -> Vector:
        return self.__p3dLine
    
    @p3dLine.setter
    def p3dLine(self, value: Vector) -> None:
        self.__p3dLine = value
    
    def calcP3dLine(self) -> None:
        self.p3dLine = self.p0d - self.__data.l1 * self.y1d - (self.__data.l2 - self.__data.h2) * self.yBase2d + self.__data.h3 * self.xBase2d
    
    #-------------------------------------#
    @property
    def p4d(self) -> Vector:
        return self.__p4d
    
    @p4d.setter
    def p4d(self, value: Vector) -> None:
        self.__p4d = value
    
    def calcP4d(self) -> None:
        self.p4d = self.p0d - self.__data.l1 * self.y1d - self.__data.l2 * self.yBase2d - self.__data.h2 * self.y3d + self.__data.h3 * self.x3d
    
    #-------------------------------------#
    @property
    def p5d(self) -> Vector:
        return self.__p5d
    
    @p5d.setter
    def p5d(self, value: Vector) -> None:
        self.__p5d = value
    
    def calcP5d(self) -> None:
        self.p5d = self.p4d - (self.__data.l3 - self.__data.h2) * self.y3d
    
    #-------------------------------------#
    @property
    def p6d(self) -> Vector:
        return self.__p6d
    
    @p6d.setter
    def p6d(self, value: Vector) -> None:
        self.__p6d = value
    
    def calcP6d(self) -> None:
        self.p6d = self.p5d - self.__data.h4 * self.x3d - self.__data.h5 * self.y3d
    
    #-------------------------------------#
    @property
    def p7d(self) -> Vector:
        return self.__p7d
    
    @p7d.setter
    def p7d(self, value: Vector) -> None:
        self.__p7d = value
    
    def calcP7d(self) -> None:
        self.p7d = self.p0d - self.__data.l1 * self.y1d - self.__data.l2 * self.yTip2d - self.__data.h6 * vector.unary(self.xTip2d + self.x3d)
    
    #-------------------------------------#
    @property
    def p8d(self) -> Vector:
        return self.__p8d
    
    @p8d.setter
    def p8d(self, value: Vector) -> None:
        self.__p8d = value
    
    def calcP8d(self) -> None:
        q_z = quaternion.fromAxisAngle(-self.__data.z0, self.__data.theta0)
        q_y = quaternion.fromAxisAngle(-self.__data.y0, self.__data.theta2d)
        v = - self.__data.h7 * self.__data.x0
        self.p8d = self.p0d + quaternion.rotate(q_y, quaternion.rotate(q_z, v))
    
    #-------------------------------------#
    @property
    def c1d(self) -> Vector:
        return self.__c1d
    
    @c1d.setter
    def c1d(self, value: Vector) -> None:
        self.__c1d = value
    
    def calcC1d(self) -> None:
        p = self.p0d - self.__data.l1 * self.y1d
        dist = vector.norm(vector.cross(p - self.p1d, p - self.p3d)) / vector.norm(self.p3d - self.p1d)
        self.c1d = self.p0d - self.__data.l1 * self.y1d + self.__data.delta1 * dist * vector.unary(self.x1d + self.xBase2d)
    
    #-------------------------------------#
    @property
    def p2d(self) -> Vector:
        return self.__p2d
    
    @p2d.setter
    def p2d(self, value: Vector) -> None:
        self.__p2d = value
    
    def calcP2d(self) -> None:
        self.p2d = 0.25 * self.p1d + 0.5 * self.c1d + 0.25 * self.p3dLine
    
    #-------------------------------------#
    @property
    def c2d(self) -> Vector:
        return self.__c2d
    
    @c2d.setter
    def c2d(self, value: Vector) -> None:
        self.__c2d = value
    
    def calcC2d(self) -> None:
        self.c2d = self.p2d + self.__data.epsilon1 * vector.dot(self.p3d - self.p2d, vector.unary(self.p3d - self.p1d)) * vector.unary(self.p3d - self.p1d)
    
    #-------------------------------------#
    @property
    def c4d(self) -> Vector:
        return self.__c4d
    
    @c4d.setter
    def c4d(self, value: Vector) -> None:
        self.__c4d = value
    
    def calcC4d(self) -> None:
        c = vector.dot(-self.yTip2d, self.y3d)
        self.c4d = self.p3d - self.__data.epsilon3 * self.__data.h2 * (1 + acos(c if -1 <= c <= 1 else 1 if c > 1 else -1)) * self.yTip2d
    
    #-------------------------------------#
    @property
    def c3d(self) -> Vector:
        return self.__c3d
    
    @c3d.setter
    def c3d(self, value: Vector) -> None:
        self.__c3d = value
    
    def calcC3d(self) -> None:
        self.c3d = self.p3d + self.__data.epsilon2 * vector.dot(self.p2d - self.p3d, vector.unary(self.p3d - self.c4d)) * vector.unary(self.p3d - self.c4d)
    
    #-------------------------------------#
    @property
    def c5d(self) -> Vector:
        return self.__c5d
    
    @c5d.setter
    def c5d(self, value: Vector) -> None:
        self.__c5d = value
    
    def calcC5d(self) -> None:
        c = vector.dot(-self.yTip2d, self.y3d)
        self.c5d = self.p4d + self.__data.epsilon3 * self.__data.h2 * (1 + acos(c if -1 <= c <= 1 else 1 if c > 1 else -1)) * self.y3d
    
    #-------------------------------------#
    @property
    def c6d(self) -> Vector:
        return self.__c6d
    
    @c6d.setter
    def c6d(self, value: Vector) -> None:
        self.__c6d = value
    
    def calcC6d(self) -> None:
        self.c6d = self.p5d - self.__data.delta2 * (vector.dot(-self.y3d, self.p6d - self.p5d)) * self.y3d
    
    #-------------------------------------#
    @property
    def c7d(self) -> Vector:
        return self.__c7d
    
    @c7d.setter
    def c7d(self, value: Vector) -> None:
        self.__c7d = value
    
    def calcC7d(self) -> None:
        self.c7d = 0.5 * (self.p6d + self.p7d) + 0.5 * self.__data.delta3 * (self.p6d - self.p7d) - 0.5 * self.__data.delta4 * vector.cross(self.z3d, self.p6d - self.p7d)
    
    #-------------------------------------#
    @property
    def c8d(self) -> Vector:
        return self.__c8d
    
    @c8d.setter
    def c8d(self, value: Vector) -> None:
        self.__c8d = value
    
    def calcC8d(self) -> None:
        self.c8d = 0.5 * (self.p7d + self.p8d) + 0.5 * self.__data.delta5 * (self.p7d - self.p8d) - self.__data.delta6 * vector.norm(self.p7d - self.p8d) * vector.unary(vector.cross(self.zTip2d + self.zBase2d, self.p7d - self.p8d))

    #########################################################
    # Curves
    #########################################################

    #-------------------------------------#
    @property
    def curve1d(self) -> Curve:
        return self.__curve1d
    
    @curve1d.setter
    def curve1d(self, value: Curve) -> None:
        self.__curve1d = value
    
    def calcCurve1d(self) -> None:
        
        n = 100
        n_2 = int(0.5 * n)

        curve_aux_1 = curve.bezier([self.p1d, self.c1d, self.p3dLine], n=n)
        curve_aux_2 = curve.bezier([self.p2d, self.c2d, self.c3d, self.p3d], n=n_2)

        out = zeros((n, 3))

        for i in range(n):
            out[i, :] = curve_aux_1[i, :] if i < n_2 else curve_aux_2[i - n_2, :]
        
        self.curve1d = out
    
    #-------------------------------------#
    @property
    def curve2d(self) -> Curve:
        return self.__curve2d
    
    @curve2d.setter
    def curve2d(self, value: Curve) -> None:
        self.__curve2d = value
    
    def calcCurve2d(self) -> None:
        n = 100
        self.curve2d = curve.bezier([self.p3d, self.c4d, self.c5d, self.p4d], n=n)
    
    #-------------------------------------#
    @property
    def curve3d(self) -> Curve:
        return self.__curve3d
    
    @curve3d.setter
    def curve3d(self, value: Curve) -> None:
        self.__curve3d = value
    
    def calcCurve3d(self) -> None:
        n = 200
        self.curve3d = curve.line([self.p4d, self.p5d], n=n)
    
    #-------------------------------------#
    @property
    def curve4d(self) -> Curve:
        return self.__curve4d
    
    @curve4d.setter
    def curve4d(self, value: Curve) -> None:
        self.__curve4d = value
    
    def calcCurve4d(self) -> None:
        n = 150
        self.curve4d = curve.bezier([self.p5d, self.c6d, self.p6d], n=n)
    
    #-------------------------------------#
    @property
    def curve5d(self) -> Curve:
        return self.__curve5d
    
    @curve5d.setter
    def curve5d(self, value: Curve) -> None:
        self.__curve5d = value
    
    def calcCurve5d(self) -> None:
        n = 100
        self.curve5d = curve.bezier([self.p6d, self.c7d, self.p7d], n=n)
    
    #-------------------------------------#
    @property
    def curve6d(self) -> Curve:
        return self.__curve6d
    
    @curve6d.setter
    def curve6d(self, value: Curve) -> None:
        self.__curve6d = value
    
    def calcCurve6d(self) -> None:
        n = 100
        self.curve6d = curve.bezier([self.p7d, self.c8d, self.p8d], n=n)
    
    #########################################################
    # Airfoils
    #########################################################

    @property
    def v1d(self) -> Vector:
        return self.curve4d[self.v1dIndex]
    
    @property
    def v1dIndex(self) -> int:
        return int((1 - self.__data.delta) * len(self.curve4d[:, 0]))
    
    #-------------------------------------#
    @property
    def v2d(self) -> Vector:
        return self.curve5d[self.v2dIndex]
    
    @property
    def v2dIndex(self) -> int:
        return int(self.__data.delta * len(self.curve4d[:, 0]))
    
    #-------------------------------------#
    @property
    def v3d(self) -> Vector:
        return self.curve5d[self.v3dIndex]
    
    @property
    def v3dIndex(self) -> int:
        return int((1 - self.__data.delta) * len(self.curve5d[:, 0]))
    
    #-------------------------------------#
    @property
    def v4d(self) -> Vector:
        return self.curve6d[self.v4dIndex]
    
    @property
    def v4dIndex(self) -> int:
        return int(self.__data.delta * len(self.curve6d[:, 0]))
    
    #-------------------------------------#
    @property
    def curve7d(self) -> Curve:
        return self.__curve7d
    
    @curve7d.setter
    def curve7d(self, value: Curve) -> None:
        self.__curve7d = value
    
    @property
    def curve8d(self) -> Curve:
        return self.__curve8d
    
    @curve8d.setter
    def curve8d(self, value: Curve) -> None:
        self.__curve8d = value
    
    def calcRootFoilD(self) -> None:
        
        if self.__data.rootAirfoil is not None:

            # Top and bottom curve
            i_max = argmin(self.__data.rootAirfoil[:, 0])
            top = self.__data.rootAirfoil[:i_max + 1, :]
            bottom = self.__data.rootAirfoil[i_max:, :]

            top = flip(top, 0)

            # Section vectors
            x = self.p8d - self.p1d
            z = self.z1d * vector.norm(x)

            # Create curves
            topFoil = zeros((len(top[:, 0]), 3))
            bottomFoil = zeros((len(bottom[:, 0]), 3))

            # Fill top curve
            topFoil[:, 0] = top[:, 0] * x[0] + top[:, 1] * z[0] + self.p1d[0]
            topFoil[:, 1] = top[:, 0] * x[1] + top[:, 1] * z[1] + self.p1d[1]
            topFoil[:, 2] = top[:, 0] * x[2] + top[:, 1] * z[2] + self.p1d[2]

            # Fill bottom curve
            bottomFoil[:, 0] = bottom[:, 0] * x[0] + bottom[:, 1] * z[0] + self.p1d[0]
            bottomFoil[:, 1] = bottom[:, 0] * x[1] + bottom[:, 1] * z[1] + self.p1d[1]
            bottomFoil[:, 2] = bottom[:, 0] * x[2] + bottom[:, 1] * z[2] + self.p1d[2]

            self.curve7d = topFoil
            self.curve8d = bottomFoil
        
        else:

            self.curve7d = zeros((1, 3))
            self.curve8d = zeros((1, 3))
    
    #-------------------------------------#
    @property
    def curve9d(self) -> Curve:
        return self.__curve9d
    
    @curve9d.setter
    def curve9d(self, value: Curve) -> None:
        self.__curve9d = value
    
    @property
    def curve10d(self) -> Curve:
        return self.__curve10d
    
    @curve10d.setter
    def curve10d(self, value: Curve) -> None:
        self.__curve10d = value
    
    def calcMiddle1FoilD(self) -> None:
        
        if self.__data.middleAirfoil is not None:

            # Top and bottom curve
            i_max = argmin(self.__data.middleAirfoil[:, 0])
            top = self.__data.middleAirfoil[:i_max + 1, :]
            bottom = self.__data.middleAirfoil[i_max:, :]

            top = flip(top, 0)

            # Section vectors
            x = self.v4d - self.p3d
            z = self.zTip2d * vector.norm(x)

            # Create curves
            topFoil = zeros((len(top[:, 0]), 3))
            bottomFoil = zeros((len(bottom[:, 0]), 3))

            # Fill top curve
            topFoil[:, 0] = top[:, 0] * x[0] + top[:, 1] * z[0] + self.p3d[0]
            topFoil[:, 1] = top[:, 0] * x[1] + top[:, 1] * z[1] + self.p3d[1]
            topFoil[:, 2] = top[:, 0] * x[2] + top[:, 1] * z[2] + self.p3d[2]

            # Fill bottom curve
            bottomFoil[:, 0] = bottom[:, 0] * x[0] + bottom[:, 1] * z[0] + self.p3d[0]
            bottomFoil[:, 1] = bottom[:, 0] * x[1] + bottom[:, 1] * z[1] + self.p3d[1]
            bottomFoil[:, 2] = bottom[:, 0] * x[2] + bottom[:, 1] * z[2] + self.p3d[2]

            self.curve9d = topFoil
            self.curve10d = bottomFoil
        
        else:

            self.curve9d = zeros((1, 3))
            self.curve10d = zeros((1, 3))
    
    #-------------------------------------#
    @property
    def curve11d(self) -> Curve:
        return self.__curve11d
    
    @curve11d.setter
    def curve11d(self, value: Curve) -> None:
        self.__curve11d = value
    
    @property
    def curve12d(self) -> Curve:
        return self.__curve12d
    
    @curve12d.setter
    def curve12d(self, value: Curve) -> None:
        self.__curve12d = value
    
    def calcMiddle2FoilD(self) -> None:
        
        if self.__data.middleAirfoil is not None:

            # Top and bottom curve
            i_max = argmin(self.__data.middleAirfoil[:, 0])
            top = self.__data.middleAirfoil[:i_max + 1, :]
            bottom = self.__data.middleAirfoil[i_max:, :]

            top = flip(top, 0)

            # Section vectors
            x = self.v3d - self.p4d
            z = self.z3d * vector.norm(x)

            # Create curves
            topFoil = zeros((len(top[:, 0]), 3))
            bottomFoil = zeros((len(bottom[:, 0]), 3))

            # Fill top curve
            topFoil[:, 0] = top[:, 0] * x[0] + top[:, 1] * z[0] + self.p4d[0]
            topFoil[:, 1] = top[:, 0] * x[1] + top[:, 1] * z[1] + self.p4d[1]
            topFoil[:, 2] = top[:, 0] * x[2] + top[:, 1] * z[2] + self.p4d[2]

            # Fill bottom curve
            bottomFoil[:, 0] = bottom[:, 0] * x[0] + bottom[:, 1] * z[0] + self.p4d[0]
            bottomFoil[:, 1] = bottom[:, 0] * x[1] + bottom[:, 1] * z[1] + self.p4d[1]
            bottomFoil[:, 2] = bottom[:, 0] * x[2] + bottom[:, 1] * z[2] + self.p4d[2]

            self.curve11d = topFoil
            self.curve12d = bottomFoil
        
        else:

            self.curve11d = zeros((1, 3))
            self.curve12d = zeros((1, 3))
    
    #-------------------------------------#
    @property
    def curve13d(self) -> Curve:
        return self.__curve13d
    
    @curve13d.setter
    def curve13d(self, value: Curve) -> None:
        self.__curve13d = value
    
    @property
    def curve14d(self) -> Curve:
        return self.__curve14d
    
    @curve14d.setter
    def curve14d(self, value: Curve) -> None:
        self.__curve14d = value
    
    def calcTipFoilD(self) -> None:
        
        if self.__data.tipAirfoil is not None:

            # Top and bottom curve
            i_max = argmin(self.__data.middleAirfoil[:, 0])
            top = self.__data.middleAirfoil[:i_max + 1, :]
            bottom = self.__data.middleAirfoil[i_max:, :]

            top = flip(top, 0)

            # Section vectors
            x = self.v2d - self.v1d
            z = self.z3d * vector.norm(x)

            # Create curves
            topFoil = zeros((len(top[:, 0]), 3))
            bottomFoil = zeros((len(bottom[:, 0]), 3))

            # Fill top curve
            topFoil[:, 0] = top[:, 0] * x[0] + top[:, 1] * z[0] + self.v1d[0]
            topFoil[:, 1] = top[:, 0] * x[1] + top[:, 1] * z[1] + self.v1d[1]
            topFoil[:, 2] = top[:, 0] * x[2] + top[:, 1] * z[2] + self.v1d[2]

            # Fill bottom curve
            bottomFoil[:, 0] = bottom[:, 0] * x[0] + bottom[:, 1] * z[0] + self.v1d[0]
            bottomFoil[:, 1] = bottom[:, 0] * x[1] + bottom[:, 1] * z[1] + self.v1d[1]
            bottomFoil[:, 2] = bottom[:, 0] * x[2] + bottom[:, 1] * z[2] + self.v1d[2]

            self.curve13d = topFoil
            self.curve14d = bottomFoil
        
        else:
        
            self.curve13d = zeros((1, 3))
            self.curve14d = zeros((1, 3))