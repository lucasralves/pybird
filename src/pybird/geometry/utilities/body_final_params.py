from math import cos, pi

from pybird.geometry.utilities.data import Data
from pybird.geometry.utilities.wing_final_params import WingFinalParams
from pybird.helpers.type import Curve, Vector
from pybird.helpers import vector
from pybird.helpers import curve


class BodyFinalParams:

    def __init__(self, data: Data, wing: WingFinalParams) -> None:
        self.__data = data
        self.__wing = wing
        self.update()
    
    def update(self) -> None:
        self.calcP9e()
        self.calcP10e()
        self.calcP9d()
        self.calcP10d()
        self.calcP11()
        self.calcP12()
        self.calcP13()
        self.calcP14()
        self.calcP15()
        self.calcP16()
        self.calcP17()
        self.calcP18()

        self.calcC9e()
        self.calcC10e()
        self.calcC11e()
        self.calcC12e()
        self.calcC9d()
        self.calcC10d()
        self.calcC11d()
        self.calcC12d()
        self.calcC13()
        self.calcC14()
        self.calcC15()
        self.calcC16()
        self.calcC17()
        self.calcC18()
        self.calcC19()
        self.calcC20()
        self.calcC21()
        self.calcC22()
        self.calcC23()
        self.calcC24()
        self.calcC25e()
        self.calcC26e()
        self.calcC27e()
        self.calcC28e()
        self.calcC25d()
        self.calcC26d()
        self.calcC27d()
        self.calcC28d()
        self.calcC29e()
        self.calcC30e()
        self.calcC31e()
        self.calcC32e()
        self.calcC29d()
        self.calcC30d()
        self.calcC31d()
        self.calcC32d()

        self.calcCurve15e()
        self.calcCurve15d()
        self.calcCurve16e()
        self.calcCurve16d()

        self.calcCurve17()
        self.calcCurve18()
        self.calcCurve19()
        self.calcCurve20()
        self.calcCurve21()
        self.calcCurve22()

        self.calcCurve23e()
        self.calcCurve24e()
        self.calcCurve25e()
        self.calcCurve26e()
        self.calcCurve23d()
        self.calcCurve24d()
        self.calcCurve25d()
        self.calcCurve26d()

        self.calcCurve27()
        self.calcCurve28()
        self.calcCurve29()
        self.calcCurve30()
        self.calcCurve31()
        self.calcCurve32()
        self.calcCurve33()
        self.calcCurve34()


    #########################################################
    # Control points
    #########################################################

    #-------------------------------------#
    @property
    def p9e(self) -> Vector:
        return self.__p9e
    
    @p9e.setter
    def p9e(self, value: Vector) -> None:
        self.__p9e = value
    
    def calcP9e(self) -> None:
        self.p9e = self.__data.h8 * self.__data.x0 + self.__data.h9 * self.__data.y0
    
    #-------------------------------------#
    @property
    def p9d(self) -> Vector:
        return self.__p9d
    
    @p9d.setter
    def p9d(self, value: Vector) -> None:
        self.__p9d = value
    
    def calcP9d(self) -> None:
        self.p9d = self.__data.h8 * self.__data.x0 - self.__data.h9 * self.__data.y0
    
    #-------------------------------------#
    @property
    def p10e(self) -> Vector:
        return self.__p10e
    
    @p10e.setter
    def p10e(self, value: Vector) -> None:
        self.__p10e = value
    
    def calcP10e(self) -> None:
        self.p10e = -(self.__data.h7 * cos(self.__data.theta0 * pi / 180) + self.__data.h10) * self.__data.x0 + self.__data.h11 * self.__data.y0
    
    #-------------------------------------#
    @property
    def p10d(self) -> Vector:
        return self.__p10d
    
    @p10d.setter
    def p10d(self, value: Vector) -> None:
        self.__p10d = value
    
    def calcP10d(self) -> None:
        self.p10d = -(self.__data.h7 * cos(self.__data.theta0 * pi / 180) + self.__data.h10) * self.__data.x0 - self.__data.h11 * self.__data.y0
    
    #-------------------------------------#
    @property
    def p11(self) -> Vector:
        return self.__p11
    
    @p11.setter
    def p11(self, value: Vector) -> None:
        self.__p11 = value
    
    def calcP11(self) -> None:
        self.p11 = self.__data.h8 * self.__data.x0 + self.__data.h9 * self.__data.z0
    
    #-------------------------------------#
    @property
    def p12(self) -> Vector:
        return self.__p12
    
    @p12.setter
    def p12(self, value: Vector) -> None:
        self.__p12 = value
    
    def calcP12(self) -> None:
        self.p12 = self.__data.h12 * self.__data.z0 + self.__data.h1 * self.__data.x0
    
    #-------------------------------------#
    @property
    def p13(self) -> Vector:
        return self.__p13
    
    @p13.setter
    def p13(self, value: Vector) -> None:
        self.__p13 = value
    
    def calcP13(self) -> None:
        self.p13 = - self.__data.h7 * cos(self.__data.theta0 * pi / 180) * self.__data.x0 + self.__data.h13 * self.__data.z0
    
    #-------------------------------------#
    @property
    def p14(self) -> Vector:
        return self.__p14
    
    @p14.setter
    def p14(self, value: Vector) -> None:
        self.__p14 = value
    
    def calcP14(self) -> None:
        self.p14 = - (self.__data.h7 * cos(self.__data.theta0 * pi / 180) + self.__data.h10) * self.__data.x0 + self.__data.h14 * self.__data.z0
    
    #-------------------------------------#
    @property
    def p15(self) -> Vector:
        return self.__p15
    
    @p15.setter
    def p15(self, value: Vector) -> None:
        self.__p15 = value
    
    def calcP15(self) -> None:
        self.p15 = - (self.__data.h7 * cos(self.__data.theta0 * pi / 180) + self.__data.h10) * self.__data.x0 - self.__data.h14 * self.__data.z0
    
    #-------------------------------------#
    @property
    def p16(self) -> Vector:
        return self.__p16
    
    @p16.setter
    def p16(self, value: Vector) -> None:
        self.__p16 = value
    
    def calcP16(self) -> None:
        self.p16 = - self.__data.h7 * cos(self.__data.theta0 * pi / 180) * self.__data.x0 - self.__data.h15 * self.__data.z0
    
    #-------------------------------------#
    @property
    def p17(self) -> Vector:
        return self.__p17
    
    @p17.setter
    def p17(self, value: Vector) -> None:
        self.__p17 = value
    
    def calcP17(self) -> None:
        self.p17 = - self.__data.h16 * self.__data.z0 + self.__data.h1 * self.__data.x0
    
    #-------------------------------------#
    @property
    def p18(self) -> Vector:
        return self.__p18
    
    @p18.setter
    def p18(self, value: Vector) -> None:
        self.__p18 = value
    
    def calcP18(self) -> None:
        self.p18 = self.__data.h8 * self.__data.x0 - self.__data.h9 * self.__data.z0
    
    #-------------------------------------#
    @property
    def c9e(self) -> Vector:
        return self.__c9e
    
    @c9e.setter
    def c9e(self, value: Vector) -> None:
        self.__c9e = value
    
    def calcC9e(self) -> None:
        v = self.__wing.p1e - self.p9e
        self.c9e = self.p9e + (1 / 3) * v + vector.norm(v) * (self.__data.delta7 * self.__data.x0 + self.__data.delta8 * self.__data.y0)
    
    #-------------------------------------#
    @property
    def c9d(self) -> Vector:
        return self.__c9d
    
    @c9d.setter
    def c9d(self, value: Vector) -> None:
        self.__c9d = value
    
    def calcC9d(self) -> None:
        v = self.__wing.p1d - self.p9d
        self.c9d = self.p9d + (1 / 3) * v + vector.norm(v) * (self.__data.delta7 * self.__data.x0 - self.__data.delta8 * self.__data.y0)
    
    #-------------------------------------#
    @property
    def c10e(self) -> Vector:
        return self.__c10e
    
    @c10e.setter
    def c10e(self, value: Vector) -> None:
        self.__c10e = value
    
    def calcC10e(self) -> None:
        v = self.__wing.p1e - self.p9e
        self.c10e = self.p9e + (2 / 3) * v + vector.norm(v) * (self.__data.delta7 * self.__data.x0 + self.__data.delta8 * self.__data.y0)
    
    #-------------------------------------#
    @property
    def c10d(self) -> Vector:
        return self.__c10d
    
    @c10d.setter
    def c10d(self, value: Vector) -> None:
        self.__c10d = value
    
    def calcC10d(self) -> None:
        v = self.__wing.p1d - self.p9d
        self.c10d = self.p9d + (2 / 3) * v + vector.norm(v) * (self.__data.delta7 * self.__data.x0 - self.__data.delta8 * self.__data.y0)
    
    #-------------------------------------#
    @property
    def c11e(self) -> Vector:
        return self.__c11e
    
    @c11e.setter
    def c11e(self, value: Vector) -> None:
        self.__c11e = value
    
    def calcC11e(self) -> None:
        v = self.p10e - self.__wing.p8e
        self.c11e = self.__wing.p8e + (1 / 3) * v + vector.norm(v) * (-self.__data.delta11 * self.__data.x0 + self.__data.delta12 * self.__data.y0)
    
    #-------------------------------------#
    @property
    def c11d(self) -> Vector:
        return self.__c11d
    
    @c11d.setter
    def c11d(self, value: Vector) -> None:
        self.__c11d = value
    
    def calcC11d(self) -> None:
        v = self.p10d - self.__wing.p8d
        self.c11d = self.__wing.p8d + (1 / 3) * v + vector.norm(v) * (-self.__data.delta11 * self.__data.x0 - self.__data.delta12 * self.__data.y0)
    
    #-------------------------------------#
    @property
    def c12e(self) -> Vector:
        return self.__c12e
    
    @c12e.setter
    def c12e(self, value: Vector) -> None:
        self.__c12e = value
    
    def calcC12e(self) -> None:
        v = self.p10e - self.__wing.p8e
        self.c12e = self.__wing.p8e + (2 / 3) * v + vector.norm(v) * (-self.__data.delta13 * self.__data.x0 + self.__data.delta14 * self.__data.y0)
    
    #-------------------------------------#
    @property
    def c12d(self) -> Vector:
        return self.__c12d
    
    @c12d.setter
    def c12d(self, value: Vector) -> None:
        self.__c12d = value
    
    def calcC12d(self) -> None:
        v = self.p10d - self.__wing.p8d
        self.c12d = self.__wing.p8d + (2 / 3) * v + vector.norm(v) * (-self.__data.delta13 * self.__data.x0 - self.__data.delta14 * self.__data.y0)
    
    #-------------------------------------#
    @property
    def c13(self) -> Vector:
        return self.__c13
    
    @c13.setter
    def c13(self, value: Vector) -> None:
        self.__c13 = value
    
    def calcC13(self) -> None:
        v = self.p12 - self.p11
        self.c13 = self.p11 + (1 / 3) * v + vector.norm(v) * (self.__data.delta15 * self.__data.x0 + self.__data.delta16 * self.__data.z0)
    
    #-------------------------------------#
    @property
    def c14(self) -> Vector:
        return self.__c14
    
    @c14.setter
    def c14(self, value: Vector) -> None:
        self.__c14 = value
    
    def calcC14(self) -> None:
        v = self.p12 - self.p11
        self.c14 = self.p11 + (2 / 3) * v + vector.norm(v) * (self.__data.delta17 * self.__data.x0 + self.__data.delta18 * self.__data.z0)
    
    #-------------------------------------#
    @property
    def c15(self) -> Vector:
        return self.__c15
    
    @c15.setter
    def c15(self, value: Vector) -> None:
        self.__c15 = value
    
    def calcC15(self) -> None:
        v = self.p13 - self.p12
        self.c15 = self.p12 + (1 / 3) * v + vector.norm(v) * (self.__data.delta19 * self.__data.x0 + self.__data.delta20 * self.__data.z0)
    
    #-------------------------------------#
    @property
    def c16(self) -> Vector:
        return self.__c16
    
    @c16.setter
    def c16(self, value: Vector) -> None:
        self.__c16 = value
    
    def calcC16(self) -> None:
        v = self.p13 - self.p12
        self.c16 = self.p12 + (2 / 3) * v + vector.norm(v) * (-self.__data.delta21 * self.__data.x0 + self.__data.delta22 * self.__data.z0)
    
    #-------------------------------------#
    @property
    def c17(self) -> Vector:
        return self.__c17
    
    @c17.setter
    def c17(self, value: Vector) -> None:
        self.__c17 = value
    
    def calcC17(self) -> None:
        v = self.p14 - self.p13
        self.c17 = self.p13 + (1 / 3) * v + vector.norm(v) * (-self.__data.delta23 * self.__data.x0 + self.__data.delta24 * self.__data.z0)
    
    #-------------------------------------#
    @property
    def c18(self) -> Vector:
        return self.__c18
    
    @c18.setter
    def c18(self, value: Vector) -> None:
        self.__c18 = value
    
    def calcC18(self) -> None:
        v = self.p14 - self.p13
        self.c18 = self.p13 + (2 / 3) * v + vector.norm(v) * (-self.__data.delta25 * self.__data.x0 + self.__data.delta26 * self.__data.z0)
    
    #-------------------------------------#
    @property
    def c19(self) -> Vector:
        return self.__c19
    
    @c19.setter
    def c19(self, value: Vector) -> None:
        self.__c19 = value
    
    def calcC19(self) -> None:
        v = self.p15 - self.p16
        self.c19 = self.p16 + (2 / 3) * v + vector.norm(v) * (-self.__data.delta27 * self.__data.x0 - self.__data.delta28 * self.__data.z0)
    
    #-------------------------------------#
    @property
    def c20(self) -> Vector:
        return self.__c20
    
    @c20.setter
    def c20(self, value: Vector) -> None:
        self.__c20 = value
    
    def calcC20(self) -> None:
        v = self.p15 - self.p16
        self.c20 = self.p16 + (1 / 3) * v + vector.norm(v) * (-self.__data.delta29 * self.__data.x0 - self.__data.delta30 * self.__data.z0)
    
    #-------------------------------------#
    @property
    def c21(self) -> Vector:
        return self.__c21
    
    @c21.setter
    def c21(self, value: Vector) -> None:
        self.__c21 = value
    
    def calcC21(self) -> None:
        v = self.p16 - self.p17
        self.c21 = self.p17 + (2 / 3) * v + vector.norm(v) * (-self.__data.delta31 * self.__data.x0 - self.__data.delta32 * self.__data.z0)
    
    #-------------------------------------#
    @property
    def c22(self) -> Vector:
        return self.__c22
    
    @c22.setter
    def c22(self, value: Vector) -> None:
        self.__c22 = value
    
    def calcC22(self) -> None:
        v = self.p16 - self.p17
        self.c22 = self.p17 + (1 / 3) * v + vector.norm(v) * (self.__data.delta33 * self.__data.x0 - self.__data.delta34 * self.__data.z0)
    
    #-------------------------------------#
    @property
    def c23(self) -> Vector:
        return self.__c23
    
    @c23.setter
    def c23(self, value: Vector) -> None:
        self.__c23 = value
    
    def calcC23(self) -> None:
        v = self.p17 - self.p18
        self.c23 = self.p18 + (2 / 3) * v + vector.norm(v) * (self.__data.delta35 * self.__data.x0 - self.__data.delta36 * self.__data.z0)
    
    #-------------------------------------#
    @property
    def c24(self) -> Vector:
        return self.__c24
    
    @c24.setter
    def c24(self, value: Vector) -> None:
        self.__c24 = value
    
    def calcC24(self) -> None:
        v = self.p17 - self.p18
        self.c24 = self.p18 + (1 / 3) * v + vector.norm(v) * (self.__data.delta37 * self.__data.x0 - self.__data.delta38 * self.__data.z0)
    
    #-------------------------------------#
    @property
    def c25e(self) -> Vector:
        return self.__c25e
    
    @c25e.setter
    def c25e(self, value: Vector) -> None:
        self.__c25e = value
    
    def calcC25e(self) -> None:
        self.c25e = self.p12 + self.__data.delta39 * self.__data.l0 * self.__data.y0
    
    #-------------------------------------#
    @property
    def c25d(self) -> Vector:
        return self.__c25d
    
    @c25d.setter
    def c25d(self, value: Vector) -> None:
        self.__c25d = value
    
    def calcC25d(self) -> None:
        self.c25d = self.p12 - self.__data.delta39 * self.__data.l0 * self.__data.y0
    
    #-------------------------------------#
    @property
    def c26e(self) -> Vector:
        return self.__c26e
    
    @c26e.setter
    def c26e(self, value: Vector) -> None:
        self.__c26e = value
    
    def calcC26e(self) -> None:
        self.c26e = self.__wing.p1e + self.__data.delta40 * self.__data.h12 * self.__data.z0
    
    #-------------------------------------#
    @property
    def c26d(self) -> Vector:
        return self.__c26d
    
    @c26d.setter
    def c26d(self, value: Vector) -> None:
        self.__c26d = value
    
    def calcC26d(self) -> None:
        self.c26d = self.__wing.p1d + self.__data.delta40 * self.__data.h12 * self.__data.z0
    
    #-------------------------------------#
    @property
    def c27e(self) -> Vector:
        return self.__c27e
    
    @c27e.setter
    def c27e(self, value: Vector) -> None:
        self.__c27e = value
    
    def calcC27e(self) -> None:
        self.c27e = self.__wing.p1e - self.__data.delta41 * self.__data.h16 * self.__data.z0
    
    #-------------------------------------#
    @property
    def c27d(self) -> Vector:
        return self.__c27d
    
    @c27d.setter
    def c27d(self, value: Vector) -> None:
        self.__c27d = value
    
    def calcC27d(self) -> None:
        self.c27d = self.__wing.p1d - self.__data.delta41 * self.__data.h16 * self.__data.z0
    
    #-------------------------------------#
    @property
    def c28e(self) -> Vector:
        return self.__c28e
    
    @c28e.setter
    def c28e(self, value: Vector) -> None:
        self.__c28e = value
    
    def calcC28e(self) -> None:
        self.c28e = self.p17 + self.__data.delta42 * self.__data.l0 * self.__data.y0
    
    #-------------------------------------#
    @property
    def c28d(self) -> Vector:
        return self.__c28d
    
    @c28d.setter
    def c28d(self, value: Vector) -> None:
        self.__c28d = value
    
    def calcC28d(self) -> None:
        self.c28d = self.p17 - self.__data.delta42 * self.__data.l0 * self.__data.y0
    
    #-------------------------------------#
    @property
    def c29e(self) -> Vector:
        return self.__c29e
    
    @c29e.setter
    def c29e(self, value: Vector) -> None:
        self.__c29e = value
    
    def calcC29e(self) -> None:
        self.c29e = self.p13 + self.__data.delta43 * vector.dot(self.__wing.p8e, self.__data.y0) * self.__data.y0
    
    #-------------------------------------#
    @property
    def c29d(self) -> Vector:
        return self.__c29d
    
    @c29d.setter
    def c29d(self, value: Vector) -> None:
        self.__c29d = value
    
    def calcC29d(self) -> None:
        self.c29d = self.p13 - self.__data.delta43 * vector.dot(self.__wing.p8e, self.__data.y0) * self.__data.y0
    
    #-------------------------------------#
    @property
    def c30e(self) -> Vector:
        return self.__c30e
    
    @c30e.setter
    def c30e(self, value: Vector) -> None:
        self.__c30e = value
    
    def calcC30e(self) -> None:
        self.c30e = self.__wing.p8e + self.__data.delta44 * self.__data.h13 * self.__data.z0
    
    #-------------------------------------#
    @property
    def c30d(self) -> Vector:
        return self.__c30d
    
    @c30d.setter
    def c30d(self, value: Vector) -> None:
        self.__c30d = value
    
    def calcC30d(self) -> None:
        self.c30d = self.__wing.p8d + self.__data.delta44 * self.__data.h13 * self.__data.z0
    
    #-------------------------------------#
    @property
    def c31e(self) -> Vector:
        return self.__c31e
    
    @c31e.setter
    def c31e(self, value: Vector) -> None:
        self.__c31e = value
    
    def calcC31e(self) -> None:
        self.c31e = self.__wing.p8e - self.__data.delta45 * self.__data.h15 * self.__data.z0
    
    #-------------------------------------#
    @property
    def c31d(self) -> Vector:
        return self.__c31d
    
    @c31d.setter
    def c31d(self, value: Vector) -> None:
        self.__c31d = value
    
    def calcC31d(self) -> None:
        self.c31d = self.__wing.p8d - self.__data.delta45 * self.__data.h15 * self.__data.z0
    
    #-------------------------------------#
    @property
    def c32e(self) -> Vector:
        return self.__c32e
    
    @c32e.setter
    def c32e(self, value: Vector) -> None:
        self.__c32e = value
    
    def calcC32e(self) -> None:
        self.c32e = self.p16 + self.__data.delta46 * vector.dot(self.__wing.p8e, self.__data.y0) * self.__data.y0
    
    #-------------------------------------#
    @property
    def c32d(self) -> Vector:
        return self.__c32d
    
    @c32d.setter
    def c32d(self, value: Vector) -> None:
        self.__c32d = value
    
    def calcC32d(self) -> None:
        self.c32d = self.p16 - self.__data.delta46 * vector.dot(self.__wing.p8e, self.__data.y0) * self.__data.y0
    
    #########################################################
    # Curves
    #########################################################

    #-------------------------------------#
    @property
    def curve15e(self) -> Curve:
        return self.__curve15e
    
    @curve15e.setter
    def curve15e(self, value: Curve) -> None:
        self.__curve15e = value
    
    def calcCurve15e(self) -> None:
        n = 50
        out = curve.bezier([self.p9e, self.c9e, self.c10e, self.__wing.p1e], n=n)
        self.curve15e = out
    
    #-------------------------------------#
    @property
    def curve15d(self) -> Curve:
        return self.__curve15d
    
    @curve15d.setter
    def curve15d(self, value: Curve) -> None:
        self.__curve15d = value
    
    def calcCurve15d(self) -> None:
        n = 50
        out = curve.bezier([self.p9d, self.c9d, self.c10d, self.__wing.p1d], n=n)
        self.curve15d = out
    
    #-------------------------------------#
    @property
    def curve16e(self) -> Curve:
        return self.__curve16e
    
    @curve16e.setter
    def curve16e(self, value: Curve) -> None:
        self.__curve16e = value
    
    def calcCurve16e(self) -> None:
        n = 50
        out = curve.bezier([self.__wing.p8e, self.c11e, self.c12e, self.p10e], n=n)
        self.curve16e = out
    
    #-------------------------------------#
    @property
    def curve16d(self) -> Curve:
        return self.__curve16d
    
    @curve16d.setter
    def curve16d(self, value: Curve) -> None:
        self.__curve16d = value
    
    def calcCurve16d(self) -> None:
        n = 50
        out = curve.bezier([self.__wing.p8d, self.c11d, self.c12d, self.p10d], n=n)
        self.curve16d = out
    
    #-------------------------------------#
    @property
    def curve17(self) -> Curve:
        return self.__curve17
    
    @curve17.setter
    def curve17(self, value: Curve) -> None:
        self.__curve17 = value
    
    def calcCurve17(self) -> None:
        n = 50
        out = curve.bezier([self.p11, self.c13, self.c14, self.p12], n=n)
        self.curve17 = out
    
    #-------------------------------------#
    @property
    def curve18(self) -> Curve:
        return self.__curve18
    
    @curve18.setter
    def curve18(self, value: Curve) -> None:
        self.__curve18 = value
    
    def calcCurve18(self) -> None:
        n = 50
        out = curve.bezier([self.p12, self.c15, self.c16, self.p13], n=n)
        self.curve18 = out
    
    #-------------------------------------#
    @property
    def curve19(self) -> Curve:
        return self.__curve19
    
    @curve19.setter
    def curve19(self, value: Curve) -> None:
        self.__curve19 = value
    
    def calcCurve19(self) -> None:
        n = 50
        out = curve.bezier([self.p13, self.c17, self.c18, self.p14], n=n)
        self.curve19 = out
    
    #-------------------------------------#
    @property
    def curve20(self) -> Curve:
        return self.__curve20
    
    @curve20.setter
    def curve20(self, value: Curve) -> None:
        self.__curve20 = value
    
    def calcCurve20(self) -> None:
        n = 50
        out = curve.bezier([self.p15, self.c19, self.c20, self.p16], n=n)
        self.curve20 = out
    
    #-------------------------------------#
    @property
    def curve21(self) -> Curve:
        return self.__curve21
    
    @curve21.setter
    def curve21(self, value: Curve) -> None:
        self.__curve21 = value
    
    def calcCurve21(self) -> None:
        n = 50
        out = curve.bezier([self.p16, self.c21, self.c22, self.p17], n=n)
        self.curve21 = out
    
    #-------------------------------------#
    @property
    def curve22(self) -> Curve:
        return self.__curve22
    
    @curve22.setter
    def curve22(self, value: Curve) -> None:
        self.__curve22 = value
    
    def calcCurve22(self) -> None:
        n = 50
        out = curve.bezier([self.p17, self.c23, self.c24, self.p18], n=n)
        self.curve22 = out
    
    #-------------------------------------#
    @property
    def curve23e(self) -> Curve:
        return self.__curve23e
    
    @curve23e.setter
    def curve23e(self, value: Curve) -> None:
        self.__curve23e = value
    
    def calcCurve23e(self) -> None:
        n = 50
        out = curve.bezier([self.p12, self.c25e, self.c26e, self.__wing.p1e], n=n)
        self.curve23e = out
    
    #-------------------------------------#
    @property
    def curve23d(self) -> Curve:
        return self.__curve23d
    
    @curve23d.setter
    def curve23d(self, value: Curve) -> None:
        self.__curve23d = value
    
    def calcCurve23d(self) -> None:
        n = 50
        out = curve.bezier([self.p12, self.c25d, self.c26d, self.__wing.p1d], n=n)
        self.curve23d = out
    
    #-------------------------------------#
    @property
    def curve24e(self) -> Curve:
        return self.__curve24e
    
    @curve24e.setter
    def curve24e(self, value: Curve) -> None:
        self.__curve24e = value
    
    def calcCurve24e(self) -> None:
        n = 50
        out = curve.bezier([self.__wing.p1e, self.c27e, self.c28e, self.p17], n=n)
        self.curve24e = out
    
    #-------------------------------------#
    @property
    def curve24d(self) -> Curve:
        return self.__curve24d
    
    @curve24d.setter
    def curve24d(self, value: Curve) -> None:
        self.__curve24d = value
    
    def calcCurve24d(self) -> None:
        n = 50
        out = curve.bezier([self.__wing.p1d, self.c27d, self.c28d, self.p17], n=n)
        self.curve24d = out
    
    #-------------------------------------#
    @property
    def curve25e(self) -> Curve:
        return self.__curve25e
    
    @curve25e.setter
    def curve25e(self, value: Curve) -> None:
        self.__curve25e = value
    
    def calcCurve25e(self) -> None:
        n = 50
        out = curve.bezier([self.p13, self.c29e, self.c30e, self.__wing.p8e], n=n)
        self.curve25e = out
    
    #-------------------------------------#
    @property
    def curve25d(self) -> Curve:
        return self.__curve25d
    
    @curve25d.setter
    def curve25d(self, value: Curve) -> None:
        self.__curve25d = value
    
    def calcCurve25d(self) -> None:
        n = 50
        out = curve.bezier([self.p13, self.c29d, self.c30d, self.__wing.p8d], n=n)
        self.curve25d = out
    
    #-------------------------------------#
    @property
    def curve26e(self) -> Curve:
        return self.__curve26e
    
    @curve26e.setter
    def curve26e(self, value: Curve) -> None:
        self.__curve26e = value
    
    def calcCurve26e(self) -> None:
        n = 50
        out = curve.bezier([self.__wing.p8e, self.c31e, self.c32e, self.p16], n=n)
        self.curve26e = out
    
    #-------------------------------------#
    @property
    def curve26d(self) -> Curve:
        return self.__curve26d
    
    @curve26d.setter
    def curve26d(self, value: Curve) -> None:
        self.__curve26d = value
    
    def calcCurve26d(self) -> None:
        n = 50
        out = curve.bezier([self.__wing.p8d, self.c31d, self.c32d, self.p16], n=n)
        self.curve26d = out
    
    #-------------------------------------#
    @property
    def curve27(self) -> Curve:
        return self.__curve27
    
    @curve27.setter
    def curve27(self, value: Curve) -> None:
        self.__curve27 = value
    
    def calcCurve27(self) -> None:
        n = 50
        out = curve.oneQuarterCurve([self.p11, self.p9e, 0.5 * (self.p9e + self.p9d)], n=n)
        self.curve27 = out
    
    #-------------------------------------#
    @property
    def curve28(self) -> Curve:
        return self.__curve28
    
    @curve28.setter
    def curve28(self, value: Curve) -> None:
        self.__curve28 = value
    
    def calcCurve28(self) -> None:
        n = 50
        out = curve.oneQuarterCurve([self.p9e, self.p18, 0.5 * (self.p9e + self.p9d)], n=n)
        self.curve28 = out
    
    #-------------------------------------#
    @property
    def curve29(self) -> Curve:
        return self.__curve29
    
    @curve29.setter
    def curve29(self, value: Curve) -> None:
        self.__curve29 = value
    
    def calcCurve29(self) -> None:
        n = 50
        out = curve.oneQuarterCurve([self.p18, self.p9d, 0.5 * (self.p9e + self.p9d)], n=n)
        self.curve29 = out
    
    #-------------------------------------#
    @property
    def curve30(self) -> Curve:
        return self.__curve30
    
    @curve30.setter
    def curve30(self, value: Curve) -> None:
        self.__curve30 = value
    
    def calcCurve30(self) -> None:
        n = 50
        out = curve.oneQuarterCurve([self.p9d, self.p11, 0.5 * (self.p9e + self.p9d)], n=n)
        self.curve30 = out
    
    #-------------------------------------#
    @property
    def curve31(self) -> Curve:
        return self.__curve31
    
    @curve31.setter
    def curve31(self, value: Curve) -> None:
        self.__curve31 = value
    
    def calcCurve31(self) -> None:
        n = 50
        out = curve.oneQuarterCurve([self.p14, self.p10e, 0.5 * (self.p10e + self.p10d)], n=n)
        self.curve31 = out
    
    #-------------------------------------#
    @property
    def curve32(self) -> Curve:
        return self.__curve32
    
    @curve32.setter
    def curve32(self, value: Curve) -> None:
        self.__curve32 = value
    
    def calcCurve32(self) -> None:
        n = 50
        out = curve.oneQuarterCurve([self.p10e, self.p15, 0.5 * (self.p10e + self.p10d)], n=n)
        self.curve32 = out
    
    #-------------------------------------#
    @property
    def curve33(self) -> Curve:
        return self.__curve33
    
    @curve33.setter
    def curve33(self, value: Curve) -> None:
        self.__curve33 = value
    
    def calcCurve33(self) -> None:
        n = 50
        out = curve.oneQuarterCurve([self.p15, self.p10d, 0.5 * (self.p10e + self.p10d)], n=n)
        self.curve33 = out
    
    #-------------------------------------#
    @property
    def curve34(self) -> Curve:
        return self.__curve34
    
    @curve34.setter
    def curve34(self, value: Curve) -> None:
        self.__curve34 = value
    
    def calcCurve34(self) -> None:
        n = 50
        out = curve.oneQuarterCurve([self.p10d, self.p14, 0.5 * (self.p10e + self.p10d)], n=n)
        self.curve34 = out