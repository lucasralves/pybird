import matplotlib.pyplot as plt
import numpy as np
from typing import NamedTuple
from math import pi, sqrt, fabs, atan2

ZERO_ERROR: float = 1e-8
FACTOR: float = 0.25 / pi

class Vec3D(NamedTuple):
    x: float
    y: float
    z: float

def norm_func(a: Vec3D) -> float:
    return (a.x * a.x + a.y * a.y + a.z * a.z) ** 0.5

def quad_doublet_potential(p: Vec3D,
                           p1: Vec3D, p2: Vec3D, p3: Vec3D, p4: Vec3D,
                           area: float,
                           max_distance: float) -> Vec3D:
    
    distance: float = norm_func(p)

    if (distance > max_distance):

        return 0.0

    else:

        d12 = sqrt((p2.x - p1.x) * (p2.x - p1.x) + (p2.y - p1.y) * (p2.y - p1.y))
        d23 = sqrt((p3.x - p2.x) * (p3.x - p2.x) + (p3.y - p2.y) * (p3.y - p2.y))
        d34 = sqrt((p4.x - p3.x) * (p4.x - p3.x) + (p4.y - p3.y) * (p4.y - p3.y))
        d41 = sqrt((p1.x - p4.x) * (p1.x - p4.x) + (p1.y - p4.y) * (p1.y - p4.y))

        S12 = (p2.y - p1.y) / d12
        S23 = (p3.y - p2.y) / d23
        S34 = (p4.y - p3.y) / d34
        S41 = (p1.y - p4.y) / d41

        C12 = (p2.x - p1.x) / d12
        C23 = (p3.x - p2.x) / d23
        C34 = (p4.x - p3.x) / d34
        C41 = (p1.x - p4.x) / d41
        
        R12 = (p.x - p1.x) * S12 - (p.y - p1.y) * C12
        R23 = (p.x - p2.x) * S23 - (p.y - p2.y) * C23
        R34 = (p.x - p3.x) * S34 - (p.y - p3.y) * C34
        R41 = (p.x - p4.x) * S41 - (p.y - p4.y) * C41

        s12_1 = (p1.x - p.x) * C12 + (p1.y - p.y) * S12
        s12_2 = (p2.x - p.x) * C12 + (p2.y - p.y) * S12

        s23_2 = (p2.x - p.x) * C23 + (p2.y - p.y) * S23
        s23_3 = (p3.x - p.x) * C23 + (p3.y - p.y) * S23

        s34_3 = (p3.x - p.x) * C34 + (p3.y - p.y) * S34
        s34_4 = (p4.x - p.x) * C34 + (p4.y - p.y) * S34

        s41_4 = (p4.x - p.x) * C41 + (p4.y - p.y) * S41
        s41_1 = (p1.x - p.x) * C41 + (p1.y - p.y) * S41

        r1 = sqrt( (p.x - p1.x) * (p.x - p1.x) + (p.y - p1.y) * (p.y - p1.y) + p.z * p.z )
        r2 = sqrt( (p.x - p2.x) * (p.x - p2.x) + (p.y - p2.y) * (p.y - p2.y) + p.z * p.z )
        r3 = sqrt( (p.x - p3.x) * (p.x - p3.x) + (p.y - p3.y) * (p.y - p3.y) + p.z * p.z )
        r4 = sqrt( (p.x - p4.x) * (p.x - p4.x) + (p.y - p4.y) * (p.y - p4.y) + p.z * p.z )

        sign_z = 1 if p.z >= 0 else -1
        abs_z = fabs(p.z)

        a12 = R12 * abs_z * (r1 * s12_2 - r2 * s12_1)
        b12 = (r1 * r2 * R12 * R12 + p.z * p.z * s12_1 * s12_2)

        a23 = R23 * abs_z * (r2 * s23_3 - r3 * s23_2)
        b23 = (r2 * r3 * R23 * R23 + p.z * p.z * s23_2 * s23_3)

        a34 = R34 * abs_z * (r3 * s34_4 - r4 * s34_3)
        b34 = (r3 * r4 * R34 * R34 + p.z * p.z * s34_3 * s34_4)

        a41 = R41 * abs_z * (r4 * s41_1 - r1 * s41_4)
        b41 = (r4 * r1 * R41 * R41 + p.z * p.z * s41_4 * s41_1)

        J12 = atan2(a12, b12)
        J23 = atan2(a23, b23)
        J34 = atan2(a34, b34)
        J41 = atan2(a41, b41)

        delta = 0.0
        if R12 < 0 and R23 < 0 and R34 < 0 and R41 < 0:
            delta = 2 * pi
        
        return sign_z * (delta + J12 + J23 + J34 + J41) * FACTOR

