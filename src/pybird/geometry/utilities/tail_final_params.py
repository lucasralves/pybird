from numpy import array, zeros

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