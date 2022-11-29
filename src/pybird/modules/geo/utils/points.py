from math import cos, fabs
from typing import List
from numpy import cross, deg2rad, dot, linspace, zeros, ndarray
from numpy.linalg import norm
from scipy.spatial.transform import Rotation as R

from pybird.modules.geo.utils.system import BaseSystem, TailSystem, WingSystem
from pybird.modules.geo.models.external import *
from pybird.modules.geo.models.convert import deg2RadConst
from pybird.modules.geo.utils import vector, bezier, circle

def l1(wing: WingModel, system: WingSystem, p0: ndarray) -> ndarray:
    p = p0 + wing.l1 * system.y1
    return p

def l2(wing: WingModel, system: WingSystem, l1: ndarray) -> ndarray:
    p = l1 + wing.l2 * system.y2Tip
    return p

def l3(wing: WingModel, system: WingSystem, l2: ndarray) -> ndarray:
    p = l2 + wing.l3 * system.y3
    return p

def p0(wing: WingModel, system: WingSystem) -> ndarray:
    p = wing.l0 * system.y0
    return p

def p1(wing: WingModel, system: WingSystem, p0: ndarray, isLeft: bool) -> ndarray:

    x, y, z = system.x0, system.y0, system.z0
    v = wing.h1 * system.x0
    
    if not (-1e-8 < wing.thetaRootZ < 1e-8):
        r1 = R.from_rotvec(deg2rad(wing.thetaRootZ) * z)
        v = r1.apply(v)
        x = r1.apply(x)
        y = r1.apply(y)

    if not (-1e-8 < wing.theta2_e if isLeft else wing.theta2_d < 1e-8):
        r2 = R.from_rotvec(-deg2rad(wing.theta2_e if isLeft else wing.theta2_d) * x)
        v = r2.apply(v)
        y = r2.apply(y)

    if not (-1e-8 < wing.thetaRootY < 1e-8):
        r3 = R.from_rotvec(-deg2rad(wing.thetaRootY) * y)
        v = r3.apply(v)
    
    p = p0 + v
    
    return p

def p2(p1: ndarray, aux1: ndarray, p3Line: ndarray) -> ndarray:
    p = 0.25 * (p1 + 2 * aux1 + p3Line)
    return p

def p3(wing: WingModel, system: WingSystem, l2: ndarray) -> ndarray:
    p = l2 - wing.h2 * system.y2Tip + wing.h3 * system.x2Tip
    return p

def p3Line(wing: WingModel, system: WingSystem, l2: ndarray) -> ndarray:
    p = l2 - wing.h2 * system.y2Tip + wing.h3 * system.x2Base
    return p

def p4(wing: WingModel, system: WingSystem, l2: ndarray) -> ndarray:
    p = l2 + wing.h2 * system.y3 + wing.h3 * system.x3
    return p

def p5(wing: WingModel, system: WingSystem, l3: ndarray) -> ndarray:
    p = l3 + wing.h3 * system.x3
    return p

def p6(p5: ndarray, aux2: ndarray, p7: ndarray, t: float) -> ndarray:
    p = bezier.quadratic([p5, aux2, p7], t)
    return p

def p7(wing: WingModel, system: WingSystem, p5: ndarray) -> ndarray:
    p = p5 - wing.h4 * system.x3 + wing.h5 * system.y3
    return p

def p8(p7: ndarray, aux3: ndarray, p10: ndarray, t: float) -> ndarray:
    p = bezier.quadratic([p7, aux3, p10], t)
    return p

def p9(p7: ndarray, aux3: ndarray, p10: ndarray, t: float) -> ndarray:
    p = bezier.quadratic([p7, aux3, p10], t)
    return p

def p10_11_aux(wing: WingModel, system: WingSystem, p4: ndarray, p3: ndarray) -> ndarray:
    pAux1 = p4 - wing.h6 * vector.unary(system.x2Tip + system.x3)
    pAux2 = p3 - wing.h6 * vector.unary(system.x2Tip + system.x3)
    p = 0.5 * (pAux1 + pAux2)
    return p

def p10(wing: WingModel, p10_11_aux: ndarray, p7: ndarray, aux3: ndarray) -> ndarray:
    t = wing.h2 / norm(p7 - p10_11_aux)
    p = bezier.quadratic([p10_11_aux, aux3, p7], t)
    return p

