#include <math.h>

#include "../../models/models.h"
#include "../../math/math.h"

const double ZERO_ERROR = 1e-12;
const double FACTOR = 0.25 / M_PI;

Vec3D tri_source_panel(Vec3D p1, Vec3D p2, Vec3D p3, Vec3D p, Vec3D e1, Vec3D e2, Vec3D e3, double area, double max_distance, int print)
{

    Vec3D vel;
    double u, v, w;

    double distance = norm_vec(p);

    if (distance > max_distance) {

        double pNorm3 = pow(norm_vec(p), 3);

        u = FACTOR * area * p.x / pNorm3;
        v = FACTOR * area * p.y / pNorm3;
        w = FACTOR * area * p.z / pNorm3;

    } else {

        double r1, r2, r3;
        double d12, d23, d31;
        double S12, S23, S31;
        double C12, C23, C31;
        double Q12, Q23, Q31;
        double R12, R23, R31;
        double J12, J23, J31;

        double s12_1, s12_2;
        double s23_2, s23_3;
        double s31_3, s31_1;

        double sign, delta;

        r1 = sqrt((p.x - p1.x) * (p.x - p1.x) + (p.y - p1.y) * (p.y - p1.y) + p.z * p.z);
        r2 = sqrt((p.x - p2.x) * (p.x - p2.x) + (p.y - p2.y) * (p.y - p2.y) + p.z * p.z);
        r3 = sqrt((p.x - p3.x) * (p.x - p3.x) + (p.y - p3.y) * (p.y - p3.y) + p.z * p.z);

        d12 = sqrt((p2.x - p1.x) * (p2.x - p1.x) + (p2.y - p1.y) * (p2.y - p1.y));
        d23 = sqrt((p3.x - p2.x) * (p3.x - p2.x) + (p3.y - p2.y) * (p3.y - p2.y));
        d31 = sqrt((p1.x - p3.x) * (p1.x - p3.x) + (p1.y - p3.y) * (p1.y - p3.y));

        S12 = (p2.y - p1.y) / d12;
        S23 = (p3.y - p2.y) / d23;
        S31 = (p1.y - p3.y) / d31;

        C12 = (p2.x - p1.x) / d12;
        C23 = (p3.x - p2.x) / d23;
        C31 = (p1.x - p3.x) / d31;

        Q12 = log((r1 + r2 + d12) / (r1 + r2 - d12));
        Q23 = log((r2 + r3 + d23) / (r2 + r3 - d23));
        Q31 = log((r3 + r1 + d31) / (r3 + r1 - d31));

        R12 = (p.x - p1.x) * S12 - (p.y - p1.y) * C12;
        R23 = (p.x - p2.x) * S23 - (p.y - p2.y) * C23;
        R31 = (p.x - p3.x) * S31 - (p.y - p3.y) * C31;

        s12_1 = (p1.x - p.x) * C12 + (p1.y - p.y) * S12;
        s12_2 = (p2.x - p.x) * C12 + (p2.y - p.y) * S12;

        s23_2 = (p2.x - p.x) * C23 + (p2.y - p.y) * S23;
        s23_3 = (p3.x - p.x) * C23 + (p3.y - p.y) * S23;

        s31_3 = (p3.x - p.x) * C31 + (p3.y - p.y) * S31;
        s31_1 = (p1.x - p.x) * C31 + (p1.y - p.y) * S31;

        J12 = atan2( (R12 * fabs(p.z) * (r1 * s12_2 - r2 * s12_1)) , (r1 * r2 * R12 * R12 + p.z * p.z * s12_1 * s12_2) );
        J23 = atan2( (R23 * fabs(p.z) * (r2 * s23_3 - r3 * s23_2)) , (r2 * r3 * R23 * R23 + p.z * p.z * s23_2 * s23_3) );
        J31 = atan2( (R31 * fabs(p.z) * (r3 * s31_1 - r1 * s31_3)) , (r3 * r1 * R31 * R31 + p.z * p.z * s31_3 * s31_1) );

        if (p.z < 0) {
            sign = - 1.0;
        } else {
            sign = 1.0;
        }

        if ((R12 < 0) && (R23 < 0) && (R31 < 0)) {
            delta = 2 * M_PI;
        } else {
            delta = 0.0;
        }
        
        u = FACTOR * (S12 * Q12 + S23 * Q23 + S31 * Q31);
        v = FACTOR * (- C12 * Q12 - C23 * Q23 - C31 * Q31);
        w = FACTOR * sign * (delta + J12 + J23 + J31);

        if (print == 1)
        {
            printf("p: [%.4e, %.4e, %.4e]\n", p.x, p.y, p.z);
            printf("p1: [%.4e, %.4e, %.4e]\n", p1.x, p1.y, p1.z);
            printf("p2: [%.4e, %.4e, %.4e]\n", p2.x, p2.y, p2.z);
            printf("p3: [%.4e, %.4e, %.4e]\n", p3.x, p3.y, p3.z);
            printf("\n");
            printf("r: [%.4e, %.4e, %.4e]\n", r1, r2, r3);
            printf("d: [%.4e, %.4e, %.4e]\n", d12, d23, d31);
            printf("S: [%.4e, %.4e, %.4e]\n", S12, S23, S31);
            printf("C: [%.4e, %.4e, %.4e]\n", C12, C23, C31);
            printf("Q: [%.4e, %.4e, %.4e]\n", Q12, Q23, Q31);
            printf("R: [%.4e, %.4e, %.4e]\n", R12, R23, R31);
            printf("s: [[%.4e, %.4e], [%.4e, %.4e], [%.4e, %.4e]]\n", s12_1, s12_2, s23_2, s23_3, s31_3, s31_1);
            printf("J: [%.4e, %.4e, %.4e]\n", J12, J23, J31);
            printf("\n");
            printf("v: [%.2e, %.2e, %.2e]\n", u, v, w);
            exit(0);
        }

    }

    vel.x = u * e1.x + v * e2.x + w * e3.x;
    vel.y = u * e1.y + v * e2.y + w * e3.y;
    vel.z = u * e1.z + v * e2.z + w * e3.z;

    return vel;
}

