from math import atan, cos
from numpy import argmin, array, flip, zeros

from pybird.geometry.utilities.body_final_params import BodyFinalParams
from pybird.geometry.utilities.data import Data
from pybird.helpers.type import Curve, Quaternion, Vector
from pybird.helpers import quaternion
from pybird.helpers import vector
from pybird.helpers import curve


class TailFinalParams:

    def __init__(self, data: Data, body: BodyFinalParams) -> None:
        self.__data = data
        self.__body = body
        self.update()
    
    def update(self) -> None:
        self.calcQuaternion()
        self.calcX4()
        self.calcY4()
        self.calcZ4()
        self.calcP19e()
        self.calcP19d()
        self.calcc33()
        self.calcP19e()
        self.calcP19d()
        self.calcp20()
        self.calcc34()
        self.calcc35()
        self.calcCurve35e()
        self.calcCurve35d()
        self.calcCurve36e()
        self.calcCurve36d()
        self.calcCurve37()
        self.calcCurve38()

        self.calcV5Index()
        self.calcV6V7Index()
        self.calcTailFirstProfileE()
        self.calcTailSecondProfileE()
        self.calcTailFirstProfileD()
        self.calcTailSecondProfileD()
    
    #########################################################
    # Quaternions
    #########################################################

    #-------------------------------------#
    @property
    def quaternion4(self) -> Quaternion:
        return self.__quaternion4
    
    @quaternion4.setter
    def quaternion4(self, value: Quaternion) -> None:
        self.__quaternion4 = value
    
    def calcQuaternion(self) -> None:

        x4 = array([-1., .0, .0])
        y4 = array([.0, -1., .0])
        z4 = array([.0, .0, 1.])
        
        # Quaternion around x
        q_x = quaternion.fromAxisAngle(x4, self.__data.theta8)

        # Rotate y axis
        y4 = quaternion.rotate(q_x, y4)

        # Quaternion around y
        q_y = quaternion.fromAxisAngle(y4, self.__data.theta9)

        # Multiply rotation
        q_xy = quaternion.multiply(q_y, q_x)

        # Rotate z axis
        z4 = quaternion.rotate(q_xy, z4)

        # Quaternion around z
        q_z = quaternion.fromAxisAngle(z4, self.__data.theta10)

        # Multiply rotation
        q_xyz = quaternion.multiply(q_z, q_xy)

        # Save quaternion
        self.quaternion4 = q_xyz
    
    #########################################################
    # Base vectors
    #########################################################

    #-------------------------------------#
    @property
    def x4(self) -> Vector:
        return self.__x4
    
    @x4.setter
    def x4(self, value: Vector) -> None:
        self.__x4 = value
    
    def calcX4(self) -> None:
        x4 = array([-1., .0, .0])
        self.x4 = quaternion.rotate(self.quaternion4, x4)
    
    @property
    def y4(self) -> Vector:
        return self.__y4
    
    @y4.setter
    def y4(self, value: Vector) -> None:
        self.__y4 = value
    
    def calcY4(self) -> None:
        y4 = array([.0, -1., .0])
        self.y4 = quaternion.rotate(self.quaternion4, y4)
    
    @property
    def z4(self) -> Vector:
        return self.__z4
    
    @z4.setter
    def z4(self, value: Vector) -> None:
        self.__z4 = value
    
    def calcZ4(self) -> None:
        z4 = array([.0, .0, 1.])
        self.z4 = quaternion.rotate(self.quaternion4, z4)
    
    #########################################################
    # Control points
    #########################################################

    #-------------------------------------#
    @property
    def p19e(self) -> Vector:
        return self.__p19e
    
    @p19e.setter
    def p19e(self, value: Vector) -> None:
        self.__p19e = value
    
    def calcP19e(self) -> None:
        self.p19e = 0.5 * (self.__body.p10e + self.__body.p10d) + self.__data.h20 * self.x4 - 0.5 * self.__data.h19 * self.y4
    
    #-------------------------------------#
    @property
    def p19d(self) -> Vector:
        return self.__p19d
    
    @p19d.setter
    def p19d(self, value: Vector) -> None:
        self.__p19d = value
    
    def calcP19d(self) -> None:
        self.p19d = 0.5 * (self.__body.p10e + self.__body.p10d) + self.__data.h20 * self.x4 + 0.5 * self.__data.h19 * self.y4 
    
    #-------------------------------------#
    @property
    def p20(self) -> Vector:
        return self.__p20
    
    @p20.setter
    def p20(self, value: Vector) -> None:
        self.__p20 = value
    
    def calcp20(self) -> None:
        if self.__data.tailShape == '1': # square
            self.p20 = 0.5 * (self.p19e + self.p19d)
        elif self.__data.tailShape == '2': # v
            self.p20 = 0.5 * (self.__body.p10e + self.__body.p10d) + (self.__data.h20 - self.__data.h21) * self.x4
        elif self.__data.tailShape == '3': # pointed
            self.p20 = 0.5 * (self.__body.p10e + self.__body.p10d) + (self.__data.h20 + self.__data.h21) * self.x4
        elif self.__data.tailShape == '4': # rounded
            radius = vector.norm(self.p19e - self.c33)
            self.p20 = self.c33 + radius * self.x4
    
    #-------------------------------------#
    @property
    def c33(self) -> Vector:
        return self.__c33
    
    @c33.setter
    def c33(self, value: Vector) -> None:
        self.__c33 = value
    
    def calcc33(self) -> None:
        self.c33 = 0.5 * (self.__body.p10e + self.__body.p10d) + self.__data.h20 * (1 - self.__data.delta47) * self.x4
    
    #-------------------------------------#
    @property
    def c34(self) -> Vector:
        return self.__c34
    
    @c34.setter
    def c34(self, value: Vector) -> None:
        self.__c34 = value
    
    def calcc34(self) -> None:
        if self.__data.tailShape == '1': # square
            self.c34 = self.__body.p14 + self.__data.delta48 * self.__data.h20 * self.x4
        elif self.__data.tailShape == '2': # v
            self.c34 = self.__body.p14 + self.__data.delta48 * (self.__data.h20 - self.__data.h21) * self.x4
        elif self.__data.tailShape == '3': # pointed
            self.c34 = self.__body.p14 + self.__data.delta48 * (self.__data.h20 + self.__data.h21) * self.x4
        elif self.__data.tailShape == '4': # rounded
            self.c34 = self.__body.p14 + self.__data.delta48 * self.__data.h19 * self.x4
    
    #-------------------------------------#
    @property
    def c35(self) -> Vector:
        return self.__c35
    
    @c35.setter
    def c35(self, value: Vector) -> None:
        self.__c35 = value
    
    def calcc35(self) -> None:
        if self.__data.tailShape == '1': # square
            self.c35 = self.__body.p15 + self.__data.delta48 * self.__data.h20 * self.x4
        elif self.__data.tailShape == '2': # v
            self.c35 = self.__body.p15 + self.__data.delta48 * (self.__data.h20 - self.__data.h21) * self.x4
        elif self.__data.tailShape == '3': # pointed
            self.c35 = self.__body.p15 + self.__data.delta48 * (self.__data.h20 + self.__data.h21) * self.x4
        elif self.__data.tailShape == '4': # rounded
            self.c35 = self.__body.p15 + self.__data.delta48 * self.__data.h19 * self.x4
    
    
    #########################################################
    # Curves
    #########################################################

    #-------------------------------------#
    @property
    def curve35e(self) -> Curve:
        return self.__curve35e
    
    @curve35e.setter
    def curve35e(self, value: Curve) -> None:
        self.__curve35e = value
    
    def calcCurve35e(self) -> None:
        n = 50
        out = curve.line([self.__body.p10e, self.p19e], n=n)
        self.curve35e = out
    
    #-------------------------------------#
    @property
    def curve35d(self) -> Curve:
        return self.__curve35d
    
    @curve35d.setter
    def curve35d(self, value: Curve) -> None:
        self.__curve35d = value
    
    def calcCurve35d(self) -> None:
        n = 50
        out = curve.line([self.__body.p10d, self.p19d], n=n)
        self.curve35d = out
    
    #-------------------------------------#
    @property
    def curve36e(self) -> Curve:
        return self.__curve36e
    
    @curve36e.setter
    def curve36e(self, value: Curve) -> None:
        self.__curve36e = value
    
    def calcCurve36e(self) -> None:
        n = 50
        if self.__data.tailShape == '4':
            out = curve.circle([self.p19e, self.p20, self.c33], n=n)
        else:
            out = curve.line([self.p19e, self.p20], n=n)
        self.curve36e = out
    
    #-------------------------------------#
    @property
    def curve36d(self) -> Curve:
        return self.__curve36d
    
    @curve36d.setter
    def curve36d(self, value: Curve) -> None:
        self.__curve36d = value
    
    def calcCurve36d(self) -> None:
        n = 50
        if self.__data.tailShape == '4':
            out = curve.circle([self.p19d, self.p20, self.c33], n=n)
        else:
            out = curve.line([self.p19d, self.p20], n=n)
        self.curve36d = out
    
    #-------------------------------------#
    @property
    def curve37(self) -> Curve:
        return self.__curve37
    
    @curve37.setter
    def curve37(self, value: Curve) -> None:
        self.__curve37 = value
    
    def calcCurve37(self) -> None:
        n = 50
        out = curve.bezier([self.__body.p14, self.c34, self.p20], n=n)
        self.curve37 = out
    
    #-------------------------------------#
    @property
    def curve38(self) -> Curve:
        return self.__curve38
    
    @curve38.setter
    def curve38(self, value: Curve) -> None:
        self.__curve38 = value
    
    def calcCurve38(self) -> None:
        n = 50
        out = curve.bezier([self.__body.p15, self.c35, self.p20], n=n)
        self.curve38 = out
    
    #-------------------------------------#
    @property
    def v5e(self) -> Curve:
        return self.__v5e
    
    @v5e.setter
    def v5e(self, value: Curve) -> None:
        self.__v5e = value
    
    @property
    def v5d(self) -> Curve:
        return self.__v5d
    
    @v5d.setter
    def v5d(self, value: Curve) -> None:
        self.__v5d = value
    
    @property
    def v5eIndex(self) -> Curve:
        return self.__v5eIndex
    
    @v5eIndex.setter
    def v5eIndex(self, value: Curve) -> None:
        self.__v5eIndex = value
    
    @property
    def v5dIndex(self) -> Curve:
        return self.__v5dIndex
    
    @v5dIndex.setter
    def v5dIndex(self, value: Curve) -> None:
        self.__v5dIndex = value
    
    def calcV5Index(self) -> None:

        theta = atan(2 * self.__data.h21 / self.__data.h19)
        delta = self.__data.h11 / cos(theta)

        curve = flip(self.curve36e, 0)
        for i in range(len(curve[:, 0])):
            norm = vector.norm(self.p20 - curve[i, :])
            if norm > delta:
                self.v5eIndex = len(curve[:, 0]) - 1 - i
                break
        
        self.v5e = self.curve36e[self.v5eIndex, :]

        curve = flip(self.curve36d, 0)
        for i in range(len(curve[:, 0])):
            norm = vector.norm(self.p20 - curve[i, :])
            if norm > delta:
                self.v5dIndex = len(curve[:, 0]) - 1 - i
                break
        
        self.v5d = self.curve36d[self.v5dIndex, :]
    
    #-------------------------------------#
    @property
    def v6e(self) -> Curve:
        return self.__v6e
    
    @v6e.setter
    def v6e(self, value: Curve) -> None:
        self.__v6e = value
    
    @property
    def v7e(self) -> Curve:
        return self.__v7e
    
    @v7e.setter
    def v7e(self, value: Curve) -> None:
        self.__v7e = value
    
    @property
    def v6d(self) -> Curve:
        return self.__v6d
    
    @v6d.setter
    def v6d(self, value: Curve) -> None:
        self.__v6d = value
    
    @property
    def v7d(self) -> Curve:
        return self.__v7d
    
    @v7d.setter
    def v7d(self, value: Curve) -> None:
        self.__v7d = value
    
    @property
    def v6eIndex(self) -> Curve:
        return self.__v6eIndex
    
    @v6eIndex.setter
    def v6eIndex(self, value: Curve) -> None:
        self.__v6eIndex = value
    
    @property
    def v6dIndex(self) -> Curve:
        return self.__v6dIndex
    
    @v6dIndex.setter
    def v6dIndex(self, value: Curve) -> None:
        self.__v6dIndex = value
    
    @property
    def v7eIndex(self) -> Curve:
        return self.__v7eIndex
    
    @v7eIndex.setter
    def v7eIndex(self, value: Curve) -> None:
        self.__v7eIndex = value
    
    @property
    def v7dIndex(self) -> Curve:
        return self.__v7dIndex
    
    @v7dIndex.setter
    def v7dIndex(self, value: Curve) -> None:
        self.__v7dIndex = value
    
    def calcV6V7Index(self) -> None:

        dist = vector.norm(self.p20 - self.p19e)
        delta = 0.05 * dist

        size = len(self.curve36e[:, 0])
        for i in range(size):
            norm = vector.norm(self.p19e - self.curve36e[i, :])
            if norm > delta:
                self.v6eIndex = i
                break
        
        self.v6e = self.curve36e[self.v6eIndex, :]
        
        size = len(self.curve35e[:, 0])
        for i in range(size):
            norm = vector.norm(self.p19e - self.curve35e[size - 1 - i, :])
            if norm > delta:
                self.v7eIndex = size - 1 - i
                break
        
        self.v7e = self.curve35e[self.v7eIndex, :]
        
        size = len(self.curve36d[:, 0])
        for i in range(size):
            norm = vector.norm(self.p19d - self.curve36d[i, :])
            if norm > delta:
                self.v6dIndex = i
                break
        
        self.v6d = self.curve36d[self.v6dIndex, :]
        
        size = len(self.curve35d[:, 0])
        for i in range(size):
            norm = vector.norm(self.p19d - self.curve35d[size - 1 - i, :])
            if norm > delta:
                self.v7dIndex = size - 1 - i
                break
        
        self.v7d = self.curve35d[self.v7dIndex, :]
    
    #-------------------------------------#
    @property
    def curve39e(self) -> Curve:
        return self.__curve39e
    
    @curve39e.setter
    def curve39e(self, value: Curve) -> None:
        self.__curve39e = value
    
    @property
    def curve40e(self) -> Curve:
        return self.__curve40e
    
    @curve40e.setter
    def curve40e(self, value: Curve) -> None:
        self.__curve40e = value
    
    def calcTailFirstProfileE(self) -> None:
        
        if self.__data.tailAirfoil is not None:

            # Top and bottom curve
            i_max = argmin(self.__data.tailAirfoil[:, 0])
            top = self.__data.tailAirfoil[:i_max + 1, :]
            bottom = self.__data.tailAirfoil[i_max:, :]

            top = flip(top, 0)

            # Section vectors
            x = self.v5e - self.__body.p10e
            z = self.z4 * vector.norm(x)

            # Create curves
            topFoil = zeros((len(top[:, 0]), 3))
            bottomFoil = zeros((len(bottom[:, 0]), 3))

            # Fill top curve
            topFoil[:, 0] = top[:, 0] * x[0] + top[:, 1] * z[0] + self.__body.p10e[0]
            topFoil[:, 1] = top[:, 0] * x[1] + top[:, 1] * z[1] + self.__body.p10e[1]
            topFoil[:, 2] = top[:, 0] * x[2] + top[:, 1] * z[2] + self.__body.p10e[2]

            # Fill bottom curve
            bottomFoil[:, 0] = bottom[:, 0] * x[0] + bottom[:, 1] * z[0] + self.__body.p10e[0]
            bottomFoil[:, 1] = bottom[:, 0] * x[1] + bottom[:, 1] * z[1] + self.__body.p10e[1]
            bottomFoil[:, 2] = bottom[:, 0] * x[2] + bottom[:, 1] * z[2] + self.__body.p10e[2]

            self.curve39e = topFoil
            self.curve40e = bottomFoil
        
        else:

            self.curve39e = zeros((1, 3))
            self.curve40e = zeros((1, 3))
    
    #-------------------------------------#
    @property
    def curve41e(self) -> Curve:
        return self.__curve41e
    
    @curve41e.setter
    def curve41e(self, value: Curve) -> None:
        self.__curve41e = value
    
    @property
    def curve42e(self) -> Curve:
        return self.__curve42e
    
    @curve42e.setter
    def curve42e(self, value: Curve) -> None:
        self.__curve42e = value
    
    def calcTailSecondProfileE(self) -> None:
        
        if self.__data.tailAirfoil is not None:

            # Top and bottom curve
            i_max = argmin(self.__data.tailAirfoil[:, 0])
            top = self.__data.tailAirfoil[:i_max + 1, :]
            bottom = self.__data.tailAirfoil[i_max:, :]

            top = flip(top, 0)

            # Section vectors
            x = self.v6e - self.v7e
            z = self.z4 * vector.norm(x)

            # Create curves
            topFoil = zeros((len(top[:, 0]), 3))
            bottomFoil = zeros((len(bottom[:, 0]), 3))

            # Fill top curve
            topFoil[:, 0] = top[:, 0] * x[0] + top[:, 1] * z[0] + self.v7e[0]
            topFoil[:, 1] = top[:, 0] * x[1] + top[:, 1] * z[1] + self.v7e[1]
            topFoil[:, 2] = top[:, 0] * x[2] + top[:, 1] * z[2] + self.v7e[2]

            # Fill bottom curve
            bottomFoil[:, 0] = bottom[:, 0] * x[0] + bottom[:, 1] * z[0] + self.v7e[0]
            bottomFoil[:, 1] = bottom[:, 0] * x[1] + bottom[:, 1] * z[1] + self.v7e[1]
            bottomFoil[:, 2] = bottom[:, 0] * x[2] + bottom[:, 1] * z[2] + self.v7e[2]

            self.curve41e = topFoil
            self.curve42e = bottomFoil
        
        else:

            self.curve41e = zeros((1, 3))
            self.curve42e = zeros((1, 3))
    
    #-------------------------------------#
    @property
    def curve39d(self) -> Curve:
        return self.__curve39d
    
    @curve39d.setter
    def curve39d(self, value: Curve) -> None:
        self.__curve39d = value
    
    @property
    def curve40d(self) -> Curve:
        return self.__curve40d
    
    @curve40d.setter
    def curve40d(self, value: Curve) -> None:
        self.__curve40d = value
    
    def calcTailFirstProfileD(self) -> None:
        
        if self.__data.tailAirfoil is not None:

            # Top and bottom curve
            i_max = argmin(self.__data.tailAirfoil[:, 0])
            top = self.__data.tailAirfoil[:i_max + 1, :]
            bottom = self.__data.tailAirfoil[i_max:, :]

            top = flip(top, 0)

            # Section vectors
            x = self.v5d - self.__body.p10d
            z = self.z4 * vector.norm(x)

            # Create curves
            topFoil = zeros((len(top[:, 0]), 3))
            bottomFoil = zeros((len(bottom[:, 0]), 3))

            # Fill top curve
            topFoil[:, 0] = top[:, 0] * x[0] + top[:, 1] * z[0] + self.__body.p10d[0]
            topFoil[:, 1] = top[:, 0] * x[1] + top[:, 1] * z[1] + self.__body.p10d[1]
            topFoil[:, 2] = top[:, 0] * x[2] + top[:, 1] * z[2] + self.__body.p10d[2]

            # Fill bottom curve
            bottomFoil[:, 0] = bottom[:, 0] * x[0] + bottom[:, 1] * z[0] + self.__body.p10d[0]
            bottomFoil[:, 1] = bottom[:, 0] * x[1] + bottom[:, 1] * z[1] + self.__body.p10d[1]
            bottomFoil[:, 2] = bottom[:, 0] * x[2] + bottom[:, 1] * z[2] + self.__body.p10d[2]

            self.curve39d = topFoil
            self.curve40d = bottomFoil
        
        else:

            self.curve39d = zeros((1, 3))
            self.curve40d = zeros((1, 3))
    
    #-------------------------------------#
    @property
    def curve41d(self) -> Curve:
        return self.__curve41d
    
    @curve41d.setter
    def curve41d(self, value: Curve) -> None:
        self.__curve41d = value
    
    @property
    def curve42d(self) -> Curve:
        return self.__curve42d
    
    @curve42d.setter
    def curve42d(self, value: Curve) -> None:
        self.__curve42d = value
    
    def calcTailSecondProfileD(self) -> None:
        
        if self.__data.tailAirfoil is not None:

            # Top and bottom curve
            i_max = argmin(self.__data.tailAirfoil[:, 0])
            top = self.__data.tailAirfoil[:i_max + 1, :]
            bottom = self.__data.tailAirfoil[i_max:, :]

            top = flip(top, 0)

            # Section vectors
            x = self.v6d - self.v7d
            z = self.z4 * vector.norm(x)

            # Create curves
            topFoil = zeros((len(top[:, 0]), 3))
            bottomFoil = zeros((len(bottom[:, 0]), 3))

            # Fill top curve
            topFoil[:, 0] = top[:, 0] * x[0] + top[:, 1] * z[0] + self.v7d[0]
            topFoil[:, 1] = top[:, 0] * x[1] + top[:, 1] * z[1] + self.v7d[1]
            topFoil[:, 2] = top[:, 0] * x[2] + top[:, 1] * z[2] + self.v7d[2]

            # Fill bottom curve
            bottomFoil[:, 0] = bottom[:, 0] * x[0] + bottom[:, 1] * z[0] + self.v7d[0]
            bottomFoil[:, 1] = bottom[:, 0] * x[1] + bottom[:, 1] * z[1] + self.v7d[1]
            bottomFoil[:, 2] = bottom[:, 0] * x[2] + bottom[:, 1] * z[2] + self.v7d[2]

            self.curve41d = topFoil
            self.curve42d = bottomFoil
        
        else:

            self.curve41d = zeros((1, 3))
            self.curve42d = zeros((1, 3))