def quad_doublet_velocity(p: Vec3D,
                       p1: Vec3D, p2: Vec3D, p3: Vec3D, p4: Vec3D,
                       area: float,
                       max_distance: float) -> Vec3D:
    
    vel: Vec3D = None

    u: float = None
    v: float = None
    w: float = None

    distance: float = norm_func(p)

    if (distance > max_distance):

        den = (p.x * p.x + p.y * p.y + p.z * p.z) ** 2.5

        u = 0.75 * FACTOR * area * p.z * p.x / den
        v = 0.75 * FACTOR * area * p.z * p.y / den
        w = - FACTOR * area * (p.x * p.x + p.y * p.y - 2 * p.z * p.z) / den

        vel = Vec3D(u, v, w)

    else:

        eps = 1e-12
        
        p_eps_x = Vec3D(p.x + eps, p.y, p.z)
        p_eps_y = Vec3D(p.x, p.y + eps, p.z)
        p_eps_z = Vec3D(p.x, p.y, p.z + eps)

        pot = quad_doublet_potential(p, p1, p2, p3, p4, area, max_distance)
        pot_eps_x = quad_doublet_potential(p_eps_x, p1, p2, p3, p4, area, max_distance)
        pot_eps_y = quad_doublet_potential(p_eps_y, p1, p2, p3, p4, area, max_distance)
        pot_eps_z = quad_doublet_potential(p_eps_z, p1, p2, p3, p4, area, max_distance)
        
        vel = Vec3D((pot_eps_x - pot) / eps, (pot_eps_y - pot) / eps, (pot_eps_z - pot) / eps)
    
    return vel

def line_vortex(p1: Vec3D, p2: Vec3D, p: Vec3D) -> Vec3D:

    r1 = Vec3D(p.x - p1.x, p.y - p1.y, p.z - p1.z)
    r2 = Vec3D(p.x - p2.x, p.y - p2.y, p.z - p2.z)
    r0 = Vec3D(p2.x - p1.x, p2.y - p1.y, p2.z - p1.z)

    r1xr2 = Vec3D(r1.y * r2.z - r1.z * r2.y, r1.z * r2.x - r1.x * r2.z, r1.x * r2.y - r1.y * r2.x)

    r1xr2_square = r1xr2.x * r1xr2.x + r1xr2.y * r1xr2.y + r1xr2.z * r1xr2.z;

    r1_norm = sqrt(r1.x * r1.x + r1.y * r1.y + r1.z * r1.z);
    r2_norm = sqrt(r2.x * r2.x + r2.y * r2.y + r2.z * r2.z);

    if ((r1_norm < ZERO_ERROR) or (r2_norm < ZERO_ERROR) or (r1xr2_square < ZERO_ERROR)):
        
        vel = Vec3D(0.0, 0.0, 0.0)

    else:
        r0r1 = r0.x * r1.x + r0.y * r1.y + r0.z * r1.z
        r0r2 = r0.x * r2.x + r0.y * r2.y + r0.z * r2.z
        
        k = (1 / (4 * pi * r1xr2_square)) * (r0r1 / r1_norm - r0r2 / r2_norm)

        vel = Vec3D(k * r1xr2.x, k * r1xr2.y, k * r1xr2.z)
    
    return vel

def quad_doublet_velocity_line(p: Vec3D,
                               p1: Vec3D, p2: Vec3D, p3: Vec3D, p4: Vec3D,
                               area: float,
                               max_distance: float) -> Vec3D:
    
    vel: Vec3D = None

    u: float = None
    v: float = None
    w: float = None

    distance: float = norm_func(p)

    if (distance > max_distance):

        den = (p.x * p.x + p.y * p.y + p.z * p.z) ** 2.5

        u = 0.75 * FACTOR * area * p.z * p.x / den
        v = 0.75 * FACTOR * area * p.z * p.y / den
        w = - FACTOR * area * (p.x * p.x + p.y * p.y - 2 * p.z * p.z) / den

        vel = Vec3D(u, v, w)

    else:

        v1 = line_vortex(p1, p2, p)
        v2 = line_vortex(p2, p3, p)
        v3 = line_vortex(p3, p4, p)
        v4 = line_vortex(p4, p1, p)
        
        vel = Vec3D(v1.x + v2.x + v3.x + v4.x, v1.y + v2.y + v3.y + v4.y, v1.z + v2.z + v3.z + v4.z)
    
    return vel