Vec3D quad_source_panel(Vec3D p1, Vec3D p2, Vec3D p3, Vec3D p4, Vec3D p, Vec3D e1, Vec3D e2, Vec3D e3, double area, double max_distance, int print)
{

    Vec3D vel;
    double u, v, w;

    double distance = norm_vec(p);

    if (distance > max_distance) {

        double pNorm3 = pow(norm_vec(p), 3);

        u = FACTOR * area * p.x / pNorm3;
        v = FACTOR * area * p.y / pNorm3;
        w = FACTOR * area * p.z / pNorm3;

    } else {

        double r1, r2, r3, r4;
        double d12, d23, d34, d41;
        double S12, S23, S34, S41;
        double C12, C23, C34, C41;
        double Q12, Q23, Q34, Q41;
        double R12, R23, R34, R41;
        double J12, J23, J34, J41;

        double s12_1, s12_2;
        double s23_2, s23_3;
        double s34_3, s34_4;
        double s41_4, s41_1;

        double sign, delta;

        r1 = sqrt((p.x - p1.x) * (p.x - p1.x) + (p.y - p1.y) * (p.y - p1.y) + p.z * p.z);
        r2 = sqrt((p.x - p2.x) * (p.x - p2.x) + (p.y - p2.y) * (p.y - p2.y) + p.z * p.z);
        r3 = sqrt((p.x - p3.x) * (p.x - p3.x) + (p.y - p3.y) * (p.y - p3.y) + p.z * p.z);
        r4 = sqrt((p.x - p4.x) * (p.x - p4.x) + (p.y - p4.y) * (p.y - p4.y) + p.z * p.z);

        d12 = sqrt((p2.x - p1.x) * (p2.x - p1.x) + (p2.y - p1.y) * (p2.y - p1.y));
        d23 = sqrt((p3.x - p2.x) * (p3.x - p2.x) + (p3.y - p2.y) * (p3.y - p2.y));
        d34 = sqrt((p4.x - p3.x) * (p4.x - p3.x) + (p4.y - p3.y) * (p4.y - p3.y));
        d41 = sqrt((p1.x - p4.x) * (p1.x - p4.x) + (p1.y - p4.y) * (p1.y - p4.y));

        S12 = (p2.y - p1.y) / d12;
        S23 = (p3.y - p2.y) / d23;
        S34 = (p4.y - p3.y) / d34;
        S41 = (p1.y - p4.y) / d41;

        C12 = (p2.x - p1.x) / d12;
        C23 = (p3.x - p2.x) / d23;
        C34 = (p4.x - p3.x) / d34;
        C41 = (p1.x - p4.x) / d41;

        Q12 = log((r1 + r2 + d12) / (r1 + r2 - d12));
        Q23 = log((r2 + r3 + d23) / (r2 + r3 - d23));
        Q34 = log((r3 + r4 + d34) / (r3 + r4 - d34));
        Q41 = log((r4 + r1 + d41) / (r4 + r1 - d41));

        R12 = (p.x - p1.x) * S12 - (p.y - p1.y) * C12;
        R23 = (p.x - p2.x) * S23 - (p.y - p2.y) * C23;
        R34 = (p.x - p3.x) * S34 - (p.y - p3.y) * C34;
        R41 = (p.x - p4.x) * S41 - (p.y - p4.y) * C41;

        s12_1 = (p1.x - p.x) * C12 + (p1.y - p.y) * S12;
        s12_2 = (p2.x - p.x) * C12 + (p2.y - p.y) * S12;

        s23_2 = (p2.x - p.x) * C23 + (p2.y - p.y) * S23;
        s23_3 = (p3.x - p.x) * C23 + (p3.y - p.y) * S23;

        s34_3 = (p3.x - p.x) * C34 + (p3.y - p.y) * S34;
        s34_4 = (p4.x - p.x) * C34 + (p4.y - p.y) * S34;

        s41_4 = (p4.x - p.x) * C41 + (p4.y - p.y) * S41;
        s41_1 = (p1.x - p.x) * C41 + (p1.y - p.y) * S41;

        J12 = atan2( (R12 * fabs(p.z) * (r1 * s12_2 - r2 * s12_1)) , (r1 * r2 * R12 * R12 + p.z * p.z * s12_1 * s12_2) );
        J23 = atan2( (R23 * fabs(p.z) * (r2 * s23_3 - r3 * s23_2)) , (r2 * r3 * R23 * R23 + p.z * p.z * s23_2 * s23_3) );
        J34 = atan2( (R34 * fabs(p.z) * (r3 * s34_4 - r4 * s34_3)) , (r3 * r4 * R34 * R34 + p.z * p.z * s34_3 * s34_4) );
        J41 = atan2( (R41 * fabs(p.z) * (r4 * s41_1 - r1 * s41_4)) , (r4 * r1 * R41 * R41 + p.z * p.z * s41_4 * s41_1) );

        if (p.z < 0) {
            sign = - 1.0;
        } else {
            sign = 1.0;
        }

        if ((R12 < 0) && (R23 < 0) && (R34 < 0) && (R41 < 0)) {
            delta = 2 * M_PI;
        } else {
            delta = 0.0;
        }
        
        u = FACTOR * (S12 * Q12 + S23 * Q23 + S34 * Q34 + S41 * Q41);
        v = FACTOR * (- C12 * Q12 - C23 * Q23 - C34 * Q34 - C41 * Q41);
        w = FACTOR * sign * (delta + J12 + J23 + J34 + J41);

        // if (print)
        // {
        //     printf("[%.2e, %.2e, %.2e]\n", u, v, w);
        // }

    }

    vel.x = u * e1.x + v * e2.x + w * e3.x;
    vel.y = u * e1.y + v * e2.y + w * e3.y;
    vel.z = u * e1.z + v * e2.z + w * e3.z;

    return vel;

}