def p11(wing: WingModel, p10_11_aux: ndarray, p13: ndarray, aux4: ndarray) -> ndarray:
    t = wing.h2 / norm(p13 - p10_11_aux)
    p = bezier.quadratic([p10_11_aux, aux4, p13], t)
    return p

def p12(p11: ndarray, aux4: ndarray, p13: ndarray) -> ndarray:
    p = 0.25 * (p11 + 2 * aux4 + p13)
    return p

def p13(wing: WingModel, system: WingSystem, p0: ndarray, isLeft: bool) -> ndarray:
    
    x, y, z = system.x0, system.y0, system.z0
    v = -wing.h7 * x

    if not (-1e-8 < wing.thetaRootZ < 1e-8):
        r1 = R.from_rotvec(deg2rad(wing.thetaRootZ) * z)
        v = r1.apply(v)
        x = r1.apply(x)
        y = r1.apply(y)
    
    if not (-1e-8 < wing.theta2_e if isLeft else wing.theta2_d < 1e-8):
        r2 = R.from_rotvec(-deg2rad(wing.theta2_e if isLeft else wing.theta2_d) * x)
        v = r2.apply(v)
        y = r2.apply(y)
    
    if not (-1e-8 < wing.thetaRootY < 1e-8):
        r3 = R.from_rotvec(-deg2rad(wing.thetaRootY) * y)
        v = r3.apply(v)
    
    p = p0 + v
    
    return p

def aux1(wing: WingModel, system: WingSystem, l1: ndarray, p1: ndarray, p3: ndarray) -> ndarray:
    p = l1 + wing.delta1 * (norm(cross(l1 - p1, l1 - p3)) / norm(p3 - p1)) * vector.unary(system.x1 + system.x2Base)
    return p

def aux2(wing: WingModel, system: WingSystem, p5: ndarray, p7: ndarray) -> ndarray:
    p = p5 + wing.delta3 * dot(system.y3, p7 - p5) * system.y3
    return p

def aux3(wing: WingModel, system: WingSystem, p7: ndarray, p10: ndarray) -> ndarray:
    p = 0.5 * (p10 + p7) + 0.5 * wing.delta4 * (p7 - p10) + 0.5 * wing.delta5 * cross(system.z3, p7 - p10)
    return p

def aux4(wing: WingModel, system: WingSystem, p11: ndarray, p13: ndarray) -> ndarray:
    p = 0.5 * (p11 + p13) + 0.5 * wing.delta6 * (p11 - p13) + wing.delta7 * norm(p11 - p13) * vector.unary(cross(system.z2Tip + system.z2Base, p11 - p13))
    return p

def c1(p1: ndarray, aux1: ndarray, p3Line: ndarray) -> ndarray:
    p = bezier.fit_quadratic_curve([p1, aux1, p3Line], 0, 0.5, True)
    return p

def c2(wing: WingModel, p1: ndarray, p2: ndarray, p3: ndarray) -> ndarray:
    v = vector.unary(p3 - p1)
    p = p2 + wing.delta1 * dot(p3 - p1, v) * v
    return p

def c3(wing: WingModel, system: WingSystem, p2: ndarray, p3: ndarray, p4: ndarray) -> ndarray:
    v = -system.y2Tip
    p = p3 + wing.delta1 * dot(p2 - p3, v) * v
    return p

def c4(wing: WingModel, system: WingSystem, p3: ndarray, p4: ndarray) -> ndarray:
    p = p3 + wing.delta2 * 0.5 * dot(p4 - p3, system.y2Tip) * system.y2Tip
    return p

def c5(wing: WingModel, system: WingSystem, p3: ndarray, p4: ndarray) -> ndarray:
    p = p4 + wing.delta2 * 0.5 * dot(p3 - p4, -system.y3) * (-system.y3)
    return p

def c6_c7(p5: ndarray, aux2: ndarray, p7: ndarray, tmax: float) -> ndarray:
    p = bezier.fit_curbic_curve([p5, aux2, p7], 0, tmax)
    return p

def c8_c9(p5: ndarray, aux2: ndarray, p7: ndarray, tmin: float) -> ndarray:
    p = bezier.fit_curbic_curve([p5, aux2, p7], tmin, 1)
    return p