# def quad_doublet_panel(p: Vec3D,
#                        p1: Vec3D, p2: Vec3D, p3: Vec3D, p4: Vec3D,
#                        area: float,
#                        max_distance: float) -> Vec3D:
    
#     vel: Vec3D = None

#     u: float = None
#     v: float = None
#     w: float = None

#     distance: float = norm_func(p)

#     if (distance > max_distance):

#         den = (p.x * p.x + p.y * p.y + p.z * p.z) ** 2.5

#         u = 0.75 * FACTOR * area * p.z * p.x / den
#         v = 0.75 * FACTOR * area * p.z * p.y / den
#         w = - FACTOR * area * (p.x * p.x + p.y * p.y - 2 * p.z * p.z) / den

#     else:

#         d12 = sqrt((p2.x - p1.x) * (p2.x - p1.x) + (p2.y - p1.y) * (p2.y - p1.y))
#         d23 = sqrt((p3.x - p2.x) * (p3.x - p2.x) + (p3.y - p2.y) * (p3.y - p2.y))
#         d34 = sqrt((p4.x - p3.x) * (p4.x - p3.x) + (p4.y - p3.y) * (p4.y - p3.y))
#         d41 = sqrt((p1.x - p4.x) * (p1.x - p4.x) + (p1.y - p4.y) * (p1.y - p4.y))

#         S12 = (p2.y - p1.y) / d12
#         S23 = (p3.y - p2.y) / d23
#         S34 = (p4.y - p3.y) / d34
#         S41 = (p1.y - p4.y) / d41

#         C12 = (p2.x - p1.x) / d12
#         C23 = (p3.x - p2.x) / d23
#         C34 = (p4.x - p3.x) / d34
#         C41 = (p1.x - p4.x) / d41
        
#         R12 = (p.x - p1.x) * S12 - (p.y - p1.y) * C12
#         R23 = (p.x - p2.x) * S23 - (p.y - p2.y) * C23
#         R34 = (p.x - p3.x) * S34 - (p.y - p3.y) * C34
#         R41 = (p.x - p4.x) * S41 - (p.y - p4.y) * C41

#         s12_1 = (p1.x - p.x) * C12 + (p1.y - p.y) * S12
#         s12_2 = (p2.x - p.x) * C12 + (p2.y - p.y) * S12

#         s23_2 = (p2.x - p.x) * C23 + (p2.y - p.y) * S23
#         s23_3 = (p3.x - p.x) * C23 + (p3.y - p.y) * S23

#         s34_3 = (p3.x - p.x) * C34 + (p3.y - p.y) * S34
#         s34_4 = (p4.x - p.x) * C34 + (p4.y - p.y) * S34

#         s41_4 = (p4.x - p.x) * C41 + (p4.y - p.y) * S41
#         s41_1 = (p1.x - p.x) * C41 + (p1.y - p.y) * S41

#         r1 = sqrt( (p.x - p1.x) * (p.x - p1.x) + (p.y - p1.y) * (p.y - p1.y) + p.z * p.z )
#         r2 = sqrt( (p.x - p2.x) * (p.x - p2.x) + (p.y - p2.y) * (p.y - p2.y) + p.z * p.z )
#         r3 = sqrt( (p.x - p3.x) * (p.x - p3.x) + (p.y - p3.y) * (p.y - p3.y) + p.z * p.z )
#         r4 = sqrt( (p.x - p4.x) * (p.x - p4.x) + (p.y - p4.y) * (p.y - p4.y) + p.z * p.z )

#         dR12dx = S12; dR12dy = - C12
#         dR23dx = S23; dR23dy = - C23
#         dR34dx = S34; dR34dy = - C34
#         dR41dx = S41; dR41dy = - C41

#         ds12_1dx = - C12; ds12_1dy = - S12
#         ds12_2dx = - C12; ds12_2dy = - S12

#         ds23_2dx = - C23; ds23_2dy = - S23
#         ds23_3dx = - C23; ds23_3dy = - S23

#         ds34_3dx = - C34; ds34_3dy = - S34
#         ds34_4dx = - C34; ds34_4dy = - S34

#         ds41_4dx = - C41; ds41_4dy = - S41
#         ds41_1dx = - C41; ds41_1dy = - S41