Vec3D line_vortex(Vec3D p1, Vec3D p2, Vec3D p)
{
    Vec3D vel;

    Vec3D r1 = {p.x - p1.x, p.y - p1.y, p.z - p1.z};
    Vec3D r2 = {p.x - p2.x, p.y - p2.y, p.z - p2.z};
    Vec3D r0 = {p2.x - p1.x, p2.y - p1.y, p2.z - p1.z};

    Vec3D r1xr2 = {r1.y * r2.z - r1.z * r2.y, r1.z * r2.x - r1.x * r2.z, r1.x * r2.y - r1.y * r2.x};

    double r1xr2_square = r1xr2.x * r1xr2.x + r1xr2.y * r1xr2.y + r1xr2.z * r1xr2.z;

    double r1_norm = sqrt(r1.x * r1.x + r1.y * r1.y + r1.z * r1.z);
    double r2_norm = sqrt(r2.x * r2.x + r2.y * r2.y + r2.z * r2.z);

    if ((r1_norm < ZERO_ERROR) || (r2_norm < ZERO_ERROR) || (r1xr2_square < ZERO_ERROR))
    {
        vel.x = 0.0;
        vel.y = 0.0;
        vel.z = 0.0;
    }
    else
    {
        double r0r1 = r0.x * r1.x + r0.y * r1.y + r0.z * r1.z;
        double r0r2 = r0.x * r2.x + r0.y * r2.y + r0.z * r2.z;
        
        double k = (1 / (4 * M_PI * r1xr2_square)) * (r0r1 / r1_norm - r0r2 / r2_norm);

        vel.x = k * r1xr2.x;
        vel.y = k * r1xr2.y;
        vel.z = k * r1xr2.z;
    }

    return vel;
}

