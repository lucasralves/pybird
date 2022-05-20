from pybird.geometry.utilities.body_final_params import BodyFinalParams
from pybird.geometry.utilities.data import Data
from pybird.helpers.type import Curve, Vector
from pybird.helpers import vector
from pybird.helpers import curve


class HeadFinalParams:

    def __init__(self, data: Data, body: BodyFinalParams) -> None:
        self.__data = data
        self.__body = body
        self.update()
    
    def update(self) -> None:
        self.calcP21e()
        self.calcP21d()
        self.calcP22()
        self.calcP23()
        self.calcP24()
        self.calcc36d()
        self.calcc36e()
        self.calcc37d()
        self.calcc37e()
        self.calcc38()
        self.calcc39()
        self.calcc40()
        self.calcc41()

        self.calcCurve39d()
        self.calcCurve39e()
        self.calcCurve40d()
        self.calcCurve40e()
        self.calcCurve41()
        self.calcCurve42()
        self.calcCurve43()
        self.calcCurve44()
        self.calcCurve45()
        self.calcCurve46()
        self.calcCurve47()
        self.calcCurve48()
    
    #########################################################
    # Control points
    #########################################################

    #-------------------------------------#
    @property
    def p21e(self) -> Vector:
        return self.__p21e
    
    @p21e.setter
    def p21e(self, value: Vector) -> None:
        self.__p21e = value
    
    def calcP21e(self) -> None:
        self.p21e = 0.5 * (self.__body.p9e + self.__body.p9d) + self.__data.h22 * self.__data.x0 + self.__data.h23 * self.__data.y0
    
    #-------------------------------------#
    @property
    def p21d(self) -> Vector:
        return self.__p21d
    
    @p21d.setter
    def p21d(self, value: Vector) -> None:
        self.__p21d = value
    
    def calcP21d(self) -> None:
        self.p21d = 0.5 * (self.__body.p9e + self.__body.p9d) + self.__data.h22 * self.__data.x0 - self.__data.h23 * self.__data.y0
    
    #-------------------------------------#
    @property
    def p23(self) -> Vector:
        return self.__p23
    
    @p23.setter
    def p23(self, value: Vector) -> None:
        self.__p23 = value
    
    def calcP23(self) -> None:
        self.p23 = 0.5 * (self.__body.p9e + self.__body.p9d) + self.__data.h22 * self.__data.x0 + self.__data.h23 * self.__data.z0
    
    #-------------------------------------#
    @property
    def p24(self) -> Vector:
        return self.__p24
    
    @p24.setter
    def p24(self, value: Vector) -> None:
        self.__p24 = value
    
    def calcP24(self) -> None:
        self.p24 = 0.5 * (self.__body.p9e + self.__body.p9d) + self.__data.h22 * self.__data.x0 - self.__data.h23 * self.__data.z0
    
    #-------------------------------------#
    @property
    def p22(self) -> Vector:
        return self.__p22
    
    @p22.setter
    def p22(self, value: Vector) -> None:
        self.__p22 = value
    
    def calcP22(self) -> None:
        self.p22 = 0.5 * (self.p21e + self.p21d) + self.__data.h24 * self.__data.x0
    
    #-------------------------------------#
    @property
    def c36e(self) -> Vector:
        return self.__c36e
    
    @c36e.setter
    def c36e(self, value: Vector) -> None:
        self.__c36e = value
    
    def calcc36e(self) -> None:
        self.c36e = self.__body.p9e + self.__data.delta49 * vector.norm(self.p21e - self.__body.p9e) * self.__data.x0
    
    #-------------------------------------#
    @property
    def c36d(self) -> Vector:
        return self.__c36d
    
    @c36d.setter
    def c36d(self, value: Vector) -> None:
        self.__c36d = value
    
    def calcc36d(self) -> None:
        self.c36d = self.__body.p9d + self.__data.delta49 * vector.norm(self.p21e - self.__body.p9e) * self.__data.x0
    
    #-------------------------------------#
    @property
    def c37e(self) -> Vector:
        return self.__c37e
    
    @c37e.setter
    def c37e(self, value: Vector) -> None:
        self.__c37e = value
    
    def calcc37e(self) -> None:
        self.c37e = self.p21e + self.__data.delta50 * vector.norm(self.p22 - self.p21e) * self.__data.x0
    
    #-------------------------------------#
    @property
    def c37d(self) -> Vector:
        return self.__c37d
    
    @c37d.setter
    def c37d(self, value: Vector) -> None:
        self.__c37d = value
    
    def calcc37d(self) -> None:
        self.c37d = self.p21d + self.__data.delta50 * vector.norm(self.p22 - self.p21d) * self.__data.x0
    
    #-------------------------------------#
    @property
    def c38(self) -> Vector:
        return self.__c38
    
    @c38.setter
    def c38(self, value: Vector) -> None:
        self.__c38 = value
    
    def calcc38(self) -> None:
        self.c38 = self.__body.p11 + self.__data.delta49 * vector.norm(self.p21e - self.__body.p9e) * self.__data.x0
    
    #-------------------------------------#
    @property
    def c39(self) -> Vector:
        return self.__c39
    
    @c39.setter
    def c39(self, value: Vector) -> None:
        self.__c39 = value
    
    def calcc39(self) -> None:
        self.c39 = self.__body.p18 + self.__data.delta49 * vector.norm(self.p21e - self.__body.p9e) * self.__data.x0

    #-------------------------------------#
    @property
    def c40(self) -> Vector:
        return self.__c40
    
    @c40.setter
    def c40(self, value: Vector) -> None:
        self.__c40 = value
    
    def calcc40(self) -> None:
        self.c40 = self.p23 + self.__data.delta50 * vector.norm(self.p22 - self.p23) * self.__data.x0
    
    #-------------------------------------#
    @property
    def c41(self) -> Vector:
        return self.__c41
    
    @c41.setter
    def c41(self, value: Vector) -> None:
        self.__c41 = value
    
    def calcc41(self) -> None:
        self.c41 = self.p24 + self.__data.delta50 * vector.norm(self.p22 - self.p23) * self.__data.x0
    

    #########################################################
    # Curves
    #########################################################

    #-------------------------------------#
    @property
    def curve39e(self) -> Curve:
        return self.__curve39e
    
    @curve39e.setter
    def curve39e(self, value: Curve) -> None:
        self.__curve39e = value
    
    def calcCurve39e(self) -> None:
        n = 50
        out = curve.bezier([self.__body.p9e, self.c36e, self.p21e], n=n)
        self.curve39e = out
    
    #-------------------------------------#
    @property
    def curve39d(self) -> Curve:
        return self.__curve39d
    
    @curve39d.setter
    def curve39d(self, value: Curve) -> None:
        self.__curve39d = value
    
    def calcCurve39d(self) -> None:
        n = 50
        out = curve.bezier([self.__body.p9d, self.c36d, self.p21d], n=n)
        self.curve39d = out
    
    #-------------------------------------#
    @property
    def curve40e(self) -> Curve:
        return self.__curve40e
    
    @curve40e.setter
    def curve40e(self, value: Curve) -> None:
        self.__curve40e = value
    
    def calcCurve40e(self) -> None:
        n = 50
        out = curve.bezier([self.p21e, self.c37e, self.p22], n=n)
        self.curve40e = out
    
    #-------------------------------------#
    @property
    def curve40d(self) -> Curve:
        return self.__curve40d
    
    @curve40d.setter
    def curve40d(self, value: Curve) -> None:
        self.__curve40d = value
    
    def calcCurve40d(self) -> None:
        n = 50
        out = curve.bezier([self.p21d, self.c37d, self.p22], n=n)
        self.curve40d = out
    
    #-------------------------------------#
    @property
    def curve41(self) -> Curve:
        return self.__curve41
    
    @curve41.setter
    def curve41(self, value: Curve) -> None:
        self.__curve41 = value
    
    def calcCurve41(self) -> None:
        n = 50
        out = curve.bezier([self.__body.p11, self.c38, self.p23], n=n)
        self.curve41 = out
    
    #-------------------------------------#
    @property
    def curve42(self) -> Curve:
        return self.__curve42
    
    @curve42.setter
    def curve42(self, value: Curve) -> None:
        self.__curve42 = value
    
    def calcCurve42(self) -> None:
        n = 50
        out = curve.bezier([self.__body.p18, self.c39, self.p24], n=n)
        self.curve42 = out
    
    #-------------------------------------#
    @property
    def curve43(self) -> Curve:
        return self.__curve43
    
    @curve43.setter
    def curve43(self, value: Curve) -> None:
        self.__curve43 = value
    
    def calcCurve43(self) -> None:
        n = 50
        out = curve.bezier([self.p23, self.c40, self.p22], n=n)
        self.curve43 = out
    
    #-------------------------------------#
    @property
    def curve44(self) -> Curve:
        return self.__curve44
    
    @curve44.setter
    def curve44(self, value: Curve) -> None:
        self.__curve44 = value
    
    def calcCurve44(self) -> None:
        n = 50
        out = curve.bezier([self.p24, self.c41, self.p22], n=n)
        self.curve44 = out
    
    #-------------------------------------#
    @property
    def curve45(self) -> Curve:
        return self.__curve45
    
    @curve45.setter
    def curve45(self, value: Curve) -> None:
        self.__curve45 = value
    
    def calcCurve45(self) -> None:
        n = 50
        out = curve.oneQuarterCurve([self.p23, self.p21e, 0.5 * (self.p21e + self.p21d)], n=n)
        self.curve45 = out
    
    #-------------------------------------#
    @property
    def curve46(self) -> Curve:
        return self.__curve46
    
    @curve46.setter
    def curve46(self, value: Curve) -> None:
        self.__curve46 = value
    
    def calcCurve46(self) -> None:
        n = 50
        out = curve.oneQuarterCurve([self.p21e, self.p24, 0.5 * (self.p21e + self.p21d)], n=n)
        self.curve46 = out
    
    #-------------------------------------#
    @property
    def curve47(self) -> Curve:
        return self.__curve47
    
    @curve47.setter
    def curve47(self, value: Curve) -> None:
        self.__curve47 = value
    
    def calcCurve47(self) -> None:
        n = 50
        out = curve.oneQuarterCurve([self.p24, self.p21d, 0.5 * (self.p21e + self.p21d)], n=n)
        self.curve47 = out
    
    #-------------------------------------#
    @property
    def curve48(self) -> Curve:
        return self.__curve48
    
    @curve48.setter
    def curve48(self, value: Curve) -> None:
        self.__curve48 = value
    
    def calcCurve48(self) -> None:
        n = 50
        out = curve.oneQuarterCurve([self.p21d, self.p23, 0.5 * (self.p21e + self.p21d)], n=n)
        self.curve48 = out