#         dr1dx = (p.x - p1.x) / r1; dr1dy = (p.y - p1.y) / r1; dr1dz = p.z / r1
#         dr2dx = (p.x - p2.x) / r2; dr2dy = (p.y - p2.y) / r2; dr2dz = p.z / r2
#         dr3dx = (p.x - p3.x) / r3; dr3dy = (p.y - p3.y) / r3; dr3dz = p.z / r3
#         dr4dx = (p.x - p4.x) / r4; dr4dy = (p.y - p4.y) / r4; dr4dz = p.z / r4

#         sign_z = 1 if p.z >= 0 else -1
#         abs_z = fabs(p.z)

#         a12 = R12 * abs_z * (r1 * s12_2 - r2 * s12_1)
#         b12 = (r1 * r2 * R12 * R12 + p.z * p.z * s12_1 * s12_2)

#         a23 = R23 * abs_z * (r2 * s23_3 - r3 * s23_2)
#         b23 = (r2 * r3 * R23 * R23 + p.z * p.z * s23_2 * s23_3)

#         a34 = R34 * abs_z * (r3 * s34_4 - r4 * s34_3)
#         b34 = (r3 * r4 * R34 * R34 + p.z * p.z * s34_3 * s34_4)

#         a41 = R41 * abs_z * (r4 * s41_1 - r1 * s41_4)
#         b41 = (r4 * r1 * R41 * R41 + p.z * p.z * s41_4 * s41_1)

#         da12dx = abs_z * ( dR12dx * (r1 * s12_2 - r2 * s12_1) + R12 * (dr1dx * s12_2 + r1 * ds12_2dx - dr2dx * s12_1 - r2 * ds12_1dx) )
#         da23dx = abs_z * ( dR23dx * (r2 * s23_3 - r3 * s23_2) + R23 * (dr2dx * s23_3 + r2 * ds23_3dx - dr3dx * s23_2 - r3 * ds23_2dx) )
#         da34dx = abs_z * ( dR34dx * (r3 * s34_4 - r4 * s34_3) + R34 * (dr3dx * s34_4 + r3 * ds34_4dx - dr4dx * s34_3 - r4 * ds34_3dx) )
#         da41dx = abs_z * ( dR41dx * (r4 * s41_1 - r1 * s41_4) + R41 * (dr4dx * s41_1 + r4 * ds41_1dx - dr1dx * s41_4 - r1 * ds41_4dx) )

#         da12dy = abs_z * ( dR12dy * (r1 * s12_2 - r2 * s12_1) + R12 * (dr1dy * s12_2 + r1 * ds12_2dy - dr2dy * s12_1 - r2 * ds12_1dy) )
#         da23dy = abs_z * ( dR23dy * (r2 * s23_3 - r3 * s23_2) + R23 * (dr2dy * s23_3 + r2 * ds23_3dy - dr3dy * s23_2 - r3 * ds23_2dy) )
#         da34dy = abs_z * ( dR34dy * (r3 * s34_4 - r4 * s34_3) + R34 * (dr3dy * s34_4 + r3 * ds34_4dy - dr4dy * s34_3 - r4 * ds34_3dy) )
#         da41dy = abs_z * ( dR41dy * (r4 * s41_1 - r1 * s41_4) + R41 * (dr4dy * s41_1 + r4 * ds41_1dy - dr1dy * s41_4 - r1 * ds41_4dy) )

#         da12dz = sign_z * R12 * (r1 * s12_2 - r2 * s12_1) + abs_z * R12 * (dr1dz * s12_2 - dr2dz * s12_1)
#         da23dz = sign_z * R23 * (r2 * s23_3 - r3 * s23_2) + abs_z * R23 * (dr2dz * s23_3 - dr3dz * s23_2)
#         da34dz = sign_z * R34 * (r3 * s34_4 - r4 * s34_3) + abs_z * R34 * (dr3dz * s34_4 - dr4dz * s34_3)
#         da41dz = sign_z * R41 * (r4 * s41_1 - r1 * s41_4) + abs_z * R41 * (dr4dz * s41_1 - dr1dz * s41_4)