Vec3D tri_doublet_panel(Vec3D p1, Vec3D p2, Vec3D p3, Vec3D p, Vec3D e1, Vec3D e2, Vec3D e3, double area, double max_distance)
{

    Vec3D vel;
    double u, v, w;

    double distance = norm_vec(p);

    if (distance > max_distance) {

        double den = pow(p.x * p.x + p.y * p.y + p.z * p.z, 2.5);

        u = 0.75 * FACTOR * area * p.z * p.x / den;
        v = 0.75 * FACTOR * area * p.z * p.y / den;
        w = - FACTOR * area * (p.x * p.x + p.y * p.y - 2 * p.z * p.z) / den;

    } else {

        Vec3D vel1;
        Vec3D vel2;
        Vec3D vel3;

        vel1 = line_vortex(p1, p2, p);
        vel2 = line_vortex(p2, p3, p);
        vel3 = line_vortex(p3, p1, p);
        
        u = vel1.x + vel2.x + vel3.x;
        v = vel1.y + vel2.y + vel3.y;
        w = vel1.z + vel2.z + vel3.z;
        
    }

    vel.x = u * e1.x + v * e2.x + w * e3.x;
    vel.y = u * e1.y + v * e2.y + w * e3.y;
    vel.z = u * e1.z + v * e2.z + w * e3.z;

    return vel;

}

Vec3D quad_doublet_panel(Vec3D p1, Vec3D p2, Vec3D p3, Vec3D p4, Vec3D p, Vec3D e1, Vec3D e2, Vec3D e3, double area, double max_distance)
{

    Vec3D vel;
    double u, v, w;

    double distance = norm_vec(p);

    if (distance > max_distance) {

        double den = pow(p.x * p.x + p.y * p.y + p.z * p.z, 2.5);

        u = 0.75 * FACTOR * area * p.z * p.x / den;
        v = 0.75 * FACTOR * area * p.z * p.y / den;
        w = - FACTOR * area * (p.x * p.x + p.y * p.y - 2 * p.z * p.z) / den;

    } else {

        Vec3D vel1;
        Vec3D vel2;
        Vec3D vel3;
        Vec3D vel4;

        vel1 = line_vortex(p1, p2, p);
        vel2 = line_vortex(p2, p3, p);
        vel3 = line_vortex(p3, p4, p);
        vel4 = line_vortex(p4, p1, p);
        
        u = vel1.x + vel2.x + vel3.x + vel4.x;
        v = vel1.y + vel2.y + vel3.y + vel4.y;
        w = vel1.z + vel2.z + vel3.z + vel4.z;
        
    }

    vel.x = u * e1.x + v * e2.x + w * e3.x;
    vel.y = u * e1.y + v * e2.y + w * e3.y;
    vel.z = u * e1.z + v * e2.z + w * e3.z;

    return vel;

}

Vec3D quad_inertial_doublet_panel(Vec3D p1, Vec3D p2, Vec3D p3, Vec3D p4, Vec3D p)
{

    Vec3D vel;

    Vec3D vel1;
    Vec3D vel2;
    Vec3D vel3;
    Vec3D vel4;

    vel1 = line_vortex(p1, p2, p);
    vel2 = line_vortex(p2, p3, p);
    vel3 = line_vortex(p3, p4, p);
    vel4 = line_vortex(p4, p1, p);
        
    vel.x = vel1.x + vel2.x + vel3.x + vel4.x;
    vel.y = vel1.y + vel2.y + vel3.y + vel4.y;
    vel.z = vel1.z + vel2.z + vel3.z + vel4.z;

    return vel;

}

Vec3D vel_doublet_sheet(Face face, Vec3D p_ctrl)
{

    Vec3D vel, p, p_local;

    p.x = p_ctrl.x - face.p_avg.x;
    p.y = p_ctrl.y - face.p_avg.y;
    p.z = p_ctrl.z - face.p_avg.z;

    p_local.x = dot_vec(p, face.e1);
    p_local.y = dot_vec(p, face.e2);
    p_local.z = dot_vec(p, face.e3);

    if (face.n_sides == 4) {
        vel = quad_doublet_panel(face.p1, face.p2, face.p3, face.p4, p_local, face.e1, face.e2, face.e3, face.area, face.max_distance);
    } else {
        vel = tri_doublet_panel(face.p1, face.p2, face.p3, p_local, face.e1, face.e2, face.e3, face.area, face.max_distance);
    }

    return vel;

}

Vec3D vel_source_sheet(Face face, Vec3D p_ctrl, int print)
{

    Vec3D vel, p, p_local;

    p.x = p_ctrl.x - face.p_avg.x;
    p.y = p_ctrl.y - face.p_avg.y;
    p.z = p_ctrl.z - face.p_avg.z;

    p_local.x = dot_vec(p, face.e1);
    p_local.y = dot_vec(p, face.e2);
    p_local.z = dot_vec(p, face.e3);

    if (face.n_sides == 4) {
        vel = quad_source_panel(face.p1, face.p2, face.p3, face.p4, p_local, face.e1, face.e2, face.e3, face.area, face.max_distance, print);
    } else {
        vel = tri_source_panel(face.p1, face.p2, face.p3, p_local, face.e1, face.e2, face.e3, face.area, face.max_distance, print);
    }

    return vel;

}