def c10_c11(p7: ndarray, aux3: ndarray, p10: ndarray, tmax: float) -> ndarray:
    p = bezier.fit_curbic_curve([p7, aux3, p10], 0, tmax)
    return p

def c12_c13(p7: ndarray, aux3: ndarray, p10: ndarray, tmin: float, tmax: float) -> ndarray:
    p = bezier.fit_curbic_curve([p7, aux3, p10], tmin, tmax)
    return p

def c14_c15(p7: ndarray, aux3: ndarray, p10: ndarray, tmin: float) -> ndarray:
    p = bezier.fit_curbic_curve([p7, aux3, p10], tmin, 1)
    return p

def c16(wing: WingModel, p10: ndarray, p11: ndarray, c15: ndarray) -> ndarray:
    v = vector.unary(p10 - c15)
    p = p10 + wing.delta2 * 0.5 * dot(p11 - p10, v) * v
    return p

def c17(wing: WingModel, p10: ndarray, p11: ndarray, c18: ndarray) -> ndarray:
    v = vector.unary(p11 - c18)
    p = p11 + wing.delta2 * 0.5 * dot(p10 - p11, v) * v
    return p

def c18_c19(p11: ndarray, aux4: ndarray, p13: ndarray, tmax: float) -> ndarray:
    p = bezier.fit_curbic_curve([p11, aux4, p13], 0, tmax)
    return p

def c20_c21(p11: ndarray, aux4: ndarray, p13: ndarray, tmin: float) -> ndarray:
    p = bezier.fit_curbic_curve([p11, aux4, p13], tmin, 1)
    return p

def p26(wing: WingModel, body: BodyModel, system: BaseSystem) -> ndarray:
    p = (wing.h1 * cos(wing.thetaRootZ * deg2RadConst) + body.h8) * system.x0 + body.h9 * system.y0
    return p

def p27(wing: WingModel, body: BodyModel, system: BaseSystem) -> ndarray:
    p = - (wing.h7 * cos(wing.thetaRootZ * deg2RadConst) + body.h10) * system.x0 + body.h11 * system.y0
    return p

def p28(wing: WingModel, body: BodyModel, system: BaseSystem) -> ndarray:
    p = (wing.h1 * cos(wing.thetaRootZ * deg2RadConst) + body.h8) * system.x0 + body.h9 * system.z0
    return p

def p29(wing: WingModel, body: BodyModel, system: BaseSystem) -> ndarray:
    p = wing.h1 * cos(wing.thetaRootZ * deg2RadConst) * system.x0 + body.h12 * system.z0
    return p

def p30(p29: ndarray, aux5: ndarray, aux6: ndarray, p31: ndarray, p14) -> List:

    t30 = bezier.find_plane_intersection([p29, aux5, aux6, p31], p14)
    p = bezier.cubic([p29, aux5, aux6, p31], t30)

    return p, t30

def p31(wing: WingModel, body: BodyModel, system: BaseSystem) -> ndarray:
    p = - wing.h7 * cos(wing.thetaRootZ * deg2RadConst) * system.x0 + body.h13 * system.z0
    return p

def p32(wing: WingModel, body: BodyModel, system: BaseSystem) -> ndarray:
    p = - (wing.h7 * cos(wing.thetaRootZ * deg2RadConst) + body.h10) * system.x0 + body.h14 * system.z0
    return p

def p33(wing: WingModel, body: BodyModel, system: BaseSystem) -> ndarray:
    p = (wing.h1 * cos(wing.thetaRootZ * deg2RadConst) + body.h8) * system.x0 - body.h9 * system.z0
    return p

def p34(wing: WingModel, body: BodyModel, system: BaseSystem) -> ndarray:
    p = wing.h1 * cos(wing.thetaRootZ * deg2RadConst) * system.x0 - body.h16 * system.z0
    return p

def p35(p34: ndarray, aux7: ndarray, aux8: ndarray, p36: ndarray, p14) -> List:

    t35 = bezier.find_plane_intersection([p34, aux7, aux8, p36], p14)
    p = bezier.cubic([p34, aux7, aux8, p36], t35)
    
    return p, t35

def p36(wing: WingModel, body: BodyModel, system: BaseSystem) -> ndarray:
    p = - wing.h7 * cos(wing.thetaRootZ * deg2RadConst) * system.x0 - body.h15 * system.z0
    return p