#         db12dx = R12 * (2 * r1 * r2 * dR12dx + dr1dx * r2 * R12 + r1 * dr2dx * R12) + p.z * p.z * (ds12_1dx * s12_2 + s12_1 * ds12_2dx)
#         db23dx = R23 * (2 * r2 * r3 * dR23dx + dr2dx * r3 * R23 + r2 * dr3dx * R23) + p.z * p.z * (ds23_2dx * s23_3 + s23_2 * ds23_3dx)
#         db34dx = R34 * (2 * r3 * r4 * dR34dx + dr3dx * r4 * R34 + r3 * dr4dx * R34) + p.z * p.z * (ds34_3dx * s34_4 + s34_3 * ds34_4dx)
#         db41dx = R41 * (2 * r4 * r1 * dR41dx + dr4dx * r1 * R41 + r4 * dr1dx * R41) + p.z * p.z * (ds41_4dx * s41_1 + s41_4 * ds41_1dx)

#         db12dy = R12 * (2 * r1 * r2 * dR12dy + dr1dy * r2 * R12 + r1 * dr2dy * R12) + p.z * p.z * (ds12_1dy * s12_2 + s12_1 * ds12_2dy)
#         db23dy = R23 * (2 * r2 * r3 * dR23dy + dr2dy * r3 * R23 + r2 * dr3dy * R23) + p.z * p.z * (ds23_2dy * s23_3 + s23_2 * ds23_3dy)
#         db34dy = R34 * (2 * r3 * r4 * dR34dy + dr3dy * r4 * R34 + r3 * dr4dy * R34) + p.z * p.z * (ds34_3dy * s34_4 + s34_3 * ds34_4dy)
#         db41dy = R41 * (2 * r4 * r1 * dR41dy + dr4dy * r1 * R41 + r4 * dr1dy * R41) + p.z * p.z * (ds41_4dy * s41_1 + s41_4 * ds41_1dy)

#         db12dz = R12 * R12 * (dr1dz * r2 + r1 * dr2dz) + sign_z * s12_1 * s12_2
#         db23dz = R23 * R23 * (dr2dz * r3 + r2 * dr3dz) + sign_z * s23_2 * s23_3
#         db34dz = R34 * R34 * (dr3dz * r4 + r3 * dr4dz) + sign_z * s34_3 * s34_4
#         db41dz = R41 * R41 * (dr4dz * r1 + r4 * dr1dz) + sign_z * s41_4 * s41_1

#         dJ12dx = ((da12dx * b12 - a12 * db12dx) / (b12 * b12)) / ((a12 / b12) * (a12 / b12) + 1)
#         dJ23dx = ((da23dx * b23 - a23 * db23dx) / (b23 * b23)) / ((a23 / b23) * (a23 / b23) + 1)
#         dJ34dx = ((da34dx * b34 - a34 * db34dx) / (b34 * b34)) / ((a34 / b34) * (a34 / b34) + 1)
#         dJ41dx = ((da41dx * b41 - a41 * db41dx) / (b41 * b41)) / ((a41 / b41) * (a41 / b41) + 1)

#         dJ12dy = ((da12dy * b12 - a12 * db12dy) / (b12 * b12)) / ((a12 / b12) * (a12 / b12) + 1)
#         dJ23dy = ((da23dy * b23 - a23 * db23dy) / (b23 * b23)) / ((a23 / b23) * (a23 / b23) + 1)
#         dJ34dy = ((da34dy * b34 - a34 * db34dy) / (b34 * b34)) / ((a34 / b34) * (a34 / b34) + 1)
#         dJ41dy = ((da41dy * b41 - a41 * db41dy) / (b41 * b41)) / ((a41 / b41) * (a41 / b41) + 1)

#         dJ12dz = ((da12dz * b12 - a12 * db12dz) / (b12 * b12)) / ((a12 / b12) * (a12 / b12) + 1)
#         dJ23dz = ((da23dz * b23 - a23 * db23dz) / (b23 * b23)) / ((a23 / b23) * (a23 / b23) + 1)
#         dJ34dz = ((da34dz * b34 - a34 * db34dz) / (b34 * b34)) / ((a34 / b34) * (a34 / b34) + 1)
#         dJ41dz = ((da41dz * b41 - a41 * db41dz) / (b41 * b41)) / ((a41 / b41) * (a41 / b41) + 1)

#         u = sign_z * (dJ12dx + dJ23dx + dJ34dx + dJ41dx)
#         v = sign_z * (dJ12dy + dJ23dy + dJ34dy + dJ41dy)
#         w = sign_z * (dJ12dz + dJ23dz + dJ34dz + dJ41dz)
    
#     vel = Vec3D(u, v, w)

#     return vel

def numpy2Vec3D(a: np.ndarray) -> Vec3D:
    return Vec3D(a[0], a[1], a[2])

