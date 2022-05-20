from cmath import cos
from numpy import asarray
from numpy.linalg import norm
from scipy.spatial.transform import Rotation as R
from math import sin, cos

from pybird.geometry.utilities.constants import Vector

class FinalParameters:
    
    def __init__(self, data: dict) -> None:
        self._data = data
        return
    
    def updateData(self, value: dict) -> None:
        self._data = value
        return
    
    @property
    def p1_e(self) -> Vector:
        x0 = asarray(self._data['x0'])
        y0 = asarray(self._data['y0'])
        l5 = self._data['l5']
        l1 = self._data['l1']
        return l5 * x0 + 0.5 * l1 * y0
    
    @property
    def p1_d(self) -> Vector:
        x0 = asarray(self._data['x0'])
        y0 = asarray(self._data['y0'])
        l5 = self._data['l5']
        l1 = self._data['l1']
        return l5 * x0 - 0.5 * l1 * y0
    
    @property
    def p2_e(self) -> Vector:
        x0 = asarray(self._data['x0'])
        y0 = asarray(self._data['y0'])
        l6 = self._data['l6']
        l3 = self._data['l3']
        l2 = self._data['l2']
        delta0 = self._data['delta0']
        inci_angle = self._data['inci_angle_left']
        s, c = sin(inci_angle / 2), cos(inci_angle / 2)

        rot = R.from_quat([-y0[0] * s, -y0[1] * s, -y0[2] * s, c])

        p0 = - delta0 * x0 + ( (l3 - l2) * delta0 / l6  + l2) * y0
        v = l2 * y0 - p0

        return p0 + asarray(rot.apply(v))
    
    @property
    def p2_d(self) -> Vector:
        x0 = asarray(self._data['x0'])
        y0 = asarray(self._data['y0'])
        l6 = self._data['l6']
        l3 = self._data['l3']
        l2 = self._data['l2']
        delta0 = self._data['delta0']
        inci_angle = self._data['inci_angle_right']
        s, c = sin(inci_angle / 2), cos(inci_angle / 2)

        rot = R.from_quat([-y0[0] * s, -y0[1] * s, -y0[2] * s, c])

        p0 = - delta0 * x0 - ( (l3 - l2) * delta0 / l6  + l2) * y0
        v = - l2 * y0 - p0

        return p0 + asarray(rot.apply(v))
    
    @property
    def p3_e(self) -> Vector:
        x0 = asarray(self._data['x0'])
        y0 = asarray(self._data['y0'])
        l6 = self._data['l6']
        l3 = self._data['l3']
        l2 = self._data['l2']
        delta0 = self._data['delta0']
        inci_angle = self._data['inci_angle_left']
        s, c = sin(inci_angle / 2), cos(inci_angle / 2)

        rot = R.from_quat([-y0[0] * s, -y0[1] * s, -y0[2] * s, c])

        p0 = - delta0 * x0 + ( (l3 - l2) * delta0 / l6  + l2) * y0
        v = l3 * y0 - l6 * x0 - p0

        return p0 + asarray(rot.apply(v))
    
    @property
    def p3_d(self) -> Vector:
        x0 = asarray(self._data['x0'])
        y0 = asarray(self._data['y0'])
        l6 = self._data['l6']
        l3 = self._data['l3']
        l2 = self._data['l2']
        delta0 = self._data['delta0']
        inci_angle = self._data['inci_angle_left']
        s, c = sin(inci_angle / 2), cos(inci_angle / 2)

        rot = R.from_quat([-y0[0] * s, -y0[1] * s, -y0[2] * s, c])

        p0 = - delta0 * x0 - ( (l3 - l2) * delta0 / l6  + l2) * y0
        v = - l3 * y0 - l6 * x0 - p0

        return p0 + asarray(rot.apply(v))

    @property
    def p4_e(self) -> Vector:
        x0 = asarray(self._data['x0'])
        y0 = asarray(self._data['y0'])
        l7 = self._data['l7']
        l6 = self._data['l6']
        l4 = self._data['l4']
        return - (l6 + l7) * x0 + 0.5 * l4 * y0
    
    @property
    def p4_d(self) -> Vector:
        x0 = asarray(self._data['x0'])
        y0 = asarray(self._data['y0'])
        l7 = self._data['l7']
        l6 = self._data['l6']
        l4 = self._data['l4']
        return - (l6 + l7) * x0 - 0.5 * l4 * y0
    
    @property
    def p5(self) -> Vector:
        x0 = asarray(self._data['x0'])
        z0 = asarray(self._data['z0'])
        l5 = self._data['l5']
        l1 = self._data['l1']
        return l5 * x0 + 0.5 * l1 * z0
    
    @property
    def p6(self) -> Vector:
        z0 = asarray(self._data['z0'])
        l8 = self._data['l8']
        return l8 * z0
    
    @property
    def p7(self) -> Vector:
        x0 = asarray(self._data['x0'])
        z0 = asarray(self._data['z0'])
        l10 = self._data['l10']
        l6 = self._data['l6']
        return - l6 * x0 + l10 * z0
    
    @property
    def p8(self) -> Vector:
        x0 = asarray(self._data['x0'])
        # z0 = asarray(self._data['z0'])
        z4 = asarray(self._data['z4'])
        l12 = self._data['l12']
        l7 = self._data['l7']
        l6 = self._data['l6']
        return - (l6 + l7) * x0 + 0.5 * l12 * z4
    
    @property
    def p9(self) -> Vector:
        x0 = asarray(self._data['x0'])
        z0 = asarray(self._data['z0'])
        l5 = self._data['l5']
        l1 = self._data['l1']
        return l5 * x0 - 0.5 * l1 * z0
    
    @property
    def p10(self) -> Vector:
        z0 = asarray(self._data['z0'])
        l9 = self._data['l9']
        return - l9 * z0
    
    @property
    def p11(self) -> Vector:
        x0 = asarray(self._data['x0'])
        z0 = asarray(self._data['z0'])
        l11 = self._data['l11']
        l6 = self._data['l6']
        return - l6 * x0 - l11 * z0
    
    @property
    def p12(self) -> Vector:
        x0 = asarray(self._data['x0'])
        z4 = asarray(self._data['z4'])
        l12 = self._data['l12']
        l7 = self._data['l7']
        l6 = self._data['l6']
        return - (l6 + l7) * x0 - 0.5 * l12 * z4
    
    @property
    def p13_e(self) -> Vector:
        y1_e = asarray(self._data['y1_left'])
        y2_e = asarray(self._data['y2_left'])
        l13 = self._data['l13']
        l14 = self._data['l14']
        delta49 = self._data['delta49']
        return self.p2_e + l13 * y1_e + (l14 - delta49) * y2_e
    
    @property
    def p13_d(self) -> Vector:
        y1_d = asarray(self._data['y1_right'])
        y2_d = asarray(self._data['y2_right'])
        l13 = self._data['l13']
        l14 = self._data['l14']
        delta49 = self._data['delta49']
        return self.p2_d - l13 * y1_d - (l14 - delta49) * y2_d
    
    @property
    def p14_e(self) -> Vector:
        y1_e = asarray(self._data['y1_left'])
        y2_e = asarray(self._data['y2_left'])
        y3_e = asarray(self._data['y3_left'])
        l13 = self._data['l13']
        l14 = self._data['l14']
        delta49 = self._data['delta49']
        return self.p2_e + l13 * y1_e + l14 * y2_e + delta49 * y3_e
    
    @property
    def p14_d(self) -> Vector:
        y1_d = asarray(self._data['y1_right'])
        y2_d = asarray(self._data['y2_right'])
        y3_d = asarray(self._data['y3_right'])
        l13 = self._data['l13']
        l14 = self._data['l14']
        delta49 = self._data['delta49']
        return self.p2_d - l13 * y1_d - l14 * y2_d - delta49 * y3_d
    
    @property
    def p15_e(self) -> Vector:
        y1_e = asarray(self._data['y1_left'])
        y2_e = asarray(self._data['y2_left'])
        y3_e = asarray(self._data['y3_left'])
        x3_e = asarray(self._data['x3_left'])
        l13 = self._data['l13']
        l14 = self._data['l14']
        l15 = self._data['l15'] 
        delta50 = self._data['delta50']
        delta51 = self._data['delta51']
        return self.p2_e + l13 * y1_e + l14 * y2_e + (l15 + delta50) * y3_e - delta51 * x3_e
    
    @property
    def p15_d(self) -> Vector:
        y1_d = asarray(self._data['y1_right'])
        y2_d = asarray(self._data['y2_right'])
        y3_d = asarray(self._data['y3_right'])
        x3_d = asarray(self._data['x3_right'])
        l13 = self._data['l13']
        l14 = self._data['l14']
        l15 = self._data['l15'] 
        delta50 = self._data['delta50']
        delta51 = self._data['delta51']
        return self.p2_d - l13 * y1_d - l14 * y2_d - (l15 + delta50) * y3_d - delta51 * x3_d
    
    @property
    def p16_e(self) -> Vector:
        x3_e = asarray(self._data['x3_left'])
        x2_e = asarray(self._data['x2_tip_left'])
        delta52 = self._data['delta52']
        return self.p14_e - delta52 * ((x2_e + x3_e) / norm(x2_e + x3_e))
    
    @property
    def p16_d(self) -> Vector:
        x3_d = asarray(self._data['x3_right'])
        x2_d = asarray(self._data['x2_tip_right'])
        delta52 = self._data['delta52']
        return self.p14_d - delta52 * ((x2_d + x3_d) / norm(x2_d + x3_d))
    
    @property
    def p17_e(self) -> Vector:
        x3_e = asarray(self._data['x3_left'])
        x2_e = asarray(self._data['x2_tip_left'])
        delta52 = self._data['delta52']
        return self.p13_e - delta52 * ((x2_e + x3_e) / norm(x2_e + x3_e))
    
    @property
    def p17_d(self) -> Vector:
        x3_d = asarray(self._data['x3_right'])
        x2_d = asarray(self._data['x2_tip_right'])
        delta52 = self._data['delta52']
        return self.p13_d - delta52 * ((x2_d + x3_d) / norm(x2_d + x3_d))
    
    @property
    def c1_e(self) -> Vector:
        x0 = asarray(self._data['x0'])
        y0 = asarray(self._data['y0'])
        delta1 = self._data['delta1']
        delta2 = self._data['delta2']
        return self.p2_e + 2 * (self.p1_e - self.p2_e) / 3 + delta1 * x0 + delta2 * y0
    
    @property
    def c1_d(self) -> Vector:
        x0 = asarray(self._data['x0'])
        y0 = asarray(self._data['y0'])
        delta1 = self._data['delta1']
        delta2 = self._data['delta2']
        return self.p2_d + 2 * (self.p1_d - self.p2_d) / 3 + delta1 * x0 - delta2 * y0
    
    @property
    def c2_e(self) -> Vector:
        x0 = asarray(self._data['x0'])
        y0 = asarray(self._data['y0'])
        delta3 = self._data['delta3']
        delta4 = self._data['delta4']
        return self.p2_e + (self.p1_e - self.p2_e) / 3 + delta3 * x0 + delta4 * y0
    
    @property
    def c2_d(self) -> Vector:
        x0 = asarray(self._data['x0'])
        y0 = asarray(self._data['y0'])
        delta3 = self._data['delta3']
        delta4 = self._data['delta4']
        return self.p2_d + (self.p1_d - self.p2_d) / 3 + delta3 * x0 - delta4 * y0
    
    @property
    def c3_e(self) -> Vector:
        x0 = asarray(self._data['x0'])
        y0 = asarray(self._data['y0'])
        delta5 = self._data['delta5']
        delta6 = self._data['delta6']
        return self.p3_e + (self.p4_e - self.p3_e) / 3 + delta5 * x0 + delta6 * y0
    
    @property
    def c3_d(self) -> Vector:
        x0 = asarray(self._data['x0'])
        y0 = asarray(self._data['y0'])
        delta5 = self._data['delta5']
        delta6 = self._data['delta6']
        return self.p3_d + (self.p4_d - self.p3_d) / 3 + delta5 * x0 - delta6 * y0
    
    @property
    def c4_e(self) -> Vector:
        x0 = asarray(self._data['x0'])
        y0 = asarray(self._data['y0'])
        delta7 = self._data['delta7']
        delta8 = self._data['delta8']
        return self.p3_e + 2 * (self.p4_e - self.p3_e) / 3 + delta7 * x0 + delta8 * y0
    
    @property
    def c4_d(self) -> Vector:
        x0 = asarray(self._data['x0'])
        y0 = asarray(self._data['y0'])
        delta7 = self._data['delta7']
        delta8 = self._data['delta8']
        return self.p3_d + 2 * (self.p4_d - self.p3_d) / 3 + delta7 * x0 - delta8 * y0
    
    @property
    def c5(self) -> Vector:
        x0 = asarray(self._data['x0'])
        z0 = asarray(self._data['z0'])
        delta9 = self._data['delta9']
        delta10 = self._data['delta10']
        return self.p5 + (self.p6 - self.p5) / 3 + delta9 * x0 + delta10 * z0
    
    @property
    def c6(self) -> Vector:
        x0 = asarray(self._data['x0'])
        z0 = asarray(self._data['z0'])
        delta11 = self._data['delta11']
        delta12 = self._data['delta12']
        return self.p5 + 2 * (self.p6 - self.p5) / 3 + delta11 * x0 + delta12 * z0
    
    @property
    def c7(self) -> Vector:
        x0 = asarray(self._data['x0'])
        z0 = asarray(self._data['z0'])
        delta13 = self._data['delta13']
        delta14 = self._data['delta14']
        return self.p6 + (self.p7 - self.p6) / 3 + delta13 * x0 + delta14 * z0
    
    @property
    def c8(self) -> Vector:
        x0 = asarray(self._data['x0'])
        z0 = asarray(self._data['z0'])
        delta15 = self._data['delta15']
        delta16 = self._data['delta16']
        return self.p6 + 2 * (self.p7 - self.p6) / 3 + delta15 * x0 + delta16 * z0
    
    @property
    def c9(self) -> Vector:
        x0 = asarray(self._data['x0'])
        z0 = asarray(self._data['z0'])
        delta17 = self._data['delta17']
        delta18 = self._data['delta18']
        return self.p7 + (self.p8 - self.p7) / 3 + delta17 * x0 + delta18 * z0
    
    @property
    def c10(self) -> Vector:
        x0 = asarray(self._data['x0'])
        z0 = asarray(self._data['z0'])
        delta19 = self._data['delta19']
        delta20 = self._data['delta20']
        return self.p7 + 2 * (self.p8 - self.p7) / 3 + delta19 * x0 + delta20 * z0
    
    @property
    def c11(self) -> Vector:
        x0 = asarray(self._data['x0'])
        z0 = asarray(self._data['z0'])
        delta21 = self._data['delta21']
        delta22 = self._data['delta22']
        return self.p9 + (self.p10 - self.p9) / 3 + delta21 * x0 - delta22 * z0
    
    @property
    def c12(self) -> Vector:
        x0 = asarray(self._data['x0'])
        z0 = asarray(self._data['z0'])
        delta23 = self._data['delta23']
        delta24 = self._data['delta24']
        return self.p9 + 2 * (self.p10 - self.p9) / 3 + delta23 * x0 - delta24 * z0
    
    @property
    def c13(self) -> Vector:
        x0 = asarray(self._data['x0'])
        z0 = asarray(self._data['z0'])
        delta25 = self._data['delta25']
        delta26 = self._data['delta26']
        return self.p10 + (self.p11 - self.p10) / 3 + delta25 * x0 - delta26 * z0
    
    @property
    def c14(self) -> Vector:
        x0 = asarray(self._data['x0'])
        z0 = asarray(self._data['z0'])
        delta27 = self._data['delta27']
        delta28 = self._data['delta28']
        return self.p10 + 2 * (self.p11 - self.p10) / 3 + delta27 * x0 - delta28 * z0
    
    @property
    def c15(self) -> Vector:
        x0 = asarray(self._data['x0'])
        z0 = asarray(self._data['z0'])
        delta29 = self._data['delta29']
        delta30 = self._data['delta30']
        return self.p11 + (self.p12 - self.p11) / 3 + delta29 * x0 - delta30 * z0
    
    @property
    def c16(self) -> Vector:
        x0 = asarray(self._data['x0'])
        z0 = asarray(self._data['z0'])
        delta31 = self._data['delta31']
        delta32 = self._data['delta32']
        return self.p11 + 2 * (self.p12 - self.p11) / 3 + delta31 * x0 - delta32 * z0
    
    @property
    def c17_e(self) -> Vector:
        z0 = asarray(self._data['z0'])
        y0 = asarray(self._data['y0'])
        delta33 = self._data['delta33']
        delta34 = self._data['delta34']
        return self.p6 + (self.p2_e - self.p6) / 3 + delta33 * y0 + delta34 * z0
    
    @property
    def c17_d(self) -> Vector:
        z0 = asarray(self._data['z0'])
        y0 = asarray(self._data['y0'])
        delta33 = self._data['delta33']
        delta34 = self._data['delta34']
        return self.p6 + (self.p2_d - self.p6) / 3 - delta33 * y0 + delta34 * z0
    
    @property
    def c18_e(self) -> Vector:
        z0 = asarray(self._data['z0'])
        y0 = asarray(self._data['y0'])
        delta35 = self._data['delta35']
        delta36 = self._data['delta36']
        return self.p6 + 2 * (self.p2_e - self.p6) / 3 + delta35 * y0 + delta36 * z0
    
    @property
    def c18_d(self) -> Vector:
        z0 = asarray(self._data['z0'])
        y0 = asarray(self._data['y0'])
        delta35 = self._data['delta35']
        delta36 = self._data['delta36']
        return self.p6 + 2 * (self.p2_d - self.p6) / 3 - delta35 * y0 + delta36 * z0
    
    @property
    def c19_e(self) -> Vector:
        z0 = asarray(self._data['z0'])
        y0 = asarray(self._data['y0'])
        delta37 = self._data['delta37']
        delta38 = self._data['delta38']
        return self.p2_e + (self.p10 - self.p2_e) / 3 + delta37 * y0 + delta38 * z0
    
    @property
    def c19_d(self) -> Vector:
        z0 = asarray(self._data['z0'])
        y0 = asarray(self._data['y0'])
        delta37 = self._data['delta37']
        delta38 = self._data['delta38']
        return self.p2_d + (self.p10 - self.p2_d) / 3 - delta37 * y0 + delta38 * z0
    
    @property
    def c20_e(self) -> Vector:
        z0 = asarray(self._data['z0'])
        y0 = asarray(self._data['y0'])
        delta39 = self._data['delta39']
        delta40 = self._data['delta40']
        return self.p2_e + 2 * (self.p10 - self.p2_e) / 3 + delta39 * y0 + delta40 * z0
    
    @property
    def c20_d(self) -> Vector:
        z0 = asarray(self._data['z0'])
        y0 = asarray(self._data['y0'])
        delta39 = self._data['delta39']
        delta40 = self._data['delta40']
        return self.p2_d + 2 * (self.p10 - self.p2_d) / 3 - delta39 * y0 + delta40 * z0
    
    @property
    def c21_e(self) -> Vector:
        z0 = asarray(self._data['z0'])
        y0 = asarray(self._data['y0'])
        delta41 = self._data['delta41']
        delta42 = self._data['delta42']
        return self.p7 + (self.p3_e - self.p7) / 3 + delta41 * y0 + delta42 * z0
    
    @property
    def c21_d(self) -> Vector:
        z0 = asarray(self._data['z0'])
        y0 = asarray(self._data['y0'])
        delta41 = self._data['delta41']
        delta42 = self._data['delta42']
        return self.p7 + (self.p3_d - self.p7) / 3 - delta41 * y0 + delta42 * z0
    
    @property
    def c22_e(self) -> Vector:
        z0 = asarray(self._data['z0'])
        y0 = asarray(self._data['y0'])
        delta43 = self._data['delta43']
        delta44 = self._data['delta44']
        return self.p7 + 2 * (self.p3_e - self.p7) / 3 + delta43 * y0 + delta44 * z0
    
    @property
    def c22_d(self) -> Vector:
        z0 = asarray(self._data['z0'])
        y0 = asarray(self._data['y0'])
        delta43 = self._data['delta43']
        delta44 = self._data['delta44']
        return self.p7 + 2 * (self.p3_d - self.p7) / 3 - delta43 * y0 + delta44 * z0
    
    @property
    def c23_e(self) -> Vector:
        z0 = asarray(self._data['z0'])
        y0 = asarray(self._data['y0'])
        delta45 = self._data['delta45']
        delta46 = self._data['delta46']
        return self.p3_e + (self.p11 - self.p3_e) / 3 + delta45 * y0 + delta46 * z0
    
    @property
    def c23_d(self) -> Vector:
        z0 = asarray(self._data['z0'])
        y0 = asarray(self._data['y0'])
        delta45 = self._data['delta45']
        delta46 = self._data['delta46']
        return self.p3_d + (self.p11 - self.p3_d) / 3 - delta45 * y0 + delta46 * z0
    
    @property
    def c24_e(self) -> Vector:
        z0 = asarray(self._data['z0'])
        y0 = asarray(self._data['y0'])
        delta47 = self._data['delta47']
        delta48 = self._data['delta48']
        return self.p3_e + 2 * (self.p11 - self.p3_e) / 3 + delta47 * y0 + delta48 * z0
    
    @property
    def c24_d(self) -> Vector:
        z0 = asarray(self._data['z0'])
        y0 = asarray(self._data['y0'])
        delta47 = self._data['delta47']
        delta48 = self._data['delta48']
        return self.p3_d + 2 * (self.p11 - self.p3_d) / 3 - delta47 * y0 + delta48 * z0
    
    @property
    def c25_e(self) -> Vector:
        x1 = asarray(self._data['x1_left'])
        x2 = asarray(self._data['x2_base_left'])
        y1 = asarray(self._data['y1_left'])
        l13 = self._data['l13']
        delta53 = self._data['delta53']
        return self.p2_e + l13 * y1 + ((x1 + x2) / norm(x1 + x2)) * delta53
    
    @property
    def c25_d(self) -> Vector:
        x1 = asarray(self._data['x1_right'])
        x2 = asarray(self._data['x2_base_right'])
        y1 = asarray(self._data['y1_right'])
        l13 = self._data['l13']
        delta53 = self._data['delta53']
        return self.p2_d - l13 * y1 + ((x1 + x2) / norm(x1 + x2)) * delta53
    
    @property
    def c26_e(self) -> Vector:
        y1 = asarray(self._data['y1_left'])
        y2 = asarray(self._data['y2_left'])
        l13 = self._data['l13']
        l14 = self._data['l14']
        return self.p2_e + l13 * y1 + l14 * y2
    
    @property
    def c26_d(self) -> Vector:
        y1 = asarray(self._data['y1_right'])
        y2 = asarray(self._data['y2_right'])
        l13 = self._data['l13']
        l14 = self._data['l14']
        return self.p2_d - l13 * y1 - l14 * y2
    
    @property
    def c27_e(self) -> Vector:
        y1 = asarray(self._data['y1_left'])
        y2 = asarray(self._data['y2_left'])
        y3 = asarray(self._data['y3_left'])
        x3 = asarray(self._data['x3_left'])
        l13 = self._data['l13']
        l14 = self._data['l14']
        l15 = self._data['l15']
        delta54 = self._data['delta54']
        return self.p2_e + l13 * y1 + l14 * y2 + l15 * y3 - delta54 * x3
    
    @property
    def c27_d(self) -> Vector:
        y1 = asarray(self._data['y1_right'])
        y2 = asarray(self._data['y2_right'])
        y3 = asarray(self._data['y3_right'])
        x3 = asarray(self._data['x3_right'])
        l13 = self._data['l13']
        l14 = self._data['l14']
        l15 = self._data['l15']
        delta54 = self._data['delta54']
        return self.p2_d - l13 * y1 - l14 * y2 - l15 * y3 - delta54 * x3
    
    @property
    def c28_e(self) -> Vector:
        y3 = asarray(self._data['y3_left'])
        x3 = asarray(self._data['x3_left'])
        delta55 = self._data['delta55']
        delta56 = self._data['delta56']
        return 0.5 * (self.p15_e + self.p16_e) + delta55 * x3 + delta56 * y3
    
    @property
    def c28_d(self) -> Vector:
        y3 = asarray(self._data['y3_right'])
        x3 = asarray(self._data['x3_right'])
        delta55 = self._data['delta55']
        delta56 = self._data['delta56']
        return 0.5 * (self.p15_d + self.p16_d) + delta55 * x3 - delta56 * y3
    
    @property
    def c29_e(self) -> Vector:
        # x2 = asarray(self._data['x2_tip_left'])
        # x3 = asarray(self._data['x3_left'])
        # delta52 = self._data['delta52']
        return 0.5 * (self.p16_e + self.p17_e) # self.c26_e - ((x2 + x3) / norm(x2 + x3)) * delta52
    
    @property
    def c29_d(self) -> Vector:
        # x2 = asarray(self._data['x2_tip_right'])
        # x3 = asarray(self._data['x3_right'])
        # delta52 = self._data['delta52']
        return 0.5 * (self.p16_d + self.p17_d) # self.c26_d - ((x2 + x3) / norm(x2 + x3)) * delta52
    
    @property
    def c30_e(self) -> Vector:
        x1 = asarray(self._data['x1_left'])
        x2 = asarray(self._data['x2_base_left'])
        y1 = asarray(self._data['y1_left'])
        y2 = asarray(self._data['y2_left'])
        delta58 = self._data['delta58']
        delta59 = self._data['delta59']
        return 0.5 * (self.p17_e + self.p3_e) - delta58 * (x1 + x2) / norm(x1 + x2) + delta59 * (y1 + y2) / norm(y1 + y2)
    
    @property
    def c30_d(self) -> Vector:
        x1 = asarray(self._data['x1_right'])
        x2 = asarray(self._data['x2_base_right'])
        y1 = asarray(self._data['y1_right'])
        y2 = asarray(self._data['y2_right'])
        delta58 = self._data['delta58']
        delta59 = self._data['delta59']
        return 0.5 * (self.p17_d + self.p3_d) - delta58 * (x1 + x2) / norm(x1 + x2) - delta59 * (y1 + y2) / norm(y1 + y2)

    @property
    def p18(self) -> Vector:
        x4 = asarray(self._data['x4'])
        y4 = asarray(self._data['y4'])
        l16 = self._data['l16']
        l17 = self._data['l17']
        return (self.p4_e + self.p4_d) / 2 + l16 * x4 - 0.5 * l17 * y4
    
    @property
    def p19(self) -> Vector:
        x4 = asarray(self._data['x4'])
        y4 = asarray(self._data['y4'])
        l16 = self._data['l16']
        l17 = self._data['l17']
        return (self.p4_e + self.p4_d) / 2 + l16 * x4 + 0.5 * l17 * y4
    
    @property
    def p20_square(self) -> Vector:
        return (self.p18 + self.p19) / 2
    
    @property
    def p20_V(self) -> Vector:
        x4 = asarray(self._data['x4'])
        l16 = self._data['l16']
        l18 = self._data['l18']
        return (self.p4_e + self.p4_d) / 2 + (l16 - l18) * x4
    
    @property
    def p20_pointed(self) -> Vector:
        x4 = asarray(self._data['x4'])
        l16 = self._data['l16']
        l18 = self._data['l18']
        return (self.p4_e + self.p4_d) / 2 + (l16 + l18) * x4
    
    @property
    def p20_rounded(self) -> Vector:
        x4 = asarray(self._data['x4'])
        c31 = self.c31
        l18 = self._data['l18']
        return c31 + l18 * x4
    
    @property
    def c31(self) -> Vector:
        x4 = asarray(self._data['x4'])
        l16 = self._data['l16']
        l17 = self._data['l17']
        l18 = self._data['l18']
        return (self.p4_e + self.p4_d) / 2 + (l16 - (l18 ** 2 + (0.5 * l17) ** 2) ** 0.5) * x4
    
    @property
    def c32(self) -> Vector:
        x0 = asarray(self._data['x0'])
        l1 = self._data['l1']
        l5 = self._data['l5']
        l20 = self._data['l20']
        return (((0.5 * l20) ** 2 - (0.5 * l1) ** 2) ** 0.5 + l5) * x0
    
    @property
    def p21_e(self) -> Vector:
        x0 = asarray(self._data['x0'])
        y0 = asarray(self._data['y0'])
        l19 = self._data['l19']
        l20 = self._data['l20']
        return self.c32 + x0 * 0.25 * l20 * l20 / l19 + y0 * 0.5 * l20 * ((1 - (l20 / (2 * l19)) ** 2) ** 0.5)
    
    @property
    def p21_d(self) -> Vector:
        x0 = asarray(self._data['x0'])
        y0 = asarray(self._data['y0'])
        l19 = self._data['l19']
        l20 = self._data['l20']
        return self.c32 + x0 * 0.25 * l20 * l20 / l19 - y0 * 0.5 * l20 * ((1 - (l20 / (2 * l19)) ** 2) ** 0.5)
    
    @property
    def p23(self) -> Vector:
        x0 = asarray(self._data['x0'])
        l19 = self._data['l19']
        return self.c32 + x0 * l19
    