def p37(wing: WingModel, body: BodyModel, system: BaseSystem) -> ndarray:
    p = - (wing.h7 * cos(wing.thetaRootZ * deg2RadConst) + body.h10) * system.x0 - body.h14 * system.z0
    return p

def _body_control_point(v1: ndarray, v2: ndarray, d1: float, d2: float, ax1: ndarray, ax2: ndarray, isFirst: bool) -> ndarray:
    mult = 1 if isFirst else 2
    return v1 + mult * (v2 - v1) / 3 + vector.norm(v2 - v1) * (d1 * ax1 + d2 * ax2)

def c22(body: BodyModel, system: BaseSystem, p26: ndarray, p1: ndarray) -> ndarray:
    p = _body_control_point(p26, p1, body.delta11, body.delta12, system.x0, system.y0, True)
    return p

def c23(body: BodyModel, system: BaseSystem, p26: ndarray, p1: ndarray) -> ndarray:
    p = _body_control_point(p26, p1, body.delta13, body.delta14, system.x0, system.y0, False)
    return p

def c24(body: BodyModel, system: BaseSystem, p13: ndarray, p27: ndarray) -> ndarray:
    p = _body_control_point(p13, p27, -body.delta15, body.delta16, system.x0, system.y0, True)
    return p

def c25(body: BodyModel, system: BaseSystem, p13: ndarray, p27: ndarray) -> ndarray:
    p = _body_control_point(p13, p27, -body.delta15, body.delta16, system.x0, system.y0, False)
    return p

def c26(body: BodyModel, system: BaseSystem, p28: ndarray, p29: ndarray) -> ndarray:
    p = _body_control_point(p28, p29, body.delta17, body.delta18, system.x0, system.z0, True)
    return p

def c27(body: BodyModel, system: BaseSystem, p28: ndarray, p29: ndarray) -> ndarray:
    p = _body_control_point(p28, p29, body.delta19, body.delta20, system.x0, system.z0, False)
    return p

def aux5(body: BodyModel, system: BaseSystem, p29: ndarray, p31: ndarray) -> ndarray:
    p = _body_control_point(p29, p31, body.delta21, body.delta22, system.x0, system.z0, True)
    return p

def aux6(body: BodyModel, system: BaseSystem, p29: ndarray, p31: ndarray) -> ndarray:
    p = _body_control_point(p29, p31, -body.delta23, body.delta24, system.x0, system.z0, False)
    return p

def c28_29(p29: ndarray, aux5: ndarray, aux6: ndarray, p31: ndarray, tmax: float) -> ndarray:
    p = bezier.fit_curbic_curve([p29, aux5, aux6, p31], 0, tmax)
    return p

def c30_31(p29: ndarray, aux5: ndarray, aux6: ndarray, p31: ndarray, tmin: float) -> ndarray:
    p = bezier.fit_curbic_curve([p29, aux5, aux6, p31], tmin, 1)
    return p

def c32(body: BodyModel, system: BaseSystem, p31: ndarray, p32: ndarray) -> ndarray:
    p = _body_control_point(p31, p32, -body.delta25, body.delta26, system.x0, system.z0, True)
    return p

def c33(body: BodyModel, system: BaseSystem, p31: ndarray, p32: ndarray) -> ndarray:
    p = _body_control_point(p31, p32, -body.delta27, body.delta28, system.x0, system.z0, False)
    return p

def c34(body: BodyModel, system: BaseSystem, p33: ndarray, p34: ndarray) -> ndarray:
    p = _body_control_point(p33, p34, body.delta29, -body.delta30, system.x0, system.z0, True)
    return p

def c35(body: BodyModel, system: BaseSystem, p33: ndarray, p34: ndarray) -> ndarray:
    p = _body_control_point(p33, p34, body.delta31, -body.delta32, system.x0, system.z0, False)
    return p

def aux7(body: BodyModel, system: BaseSystem, p34: ndarray, p36: ndarray) -> ndarray:
    p = _body_control_point(p34, p36, body.delta33, -body.delta34, system.x0, system.z0, True)
    return p

def aux8(body: BodyModel, system: BaseSystem, p34: ndarray, p36: ndarray) -> ndarray:
    p = _body_control_point(p34, p36, -body.delta35, -body.delta36, system.x0, system.z0, False)
    return p