def test_pot():

    p1 = 1 * np.array([1, 1, 0])
    p2 = 1 * np.array([-1, 1, 0])
    p3 = 1 * np.array([-1, -1, 0])
    p4 = 1 * np.array([1, -1, 0])

    p_avg = 0.25 * (p1 + p2 + p3 + p4)

    p1 = numpy2Vec3D(p1 - p_avg)
    p2 = numpy2Vec3D(p2 - p_avg)
    p3 = numpy2Vec3D(p3 - p_avg)
    p4 = numpy2Vec3D(p4 - p_avg)

    area = 1.0
    max_distance = 1e2

    n = 100
    l = 2
    x1 = np.linspace(-l, l, num=n)
    y1 = np.linspace(-l, l, num=n)
    z1 = 1.0

    x2 = np.linspace(-l, l, num=n)
    y2 = 0.0
    z2 = np.linspace(-l, l, num=n)

    X1, Y1 = np.meshgrid(x1, y1)
    X2, Z2 = np.meshgrid(x2, z2)

    pot1 = np.empty((n, n), dtype=np.double)
    pot2 = np.empty((n, n), dtype=np.double)

    for i in range(n):
        for j in range(n):
            
            p_1 = Vec3D(X1[i, j], Y1[i, j], z1)
            p_2 = Vec3D(X2[i, j], y2, Z2[i, j])

            pot1[i, j] = quad_doublet_potential(p_1, p1, p2, p3, p4, area, max_distance)
            pot2[i, j] = quad_doublet_potential(p_2, p1, p2, p3, p4, area, max_distance)
    

    plt.figure()
    plt.title('xy')
    plt.contourf(X1, Y1, pot1[:, :])
    plt.colorbar()
    plt.plot([p1.x, p2.x, p3.x, p4.x, p1.x], [p1.y, p2.y, p3.y, p4.y, p1.y], 'k')
    plt.grid()
    plt.axis('equal')

    plt.figure()
    plt.title('xz')
    plt.contourf(X2, Z2, pot2[:, :])
    plt.colorbar()
    plt.plot([p1.x, p2.x, p3.x, p4.x, p1.x], [p1.y, p2.y, p3.y, p4.y, p1.y], 'k')
    plt.grid()
    plt.axis('equal')

    plt.show()

    return

def test_vel():

    p1 = 10 * np.array([10, 1, 0])
    p2 = 10 * np.array([-10, 1, 0])
    p3 = 10 * np.array([-10, -1, 0])
    p4 = 10 * np.array([10, -1, 0])

    p_avg = 0.25 * (p1 + p2 + p3 + p4)

    p1 = p1 - p_avg
    p2 = p2 - p_avg
    p3 = p3 - p_avg
    p4 = p4 - p_avg

    min_dist = min([np.linalg.norm(p1 - p2) / 2, np.linalg.norm(p2 - p3) / 2])

    area = 0.5 * (np.linalg.norm(np.cross(p2 - p1, p3 - p1)) + np.linalg.norm(np.cross(p3 - p1, p4 - p1)))
    max_distance = 10 * np.sqrt(4 * area / np.pi)

    p1 = numpy2Vec3D(p1 - p_avg)
    p2 = numpy2Vec3D(p2 - p_avg)
    p3 = numpy2Vec3D(p3 - p_avg)
    p4 = numpy2Vec3D(p4 - p_avg)

    n = 100
    l = 3.1
    x1 = np.linspace(-l, l, num=n)
    y1 = np.linspace(-l, l, num=n)
    z1 = 0.000001

    x2 = np.linspace(-l, l, num=n)
    y2 = 0.0
    z2 = np.linspace(-l, l, num=n)

    x3 = 0.0
    y3 = np.linspace(-l, l, num=n)
    z3 = np.linspace(-l, l, num=n)

    X1, Y1 = np.meshgrid(x1, y1)
    X2, Z2 = np.meshgrid(x2, z2)
    Y3, Z3 = np.meshgrid(x2, z2)

    vel1 = np.empty((n, n, 3), dtype=np.double)
    vel2 = np.empty((n, n, 3), dtype=np.double)
    vel3 = np.empty((n, n, 3), dtype=np.double)

    for i in range(n):
        for j in range(n):
            
            p_1 = Vec3D(X1[i, j], Y1[i, j], z1)
            p_2 = Vec3D(X2[i, j], y2, Z2[i, j])
            p_3 = Vec3D(x3, Y3[i, j], Z3[i, j])

            vel_1 = quad_doublet_velocity(p_1, p1, p2, p3, p4, area, max_distance)
            vel_2 = quad_doublet_velocity(p_2, p1, p2, p3, p4, area, max_distance)
            vel_3 = quad_doublet_velocity(p_3, p1, p2, p3, p4, area, max_distance)

            vel1[i, j, 0] = vel_1.x
            vel1[i, j, 1] = vel_1.y
            vel1[i, j, 2] = vel_1.z

            # vel2[i, j, 0] = vel_2.x
            # vel2[i, j, 1] = vel_2.y
            # vel2[i, j, 2] = vel_2.z

            # vel3[i, j, 0] = vel_3.x
            # vel3[i, j, 1] = vel_3.y
            # vel3[i, j, 2] = vel_3.z
    
    print(min_dist * vel1[int(0.5 * n), int(0.5 * n), :])
    

    plt.figure()
    plt.title('xy')
    plt.contourf(X1, Y1, vel1[:, :, 2])
    plt.colorbar()
    plt.quiver(X1, Y1, vel1[:, :, 0], vel1[:, :, 1])
    plt.plot([p1.x, p2.x, p3.x, p4.x, p1.x], [p1.y, p2.y, p3.y, p4.y, p1.y], 'k')
    plt.grid()
    plt.axis('equal')

    # plt.figure()
    # plt.title('xz')
    # plt.contourf(X2, Z2, vel2[:, :, 1])
    # plt.colorbar()
    # plt.quiver(X2, Z2, vel2[:, :, 0], vel2[:, :, 2])
    # plt.plot([p1.x, p2.x, p3.x, p4.x, p1.x], [p1.z, p2.z, p3.z, p4.z, p1.z], 'k')
    # plt.grid()
    # plt.axis('equal')

    # plt.figure()
    # plt.title('yz')
    # plt.contourf(Y3, Z3, vel3[:, :, 0])
    # plt.colorbar()
    # plt.quiver(Y3, Z3, vel3[:, :, 1], vel3[:, :, 2])
    # plt.plot([p1.y, p2.y, p3.y, p4.y, p1.y], [p1.z, p2.z, p3.z, p4.z, p1.z], 'k')
    # plt.grid()
    # plt.axis('equal')

    plt.show()

    return