def c36_37(p34: ndarray, aux7: ndarray, aux8: ndarray, p36: ndarray, tmax: float) -> ndarray:
    p = bezier.fit_curbic_curve([p34, aux7, aux8, p36], 0, tmax)
    return p

def c38_39(p34: ndarray, aux7: ndarray, aux8: ndarray, p36: ndarray, tmin: float) -> ndarray:
    p = bezier.fit_curbic_curve([p34, aux7, aux8, p36], tmin, 1)
    return p

def c40(body: BodyModel, system: BaseSystem, p36: ndarray, p37: ndarray) -> ndarray:
    p = _body_control_point(p36, p37, -body.delta37, -body.delta38, system.x0, system.z0, True)
    return p

def c41(body: BodyModel, system: BaseSystem, p36: ndarray, p37: ndarray) -> ndarray:
    p = _body_control_point(p36, p37, -body.delta39, -body.delta40, system.x0, system.z0, False)
    return p

def c42(body: BodyModel, system: BaseSystem, p1: ndarray, p29: ndarray) -> ndarray:
    v = p29 - p1
    ySize = fabs(dot(v, system.y0))
    zSize = fabs(dot(v, system.z0))
    p = p29 + (ySize * body.delta41 * system.y0 - zSize * body.delta42 * system.z0)
    return p

def c43(body: BodyModel, system: BaseSystem, p1: ndarray, p29: ndarray) -> ndarray:
    v = p29 - p1
    ySize = fabs(dot(v, system.y0))
    zSize = fabs(dot(v, system.z0))
    p = p1 + (-ySize * body.delta43 * system.y0 + zSize * body.delta44 * system.z0)
    return p

def c44(body: BodyModel, system: BaseSystem, p1: ndarray, p34: ndarray) -> ndarray:
    v = p34 - p1
    ySize = fabs(dot(v, system.y0))
    zSize = fabs(dot(v, system.z0))
    p = p1 + (-ySize * body.delta45 * system.y0 - zSize * body.delta46 * system.z0)
    return p

def c45(body: BodyModel, system: BaseSystem, p1: ndarray, p34: ndarray) -> ndarray:
    v = p34 - p1
    ySize = fabs(dot(v, system.y0))
    zSize = fabs(dot(v, system.z0))
    p = p34 + (ySize * body.delta47 * system.y0 + zSize * body.delta48 * system.z0)
    return p

def c46_47_48_49(body: BodyModel, system: BaseSystem, p30: ndarray, p14: ndarray, p15: ndarray, p35: ndarray, t30: float) -> List[ndarray]:
    
    v = p30 - p14
    ySize1 = fabs(dot(v, system.y0))
    zSize1 = fabs(dot(v, system.z0))

    v = p35 - p15
    ySize2 = fabs(dot(v, system.y0))
    zSize2 = fabs(dot(v, system.z0))

    # 46
    c46 = p30 + (ySize1 * body.delta57 * system.y0 - zSize1 * body.delta58 * system.z0)

    # 47
    c47 = p14 + (-ySize1 * body.delta59 * system.y0 + zSize1 * body.delta60 * system.z0)

    # 48
    c48 = p15 + (-ySize2 * body.delta61 * system.y0 - zSize2 * body.delta62 * system.z0)

    # 49
    c49 = p35 + (ySize2 * body.delta63 * system.y0 + zSize2 * body.delta64 * system.z0)

    return [c46, c47, c48, c49]

def c50(body: BodyModel, system: BaseSystem, p13: ndarray, p31: ndarray) -> ndarray:
    v = p31 - p13
    ySize = fabs(dot(v, system.y0))
    zSize = fabs(dot(v, system.z0))
    p = p31 + (ySize * body.delta49 * system.y0 - zSize * body.delta50 * system.z0)
    return p

def c51(body: BodyModel, system: BaseSystem, p13: ndarray, p31: ndarray) -> ndarray:
    v = p31 - p13
    ySize = fabs(dot(v, system.y0))
    zSize = fabs(dot(v, system.z0))
    p = p13 + (-ySize * body.delta51 * system.y0 + zSize * body.delta52 * system.z0)
    return p

def c52(body: BodyModel, system: BaseSystem, p13: ndarray, p36: ndarray) -> ndarray:
    v = p36 - p13
    ySize = fabs(dot(v, system.y0))
    zSize = fabs(dot(v, system.z0))
    p = p13 + (-ySize * body.delta53 * system.y0 - zSize * body.delta54 * system.z0)
    return p