def test_vel_points():

    v1 = numpy2Vec3D(np.array([-1.47e-02, -5.82e-03, 0.00e+00]))
    v2 = numpy2Vec3D(np.array([-6.59e-03, -1.38e-02, 0.00e+00]))
    v3 = numpy2Vec3D(np.array([1.51e-02, 7.98e-03, 0.00e+00]))
    v4 = numpy2Vec3D(np.array([6.18e-03, 1.16e-02, 0.00e+00]))

    p1 = numpy2Vec3D(np.array([-1.20e-17, -1.23e-17, 1.00e-08]))
    p2 = numpy2Vec3D(np.array([3.58e-02, 3.29e-02, 7.29e-04]))
    p3 = numpy2Vec3D(np.array([5.44e-02, 2.95e-02, 7.98e-04]))

    vel_1 = quad_doublet_velocity(p1, v1, v2, v3, v4, 1, 10)
    vel_2 = quad_doublet_velocity(p2, v1, v2, v3, v4, 1, 10)
    vel_3 = quad_doublet_velocity(p3, v1, v2, v3, v4, 1, 10)
    
    print(vel_1)
    print(vel_2)
    print(vel_3)

    return

def test_compare(p1: np.ndarray,
                 p2: np.ndarray,
                 p3: np.ndarray,
                 p4: np.ndarray,
                 plane: str,
                 dist: float):

    p_avg = 0.25 * (p1 + p2 + p3 + p4)

    p1 = p1 - p_avg
    p2 = p2 - p_avg
    p3 = p3 - p_avg
    p4 = p4 - p_avg

    area = 0.5 * (np.linalg.norm(np.cross(p2 - p1, p3 - p1)) + np.linalg.norm(np.cross(p3 - p1, p4 - p1)))
    max_distance = 10 * np.sqrt(4 * area / np.pi)

    p1 = numpy2Vec3D(p1 - p_avg)
    p2 = numpy2Vec3D(p2 - p_avg)
    p3 = numpy2Vec3D(p3 - p_avg)
    p4 = numpy2Vec3D(p4 - p_avg)

    n = 100
    l = 3.1
    axis_1 = np.linspace(-l, l, num=n)
    axis_2 = np.linspace(-l, l, num=n)

    axis_1, axis_2 = np.meshgrid(axis_1, axis_2)

    vel_line = np.empty((n, n, 3), dtype=np.double)
    vel_pot = np.empty((n, n, 3), dtype=np.double)

    for i in range(n):
        for j in range(n):
            
            if plane == 'xy': p = Vec3D(axis_1[i, j], axis_2[i, j], dist)
            if plane == 'xz': p = Vec3D(axis_1[i, j], dist, axis_2[i, j])
            if plane == 'yz': p = Vec3D(dist, axis_1[i, j], axis_2[i, j])

            vel_vec = quad_doublet_velocity_line(p, p1, p2, p3, p4, area, max_distance)

            vel_line[i, j, 0] = vel_vec.x
            vel_line[i, j, 1] = vel_vec.y
            vel_line[i, j, 2] = vel_vec.z

            vel_vec = quad_doublet_velocity(p, p1, p2, p3, p4, area, max_distance)

            vel_pot[i, j, 0] = - vel_vec.x
            vel_pot[i, j, 1] = - vel_vec.y
            vel_pot[i, j, 2] = - vel_vec.z
    
    plt.figure()

    if plane == 'xy': plt.title('xy - from line')
    if plane == 'xz': plt.title('xz - from line')
    if plane == 'yz': plt.title('yz - from line')

    if plane == 'xy': plt.contourf(axis_1, axis_2, vel_line[:, :, 2])
    if plane == 'xz': plt.contourf(axis_1, axis_2, vel_line[:, :, 1])
    if plane == 'yz': plt.contourf(axis_1, axis_2, vel_line[:, :, 0])

    plt.colorbar()

    if plane == 'xy': plt.quiver(axis_1, axis_2, vel_line[:, :, 0], vel_line[:, :, 1])
    if plane == 'xz': plt.quiver(axis_1, axis_2, vel_line[:, :, 0], vel_line[:, :, 2])
    if plane == 'yz': plt.quiver(axis_1, axis_2, vel_line[:, :, 1], vel_line[:, :, 2])

    if plane == 'xy': plt.plot([p1.x, p2.x, p3.x, p4.x, p1.x], [p1.y, p2.y, p3.y, p4.y, p1.y], 'k')
    if plane == 'xz': plt.plot([p1.x, p2.x, p3.x, p4.x, p1.x], [p1.z, p2.z, p3.z, p4.z, p1.z], 'k')
    if plane == 'yz': plt.plot([p1.y, p2.y, p3.y, p4.y, p1.y], [p1.z, p2.z, p3.z, p4.z, p1.z], 'k')

    plt.grid()
    plt.axis('equal')

    #------------------------------------------#
    plt.figure()

    if plane == 'xy': plt.title('xy - from pot')
    if plane == 'xz': plt.title('xz - from pot')
    if plane == 'yz': plt.title('yz - from pot')

    if plane == 'xy': plt.contourf(axis_1, axis_2, vel_pot[:, :, 2])
    if plane == 'xz': plt.contourf(axis_1, axis_2, vel_pot[:, :, 1])
    if plane == 'yz': plt.contourf(axis_1, axis_2, vel_pot[:, :, 0])

    plt.colorbar()

    if plane == 'xy': plt.quiver(axis_1, axis_2, vel_pot[:, :, 0], vel_pot[:, :, 1])
    if plane == 'xz': plt.quiver(axis_1, axis_2, vel_pot[:, :, 0], vel_pot[:, :, 2])
    if plane == 'yz': plt.quiver(axis_1, axis_2, vel_pot[:, :, 1], vel_pot[:, :, 2])

    if plane == 'xy': plt.plot([p1.x, p2.x, p3.x, p4.x, p1.x], [p1.y, p2.y, p3.y, p4.y, p1.y], 'k')
    if plane == 'xz': plt.plot([p1.x, p2.x, p3.x, p4.x, p1.x], [p1.z, p2.z, p3.z, p4.z, p1.z], 'k')
    if plane == 'yz': plt.plot([p1.y, p2.y, p3.y, p4.y, p1.y], [p1.z, p2.z, p3.z, p4.z, p1.z], 'k')

    plt.grid()
    plt.axis('equal')

    plt.show()

    return

if __name__ == '__main__':
    
    p1 = np.array([+1.0, +1.0, 0.0])
    p2 = np.array([-1.0, +1.0, 0.0])
    p3 = np.array([-1.0, -1.0, 0.0])
    p4 = np.array([+1.0, -1.0, 0.0])

    test_compare(p1, p2, p3, p4, 'xy', 0.00001)