def c53(body: BodyModel, system: BaseSystem, p13: ndarray, p36: ndarray) -> ndarray:
    v = p36 - p13
    ySize = fabs(dot(v, system.y0))
    zSize = fabs(dot(v, system.z0))
    p = p36 + (ySize * body.delta55 * system.y0 + zSize * body.delta56 * system.z0)
    return p

def p38(head: HeadModel, system: BaseSystem, center: ndarray) -> ndarray:
    p = center + head.h17 * system.x0 + head.h18 * system.z0
    return p

def p39(head: HeadModel, system: BaseSystem, center: ndarray) -> ndarray:
    p = center + head.h17 * system.x0 - head.h18 * system.z0
    return p

def p41e(head: HeadModel, system: BaseSystem, center: ndarray) -> ndarray:
    p = center + head.h17 * system.x0 + head.h18 * system.y0
    return p

def p41d(head: HeadModel, system: BaseSystem, center: ndarray) -> ndarray:
    p = center + head.h17 * system.x0 - head.h18 * system.y0
    return p

def p42(head: HeadModel, system: BaseSystem, center: ndarray) -> ndarray:
    p = center + (head.h17 + head.h19) * system.x0
    return p

def c54(head: HeadModel, system: BaseSystem, p28: ndarray) -> ndarray:
    p = p28 + system.x0 * head.h17 * head.delta65
    return p

def c56e(head: HeadModel, system: BaseSystem, p26e: ndarray) -> ndarray:
    p = p26e + system.x0 * head.h17 * head.delta65
    return p

def c56d(head: HeadModel, system: BaseSystem, p26d: ndarray) -> ndarray:
    p = p26d + system.x0 * head.h17 * head.delta65
    return p

def c55(head: HeadModel, system: BaseSystem, p33: ndarray) -> ndarray:
    p = p33 + system.x0 * head.h17 * head.delta65
    return p

def c57(head: HeadModel, system: BaseSystem, p38: ndarray) -> ndarray:
    p = p38 + system.x0 * head.h19 * head.delta66
    return p

def c59e(head: HeadModel, system: BaseSystem, p41e: ndarray) -> ndarray:
    p = p41e + system.x0 * head.h19 * head.delta66
    return p

def c59d(head: HeadModel, system: BaseSystem, p41d: ndarray) -> ndarray:
    p = p41d + system.x0 * head.h19 * head.delta66
    return p

def c58(head: HeadModel, system: BaseSystem, p39: ndarray) -> ndarray:
    p = p39 + system.x0 * head.h19 * head.delta66
    return p

def p51(tail: TailModel, system: TailSystem, center: ndarray) -> ndarray:
    if tail.shape == TailShape.rounded or tail.shape == TailShape.pointed:
        p = center + (tail.h20 + tail.h21) * system.x4
    elif tail.shape == TailShape.v:
        p = center + (tail.h20 - tail.h21) * system.x4
    else:
        p = center + tail.h20 * system.x4
    return p

def p47e(tail: TailModel, system: TailSystem, center: ndarray) -> ndarray:
    p = center + tail.h20 * system.x4 - tail.h22 * system.y4
    return p

def p47d(tail: TailModel, system: TailSystem, center: ndarray) -> ndarray:
    p = center + tail.h20 * system.x4 + tail.h22 * system.y4
    return p

def p49e(body: BodyModel, tail: TailModel, system: TailSystem, center: ndarray) -> ndarray:

    v1 = p51(tail, system, center)
    v2e = p47e(tail, system, center)
    v2d = p47d(tail, system, center)

    if tail.shape == TailShape.rounded:

        circleCenter = circle.find_center(v1, v2e, v2d)
        radius = vector.norm(v1 - circleCenter)
        angle = body.h11 / radius
        normal = vector.unary(cross(v1 - circleCenter, v2e - circleCenter))
        rot = R.from_rotvec(angle * normal)
        p = circleCenter + rot.apply(v1 - circleCenter)

    else:
        
        u = vector.unary(v2e - v1)
        p = v1 + u * body.h11

    return p

def p49d(body: BodyModel, tail: TailModel, system: TailSystem, center: ndarray) -> ndarray:

    v1 = p51(tail, system, center)
    v2e = p47e(tail, system, center)
    v2d = p47d(tail, system, center)

    if tail.shape == TailShape.rounded:

        circleCenter = circle.find_center(v1, v2e, v2d)
        radius = vector.norm(v1 - circleCenter)
        angle = body.h11 / radius
        normal = vector.unary(cross(v1 - circleCenter, v2d - circleCenter))
        rot = R.from_rotvec(angle * normal)
        p = circleCenter + rot.apply(v1 - circleCenter)

    else:

        u = vector.unary(v2d - v1)
        p = v1 + u * body.h11

    return p

def p45(p32: ndarray, p51: ndarray) -> ndarray:
    p = 0.5 * (p32 + p51)
    return p

def p46(p37: ndarray, p51: ndarray) -> ndarray:
    p =  0.5 * (p37 + p51)
    return p

def curve82e(body: BodyModel, tail: TailModel, system: TailSystem, center: ndarray, n: int) -> ndarray:
    
    v1 = p47e(tail, system, center)
    v2 = p49e(body, tail, system, center)

    t = linspace(0, 1, num=n + 2)
    curve = zeros((n, 3))

    if tail.shape == TailShape.rounded:

        v3 = p49d(body, tail, system, center)

        circleCenter = circle.find_center(v1, v2, v3)
        curve = circle.circle_arc(circleCenter, v1, v2, n + 2, removeEdges=True)

        return curve

    else:

        const1 = t[1:n + 1]
        const2 = 1 - const1

        curve[:, 0] = const1 * v2[0] + const2 * v1[0]
        curve[:, 1] = const1 * v2[1] + const2 * v1[1]
        curve[:, 2] = const1 * v2[2] + const2 * v1[2]

        return curve

def curve82d(body: BodyModel, tail: TailModel, system: TailSystem, center: ndarray, n: int) -> ndarray:

    v1 = p47d(tail, system, center)
    v2 = p49d(body, tail, system, center)

    t = linspace(0, 1, num=n + 2)
    curve = zeros((n, 3))

    if tail.shape == TailShape.rounded:

        v3 = p49e(body, tail, system, center)

        circleCenter = circle.find_center(v1, v2, v3)
        curve = circle.circle_arc(circleCenter, v1, v2, n + 2, removeEdges=True)

        return curve

    else:

        const1 = t[1:n + 1]
        const2 = 1 - const1

        curve[:, 0] = const1 * v2[0] + const2 * v1[0]
        curve[:, 1] = const1 * v2[1] + const2 * v1[1]
        curve[:, 2] = const1 * v2[2] + const2 * v1[2]

        return curve

def curve83e(body: BodyModel, tail: TailModel, system: TailSystem, center: ndarray, n: int) -> ndarray:
    
    v1 = p49e(body, tail, system, center)
    v2 = p51(tail, system, center)

    t = linspace(0, 1, num=n + 2)
    curve = zeros((n, 3))

    if tail.shape == TailShape.rounded:

        v3 = p49d(body, tail, system, center)

        circleCenter = circle.find_center(v1, v2, v3)
        curve = circle.circle_arc(circleCenter, v1, v2, n + 2, removeEdges=True)

        return curve

    else:

        const1 = t[1:n + 1]
        const2 = 1 - const1

        curve[:, 0] = const1 * v2[0] + const2 * v1[0]
        curve[:, 1] = const1 * v2[1] + const2 * v1[1]
        curve[:, 2] = const1 * v2[2] + const2 * v1[2]

        return curve

def curve83d(body: BodyModel, tail: TailModel, system: TailSystem, center: ndarray, n: int) -> ndarray:

    v1 = p49d(body, tail, system, center)
    v2 = p51(tail, system, center)

    t = linspace(0, 1, num=n + 2)
    curve = zeros((n, 3))

    if tail.shape == TailShape.rounded:

        v3 = p49e(body, tail, system, center)

        circleCenter = circle.find_center(v1, v2, v3)
        curve = circle.circle_arc(circleCenter, v1, v2, n + 2, removeEdges=True)

        return curve

    else:

        const1 = t[1:n + 1]
        const2 = 1 - const1

        curve[:, 0] = const1 * v2[0] + const2 * v1[0]
        curve[:, 1] = const1 * v2[1] + const2 * v1[1]
        curve[:, 2] = const1 * v2[2] + const2 * v1[2]

        return curve
