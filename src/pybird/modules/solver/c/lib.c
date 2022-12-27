#include <stdio.h>
#include <math.h>

/*-------------------------------------------
    STRUCTS
--------------------------------------------*/
typedef struct {
    double x;
    double y;
    double z;
} Vec3D;

void print_vec(Vec3D a)
{
    printf("[%.2e, %.2e, %.2e]", a.x, a.y, a.z);
}

/*-------------------------------------------
    MATH
--------------------------------------------*/
double norm_func(Vec3D a)
{
    return sqrt(a.x * a.x + a.y * a.y + a.z * a.z);
}

double dot_func(Vec3D a,
                Vec3D b)
{
    return a.x * b.x + a.y * b.y + a.z * b.z;
}

double abs_func(double a)
{
    if (a < 0) {
        return - a;
    } else {
        return a;
    }
}

double division_func(double a,
                     double b)
{
    double b_abs = abs_func(b);

    if (b_abs < 1e-12) {
        return a * b / (b_abs * (b_abs + 1e-12));
    } else {
        return a / b;
    }
}

double distance_func(Vec3D a, Vec3D b)
{
    return sqrt((a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y) + (a.z - b.z) * (a.z - b.z));
}

void unary_func(Vec3D *a)
{
    double norm = sqrt(a->x * a->x + a->y * a->y + a->z * a->z);
    a->x = a->x / norm;
    a->y = a->y / norm;
    a->z = a->z / norm;
}

Vec3D cross_func(Vec3D a, Vec3D b)
{
    Vec3D out;
    out.x = a.y * b.z - a.z * b.y;
    out.y = a.z * b.x - a.x * b.z;
    out.z = a.x * b.y - a.y * b.x;
    return out;
}

double fabs_func(double a)
{
    if (a < 0) return - a;
    return a;
}

/*-------------------------------------------
    INDUCED VELOCITY
--------------------------------------------*/
const double ZERO_ERROR = 1e-12;
const double FACTOR = 0.25 / M_PI;

Vec3D tri_source_panel(Vec3D p,
                       Vec3D p1, Vec3D p2, Vec3D p3,
                       Vec3D e1, Vec3D e2, Vec3D e3,
                       double area,
                       double max_distance)
{

    Vec3D vel;
    double u, v, w;

    double distance = norm_func(p);

    if (distance > max_distance) {

        double pNorm3 = pow(norm_func(p), 3);

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
    }

    vel.x = u * e1.x + v * e2.x + w * e3.x;
    vel.y = u * e1.y + v * e2.y + w * e3.y;
    vel.z = u * e1.z + v * e2.z + w * e3.z;

    return vel;
}

Vec3D quad_source_panel(Vec3D p,
                        Vec3D p1, Vec3D p2, Vec3D p3, Vec3D p4,
                        Vec3D e1, Vec3D e2, Vec3D e3,
                        double area,
                        double max_distance)
{

    Vec3D vel;
    double u, v, w;

    double distance = norm_func(p);

    if (distance > max_distance) {

        double pNorm3 = pow(norm_func(p), 3);

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
    }

    vel.x = u * e1.x + v * e2.x + w * e3.x;
    vel.y = u * e1.y + v * e2.y + w * e3.y;
    vel.z = u * e1.z + v * e2.z + w * e3.z;

    return vel;

}

Vec3D line_vortex(Vec3D p, Vec3D p1, Vec3D p2)
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

// double quad_doublet_pot(Vec3D p,
//                         Vec3D p1, Vec3D p2, Vec3D p3, Vec3D p4)
// {

//     double pot;

//     double r1, r2, r3, r4;
//     double d12, d23, d34, d41;
//     double S12, S23, S34, S41;
//     double C12, C23, C34, C41;
//     double R12, R23, R34, R41;
//     double J12, J23, J34, J41;

//     double s12_1, s12_2;
//     double s23_2, s23_3;
//     double s34_3, s34_4;
//     double s41_4, s41_1;

//     double sign, delta;

//     r1 = sqrt((p.x - p1.x) * (p.x - p1.x) + (p.y - p1.y) * (p.y - p1.y) + p.z * p.z);
//     r2 = sqrt((p.x - p2.x) * (p.x - p2.x) + (p.y - p2.y) * (p.y - p2.y) + p.z * p.z);
//     r3 = sqrt((p.x - p3.x) * (p.x - p3.x) + (p.y - p3.y) * (p.y - p3.y) + p.z * p.z);
//     r4 = sqrt((p.x - p4.x) * (p.x - p4.x) + (p.y - p4.y) * (p.y - p4.y) + p.z * p.z);

//     d12 = sqrt((p2.x - p1.x) * (p2.x - p1.x) + (p2.y - p1.y) * (p2.y - p1.y));
//     d23 = sqrt((p3.x - p2.x) * (p3.x - p2.x) + (p3.y - p2.y) * (p3.y - p2.y));
//     d34 = sqrt((p4.x - p3.x) * (p4.x - p3.x) + (p4.y - p3.y) * (p4.y - p3.y));
//     d41 = sqrt((p1.x - p4.x) * (p1.x - p4.x) + (p1.y - p4.y) * (p1.y - p4.y));

//     S12 = (p2.y - p1.y) / d12;
//     S23 = (p3.y - p2.y) / d23;
//     S34 = (p4.y - p3.y) / d34;
//     S41 = (p1.y - p4.y) / d41;

//     C12 = (p2.x - p1.x) / d12;
//     C23 = (p3.x - p2.x) / d23;
//     C34 = (p4.x - p3.x) / d34;
//     C41 = (p1.x - p4.x) / d41;

//     R12 = (p.x - p1.x) * S12 - (p.y - p1.y) * C12;
//     R23 = (p.x - p2.x) * S23 - (p.y - p2.y) * C23;
//     R34 = (p.x - p3.x) * S34 - (p.y - p3.y) * C34;
//     R41 = (p.x - p4.x) * S41 - (p.y - p4.y) * C41;

//     s12_1 = (p1.x - p.x) * C12 + (p1.y - p.y) * S12;
//     s12_2 = (p2.x - p.x) * C12 + (p2.y - p.y) * S12;

//     s23_2 = (p2.x - p.x) * C23 + (p2.y - p.y) * S23;
//     s23_3 = (p3.x - p.x) * C23 + (p3.y - p.y) * S23;

//     s34_3 = (p3.x - p.x) * C34 + (p3.y - p.y) * S34;
//     s34_4 = (p4.x - p.x) * C34 + (p4.y - p.y) * S34;

//     s41_4 = (p4.x - p.x) * C41 + (p4.y - p.y) * S41;
//     s41_1 = (p1.x - p.x) * C41 + (p1.y - p.y) * S41;

//     J12 = atan2( (R12 * fabs(p.z) * (r1 * s12_2 - r2 * s12_1)) , (r1 * r2 * R12 * R12 + p.z * p.z * s12_1 * s12_2) );
//     J23 = atan2( (R23 * fabs(p.z) * (r2 * s23_3 - r3 * s23_2)) , (r2 * r3 * R23 * R23 + p.z * p.z * s23_2 * s23_3) );
//     J34 = atan2( (R34 * fabs(p.z) * (r3 * s34_4 - r4 * s34_3)) , (r3 * r4 * R34 * R34 + p.z * p.z * s34_3 * s34_4) );
//     J41 = atan2( (R41 * fabs(p.z) * (r4 * s41_1 - r1 * s41_4)) , (r4 * r1 * R41 * R41 + p.z * p.z * s41_4 * s41_1) );

//     if (p.z < 0) {
//         sign = - 1.0;
//     } else {
//         sign = 1.0;
//     }

//     if ((R12 < 0) && (R23 < 0) && (R34 < 0) && (R41 < 0)) {
//         delta = 2 * M_PI;
//     } else {
//         delta = 0.0;
//     }
        
//     pot = FACTOR * sign * (delta + J12 + J23 + J34 + J41);

//     return pot;

// }

// double tri_doublet_pot(Vec3D p,
//                        Vec3D p1, Vec3D p2, Vec3D p3)
// {

//     double pot;

//     double r1, r2, r3;
//     double d12, d23, d31;
//     double S12, S23, S31;
//     double C12, C23, C31;
//     double Q12, Q23, Q31;
//     double R12, R23, R31;
//     double J12, J23, J31;

//     double s12_1, s12_2;
//     double s23_2, s23_3;
//     double s31_3, s31_1;

//     double sign, delta;

//     r1 = sqrt((p.x - p1.x) * (p.x - p1.x) + (p.y - p1.y) * (p.y - p1.y) + p.z * p.z);
//     r2 = sqrt((p.x - p2.x) * (p.x - p2.x) + (p.y - p2.y) * (p.y - p2.y) + p.z * p.z);
//     r3 = sqrt((p.x - p3.x) * (p.x - p3.x) + (p.y - p3.y) * (p.y - p3.y) + p.z * p.z);

//     d12 = sqrt((p2.x - p1.x) * (p2.x - p1.x) + (p2.y - p1.y) * (p2.y - p1.y));
//     d23 = sqrt((p3.x - p2.x) * (p3.x - p2.x) + (p3.y - p2.y) * (p3.y - p2.y));
//     d31 = sqrt((p1.x - p3.x) * (p1.x - p3.x) + (p1.y - p3.y) * (p1.y - p3.y));

//     S12 = (p2.y - p1.y) / d12;
//     S23 = (p3.y - p2.y) / d23;
//     S31 = (p1.y - p3.y) / d31;

//     C12 = (p2.x - p1.x) / d12;
//     C23 = (p3.x - p2.x) / d23;
//     C31 = (p1.x - p3.x) / d31;

//     R12 = (p.x - p1.x) * S12 - (p.y - p1.y) * C12;
//     R23 = (p.x - p2.x) * S23 - (p.y - p2.y) * C23;
//     R31 = (p.x - p3.x) * S31 - (p.y - p3.y) * C31;

//     s12_1 = (p1.x - p.x) * C12 + (p1.y - p.y) * S12;
//     s12_2 = (p2.x - p.x) * C12 + (p2.y - p.y) * S12;

//     s23_2 = (p2.x - p.x) * C23 + (p2.y - p.y) * S23;
//     s23_3 = (p3.x - p.x) * C23 + (p3.y - p.y) * S23;

//     s31_3 = (p3.x - p.x) * C31 + (p3.y - p.y) * S31;
//     s31_1 = (p1.x - p.x) * C31 + (p1.y - p.y) * S31;

//     J12 = atan2( (R12 * fabs(p.z) * (r1 * s12_2 - r2 * s12_1)) , (r1 * r2 * R12 * R12 + p.z * p.z * s12_1 * s12_2) );
//     J23 = atan2( (R23 * fabs(p.z) * (r2 * s23_3 - r3 * s23_2)) , (r2 * r3 * R23 * R23 + p.z * p.z * s23_2 * s23_3) );
//     J31 = atan2( (R31 * fabs(p.z) * (r3 * s31_1 - r1 * s31_3)) , (r3 * r1 * R31 * R31 + p.z * p.z * s31_3 * s31_1) );

//     if (p.z < 0) {
//         sign = - 1.0;
//     } else {
//         sign = 1.0;
//     }

//     if ((R12 < 0) && (R23 < 0) && (R31 < 0)) {
//         delta = 2 * M_PI;
//     } else {
//         delta = 0.0;
//     }

//     pot = FACTOR * sign * (delta + J12 + J23 + J31);

//     return pot;

// }

Vec3D tri_doublet_panel(Vec3D p,
                        Vec3D p1, Vec3D p2, Vec3D p3,
                        Vec3D e1, Vec3D e2, Vec3D e3,
                        double area,
                        double max_distance)
{
    Vec3D vel, p_local;

    p_local.x = dot_func(p, e1);
    p_local.y = dot_func(p, e2);
    p_local.z = dot_func(p, e3);

    double distance = norm_func(p);
    double u, v, w;

    if (distance > max_distance) {

        double den = pow(p.x * p.x + p.y * p.y + p.z * p.z, 2.5);

        u = 0.75 * FACTOR * area * p.z * p.x / den;
        v = 0.75 * FACTOR * area * p.z * p.y / den;
        w = - FACTOR * area * (p.x * p.x + p.y * p.y - 2 * p.z * p.z) / den;
    
    } else {

        Vec3D vel1, vel2, vel3, vel4;

        vel1 = line_vortex(p, p1, p2);
        vel2 = line_vortex(p, p2, p3);
        vel3 = line_vortex(p, p3, p1);

        u = vel1.x + vel2.x + vel3.x;
        v = vel1.y + vel2.y + vel3.y;
        w = vel1.z + vel2.z + vel3.z;
    }

    vel.x = u * e1.x + v * e2.x + w * e3.x;
    vel.y = u * e1.y + v * e2.y + w * e3.y;
    vel.z = u * e1.z + v * e2.z + w * e3.z;

    return vel;
}

Vec3D quad_doublet_panel(Vec3D p,
                         Vec3D p1, Vec3D p2, Vec3D p3, Vec3D p4,
                         Vec3D e1, Vec3D e2, Vec3D e3,
                         double area,
                         double max_distance)
{
    Vec3D vel, p_local;

    p_local.x = dot_func(p, e1);
    p_local.y = dot_func(p, e2);
    p_local.z = dot_func(p, e3);

    double distance = norm_func(p);
    double u, v, w;

    if (distance > max_distance) {

        double den = pow(p.x * p.x + p.y * p.y + p.z * p.z, 2.5);

        u = 0.75 * FACTOR * area * p.z * p.x / den;
        v = 0.75 * FACTOR * area * p.z * p.y / den;
        w = - FACTOR * area * (p.x * p.x + p.y * p.y - 2 * p.z * p.z) / den;
    
    } else {

        Vec3D vel1, vel2, vel3, vel4;

        vel1 = line_vortex(p, p1, p2);
        vel2 = line_vortex(p, p2, p3);
        vel3 = line_vortex(p, p3, p4);
        vel4 = line_vortex(p, p4, p1);

        u = vel1.x + vel2.x + vel3.x + vel4.x;
        v = vel1.y + vel2.y + vel3.y + vel4.y;
        w = vel1.z + vel2.z + vel3.z + vel4.z;
    }

    vel.x = u * e1.x + v * e2.x + w * e3.x;
    vel.y = u * e1.y + v * e2.y + w * e3.y;
    vel.z = u * e1.z + v * e2.z + w * e3.z;

    return vel;
}

Vec3D vel_doublet_sheet(int n_sides,
                        Vec3D p,
                        Vec3D e1, Vec3D e2, Vec3D e3,
                        Vec3D p1, Vec3D p2, Vec3D p3, Vec3D p4,
                        double area,
                        double max_distance)
{

    Vec3D vel, p_local;

    p_local.x = dot_func(p, e1);
    p_local.y = dot_func(p, e2);
    p_local.z = dot_func(p, e3);

    if (n_sides == 4) {
        vel = quad_doublet_panel(p_local, p1, p2, p3, p4, e1, e2, e3, area, max_distance);
    } else {
        vel = tri_doublet_panel(p_local, p1, p2, p3, e1, e2, e3, area, max_distance);
    }

    return vel;
}

Vec3D vel_source_sheet(int n_sides,
                       Vec3D p,
                       Vec3D e1, Vec3D e2, Vec3D e3,
                       Vec3D p1, Vec3D p2, Vec3D p3, Vec3D p4,
                       double area,
                       double max_distance)
{

    Vec3D vel, p_local;

    p_local.x = dot_func(p, e1);
    p_local.y = dot_func(p, e2);
    p_local.z = dot_func(p, e3);

    if (n_sides == 4) {
        vel = quad_source_panel(p_local, p1, p2, p3, p4, e1, e2, e3, area, max_distance);
    } else {
        vel = tri_source_panel(p_local, p1, p2, p3, e1, e2, e3, area, max_distance);
    }

    return vel;
}

/*-------------------------------------------
    Aij and Bi COEFS
--------------------------------------------*/
void get_Aij_and_Bi_coefs(int nf,
                          int n_sides[],
                          double p_avg[],
                          double p_ctrl[],
                          double e1[],
                          double e2[],
                          double e3[],
                          double p1[],
                          double p2[],
                          double p3[],
                          double p4[],
                          double areas[],
                          double max_distances[],
                          double scale[],
                          double freestream[],
                          double source[],
                          double Aij_x[],
                          double Aij_y[],
                          double Aij_z[],
                          double Bi_x[],
                          double Bi_y[],
                          double Bi_z[])
{
    int i, j;

    int n_sides_j;
    Vec3D p_ij;
    Vec3D e1_j, e2_j, e3_j;
    Vec3D p1_j, p2_j, p3_j, p4_j;
    double area_j;
    double max_distance_j;

    Vec3D vel_source, vel_doublet;

    for (i = 0; i < nf; i++)
    {

        Bi_x[i] = freestream[0];
        Bi_y[i] = freestream[1];
        Bi_z[i] = freestream[2];

        for (j = 0; j < nf; j++)
        {

            n_sides_j = n_sides[j];

            p_ij.x = p_ctrl[3 * i] - p_avg[3 * j]; p_ij.y = p_ctrl[3 * i + 1] - p_avg[3 * j + 1]; p_ij.z = p_ctrl[3 * i + 2] - p_avg[3 * j + 2];

            e1_j.x = e1[3 * j]; e1_j.y = e1[3 * j + 1]; e1_j.z = e1[3 * j + 2];
            e2_j.x = e2[3 * j]; e2_j.y = e2[3 * j + 1]; e2_j.z = e2[3 * j + 2];
            e3_j.x = e3[3 * j]; e3_j.y = e3[3 * j + 1]; e3_j.z = e3[3 * j + 2];

            p1_j.x = p1[2 * j]; p1_j.y = p1[2 * j + 1]; p1_j.z = 0.0;
            p2_j.x = p2[2 * j]; p2_j.y = p2[2 * j + 1]; p2_j.z = 0.0;
            p3_j.x = p3[2 * j]; p3_j.y = p3[2 * j + 1]; p3_j.z = 0.0;
            p4_j.x = p4[2 * j]; p4_j.y = p4[2 * j + 1]; p4_j.z = 0.0;

            area_j = areas[j];
            max_distance_j = max_distances[j];

            vel_doublet = vel_doublet_sheet(n_sides_j, p_ij, e1_j, e2_j, e3_j, p1_j, p2_j, p3_j, p4_j, area_j, max_distance_j);
            vel_source = vel_source_sheet(n_sides_j, p_ij, e1_j, e2_j, e3_j, p1_j, p2_j, p3_j, p4_j, area_j, max_distance_j);

            Bi_x[i] = Bi_x[i] + source[j] * vel_source.x;
            Bi_y[i] = Bi_y[i] + source[j] * vel_source.y;
            Bi_z[i] = Bi_z[i] + source[j] * vel_source.z;

            Aij_x[i * nf + j] = vel_doublet.x;
            Aij_y[i * nf + j] = vel_doublet.y;
            Aij_z[i * nf + j] = vel_doublet.z;
        
        }
    }

}

/*-------------------------------------------
    Get the velocity at a point
--------------------------------------------*/
void get_point_velocity(int nf,
                        int nte,
                        int nw,
                        int wake_id,
                        int n_sides[],
                        double p_avg[],
                        double e1[],
                        double e2[],
                        double e3[],
                        double p1[],
                        double p2[],
                        double p3[],
                        double p4[],
                        double areas[],
                        double max_distances[],
                        double freestream[],
                        double source[],
                        double doublet[],
                        int wake_ids[],
                        double wake_vertices[],
                        double wake_areas[],
                        double wake_circulation[],
                        double p[],
                        int skip_i, int skip_j,
                        double vel[])
{
    int i, j;

    int n_sides_j;
    Vec3D p_ij;
    Vec3D e1_j, e2_j, e3_j;
    Vec3D p1_j, p2_j, p3_j, p4_j;
    double area_j;
    double max_distance_j;

    Vec3D vel_source, vel_doublet;

    vel[0] = freestream[0];
    vel[1] = freestream[1];
    vel[2] = freestream[2];

    // Surface
    for (j = 0; j < nf; j++)
    {

        n_sides_j = n_sides[j];

        p_ij.x = p[0] - p_avg[3 * j]; p_ij.y = p[1] - p_avg[3 * j + 1]; p_ij.z = p[2] - p_avg[3 * j + 2];

        e1_j.x = e1[3 * j]; e1_j.y = e1[3 * j + 1]; e1_j.z = e1[3 * j + 2];
        e2_j.x = e2[3 * j]; e2_j.y = e2[3 * j + 1]; e2_j.z = e2[3 * j + 2];
        e3_j.x = e3[3 * j]; e3_j.y = e3[3 * j + 1]; e3_j.z = e3[3 * j + 2];

        p1_j.x = p1[2 * j]; p1_j.y = p1[2 * j + 1]; p1_j.z = 0.0;
        p2_j.x = p2[2 * j]; p2_j.y = p2[2 * j + 1]; p2_j.z = 0.0;
        p3_j.x = p3[2 * j]; p3_j.y = p3[2 * j + 1]; p3_j.z = 0.0;
        p4_j.x = p4[2 * j]; p4_j.y = p4[2 * j + 1]; p4_j.z = 0.0;

        area_j = areas[j];
        max_distance_j = max_distances[j];

        vel_doublet = vel_doublet_sheet(n_sides_j, p_ij, e1_j, e2_j, e3_j, p1_j, p2_j, p3_j, p4_j, area_j, max_distance_j);
        vel_source = vel_source_sheet(n_sides_j, p_ij, e1_j, e2_j, e3_j, p1_j, p2_j, p3_j, p4_j, area_j, max_distance_j);

        vel[0] = vel[0] + doublet[j] * vel_doublet.x + source[j] * vel_source.x;
        vel[1] = vel[1] + doublet[j] * vel_doublet.y + source[j] * vel_source.y;
        vel[2] = vel[2] + doublet[j] * vel_doublet.z + source[j] * vel_source.z;
        
    }

    // Wake
    int id1, id2, id3, id4;
    int indexes[3];
    int shape[3];

    Vec3D v, v1, v2, v3, v4;
    Vec3D p_avg_wake;

    Vec3D vec1, vec2;

    v.x = p[0]; v.y = p[1]; v.z = p[2];

    for (i = 0; i < nte; i++)
    {
        for (j = 0; j < wake_id; j++)
        {
            // Vertices ids
            shape[0] = nte; shape[1] = nw; shape[2] = 2;
            indexes[0] = i;

            indexes[1] = j; indexes[2] = 0;
            id1 = wake_ids[indexes[0] * shape[1] * shape[2] + indexes[1] * shape[2] + indexes[2]];
            
            indexes[1] = j; indexes[2] = 1;
            id2 = wake_ids[indexes[0] * shape[1] * shape[2] + indexes[1] * shape[2] + indexes[2]];
            
            indexes[1] = j + 1; indexes[2] = 1;
            id3 = wake_ids[indexes[0] * shape[1] * shape[2] + indexes[1] * shape[2] + indexes[2]];
            
            indexes[1] = j + 1; indexes[2] = 0;
            id4 = wake_ids[indexes[0] * shape[1] * shape[2] + indexes[1] * shape[2] + indexes[2]];

            // Vertices vectors
            v1.x = wake_vertices[3 * id1]; v1.y = wake_vertices[3 * id1 + 1]; v1.z = wake_vertices[3 * id1 + 2];
            v2.x = wake_vertices[3 * id2]; v2.y = wake_vertices[3 * id2 + 1]; v2.z = wake_vertices[3 * id2 + 2];
            v3.x = wake_vertices[3 * id3]; v3.y = wake_vertices[3 * id3 + 1]; v3.z = wake_vertices[3 * id3 + 2];
            v4.x = wake_vertices[3 * id4]; v4.y = wake_vertices[3 * id4 + 1]; v4.z = wake_vertices[3 * id4 + 2];

            // Check
            if ((i == skip_i) && (j == skip_j)) continue;
            if ((distance_func(v, v1) < 1e-5) || (distance_func(v, v2) < 1e-5) || (distance_func(v, v3) < 1e-5) || (distance_func(v, v4) < 1e-5)) continue;
            
            // Average point
            p_avg_wake.x = 0.25 * (v1.x + v2.x + v3.x + v4.x); p_avg_wake.y = 0.25 * (v1.y + v2.y + v3.y + v4.y); p_avg_wake.z = 0.25 * (v1.z + v2.z + v3.z + v4.z);

            // e3
            vec1.x = v2.x - v4.x; vec1.y = v2.y - v4.y; vec1.z = v2.z - v4.z;
            vec2.x = v3.x - v1.x; vec2.y = v3.y - v1.y; vec2.z = v3.z - v1.z;

            e3_j = cross_func(vec1, vec2);
            unary_func(&e3_j);

            // e1
            e1_j.x = 1.0; e1_j.y = 1.0; e1_j.z = 1.0;

            if (fabs_func(e3_j.x > 1e-2)) {
                e1_j.x = - (e3_j.y + e3_j.z) / e3_j.x;
            } else {
                if (fabs_func(e3_j.y > 1e-2)) {
                    e1_j.y = - (e3_j.x + e3_j.z) / e3_j.y;
                } else {
                    e1_j.z = - (e3_j.x + e3_j.y) / e3_j.z;
                }
            }

            unary_func(&e1_j);

            // e2
            e2_j = cross_func(e3_j, e1_j);
            unary_func(&e2_j);

            // Points
            v1.x = v1.x - p_avg_wake.x; v1.y = v1.y - p_avg_wake.y; v1.z = v1.z - p_avg_wake.z;
            v2.x = v2.x - p_avg_wake.x; v2.y = v2.y - p_avg_wake.y; v2.z = v2.z - p_avg_wake.z;
            v3.x = v3.x - p_avg_wake.x; v3.y = v3.y - p_avg_wake.y; v3.z = v3.z - p_avg_wake.z;
            v4.x = v4.x - p_avg_wake.x; v4.y = v4.y - p_avg_wake.y; v4.z = v4.z - p_avg_wake.z;

            p1_j.x = dot_func(v1, e1_j); p1_j.y = dot_func(v1, e2_j); p1_j.z = 0.0;
            p2_j.x = dot_func(v2, e1_j); p2_j.y = dot_func(v2, e2_j); p2_j.z = 0.0;
            p3_j.x = dot_func(v3, e1_j); p3_j.y = dot_func(v3, e2_j); p3_j.z = 0.0;
            p4_j.x = dot_func(v4, e1_j); p4_j.y = dot_func(v4, e2_j); p4_j.z = 0.0;

            // Area
            vec1.x = v2.x - v1.x; vec1.y = v2.y - v1.y; vec1.z = v2.z - v1.z;
            vec2.x = v3.x - v1.x; vec2.y = v3.y - v1.y; vec2.z = v3.z - v1.z;

            area_j = 0.5 * norm_func(cross_func(vec1, vec2));

            vec1.x = v3.x - v1.x; vec1.y = v3.y - v1.y; vec1.z = v3.z - v1.z;
            vec2.x = v4.x - v1.x; vec2.y = v4.y - v1.y; vec2.z = v4.z - v1.z;

            area_j = area_j + 0.5 * norm_func(cross_func(vec1, vec2));

            // Max distance
            max_distance_j = 10 * 2 * sqrt(area_j / M_PI);

            // Point
            vec1.x = p[0] - p_avg_wake.x; vec1.y = p[1] - p_avg_wake.y; vec1.z = p[2] - p_avg_wake.z;

            p_ij.x = dot_func(vec1, e1_j);
            p_ij.y = dot_func(vec1, e2_j);
            p_ij.z = dot_func(vec1, e3_j);

            // Velocity
            vel_doublet = vel_doublet_sheet(n_sides_j, p_ij, e1_j, e2_j, e3_j, p1_j, p2_j, p3_j, p4_j, area_j, max_distance_j);
            
            shape[0] = nte; shape[1] = nw - 1; shape[2] = 2;
            indexes[0] = i; indexes[1] = j; indexes[2] = 0;

            vel[0] = vel[0] + (wake_areas[indexes[0] * shape[1] + indexes[1]] / area_j) * wake_circulation[indexes[0] * shape[1] + indexes[1]] * vel_doublet.x;
            vel[1] = vel[1] + (wake_areas[indexes[0] * shape[1] + indexes[1]] / area_j) * wake_circulation[indexes[0] * shape[1] + indexes[1]] * vel_doublet.y;
            vel[2] = vel[2] + (wake_areas[indexes[0] * shape[1] + indexes[1]] / area_j) * wake_circulation[indexes[0] * shape[1] + indexes[1]] * vel_doublet.z;
        }
    }
}

/*-------------------------------------------
    Get the velocity at a point
--------------------------------------------*/
void get_Cij(int nf,
             int nte,
             int nw,
             double p_ctrl[],
             int wake_ids[],
             double wake_vertices[],
             double Cij_x[],
             double Cij_y[],
             double Cij_z[])
{
    int i, j;

    int n_sides_j;
    Vec3D p_ij;
    Vec3D e1_j, e2_j, e3_j;
    Vec3D p1_j, p2_j, p3_j, p4_j;
    double area_j;
    double max_distance_j;

    Vec3D vel_doublet;

    int id1, id2, id3, id4;
    int indexes[3];
    int shape[3];

    Vec3D v, v1, v2, v3, v4;
    Vec3D p_avg_wake;

    Vec3D vec1, vec2;

    for (i = 0; i < nte; i++)
    {
        // Vertices ids
        shape[0] = nte; shape[1] = nw; shape[2] = 2;
        indexes[0] = i;

        indexes[1] = 0; indexes[2] = 0;
        id1 = wake_ids[indexes[0] * shape[1] * shape[2] + indexes[1] * shape[2] + indexes[2]];
            
        indexes[1] = 0; indexes[2] = 1;
        id2 = wake_ids[indexes[0] * shape[1] * shape[2] + indexes[1] * shape[2] + indexes[2]];
            
        indexes[1] = 1; indexes[2] = 1;
        id3 = wake_ids[indexes[0] * shape[1] * shape[2] + indexes[1] * shape[2] + indexes[2]];
            
        indexes[1] = 1; indexes[2] = 0;
        id4 = wake_ids[indexes[0] * shape[1] * shape[2] + indexes[1] * shape[2] + indexes[2]];

        // Vertices vectors
        v1.x = wake_vertices[3 * id1]; v1.y = wake_vertices[3 * id1 + 1]; v1.z = wake_vertices[3 * id1 + 2];
        v2.x = wake_vertices[3 * id2]; v2.y = wake_vertices[3 * id2 + 1]; v2.z = wake_vertices[3 * id2 + 2];
        v3.x = wake_vertices[3 * id3]; v3.y = wake_vertices[3 * id3 + 1]; v3.z = wake_vertices[3 * id3 + 2];
        v4.x = wake_vertices[3 * id4]; v4.y = wake_vertices[3 * id4 + 1]; v4.z = wake_vertices[3 * id4 + 2];
            
        // Average point
        p_avg_wake.x = 0.25 * (v1.x + v2.x + v3.x + v4.x); p_avg_wake.y = 0.25 * (v1.y + v2.y + v3.y + v4.y); p_avg_wake.z = 0.25 * (v1.z + v2.z + v3.z + v4.z);

        // e3
        vec1.x = v2.x - v4.x; vec1.y = v2.y - v4.y; vec1.z = v2.z - v4.z;
        vec2.x = v3.x - v1.x; vec2.y = v3.y - v1.y; vec2.z = v3.z - v1.z;

        e3_j = cross_func(vec1, vec2);
        unary_func(&e3_j);

        // e1
        e1_j.x = 1.0; e1_j.y = 1.0; e1_j.z = 1.0;

        if (fabs_func(e3_j.x > 1e-2)) {
            e1_j.x = - (e3_j.y + e3_j.z) / e3_j.x;
        } else {
            if (fabs_func(e3_j.y > 1e-2)) {
                e1_j.y = - (e3_j.x + e3_j.z) / e3_j.y;
            } else {
                e1_j.z = - (e3_j.x + e3_j.y) / e3_j.z;
            }
        }
        
        unary_func(&e1_j);

        // e2
        e2_j = cross_func(e3_j, e1_j);
        unary_func(&e2_j);

        // Points
        v1.x = v1.x - p_avg_wake.x; v1.y = v1.y - p_avg_wake.y; v1.z = v1.z - p_avg_wake.z;
        v2.x = v2.x - p_avg_wake.x; v2.y = v2.y - p_avg_wake.y; v2.z = v2.z - p_avg_wake.z;
        v3.x = v3.x - p_avg_wake.x; v3.y = v3.y - p_avg_wake.y; v3.z = v3.z - p_avg_wake.z;
        v4.x = v4.x - p_avg_wake.x; v4.y = v4.y - p_avg_wake.y; v4.z = v4.z - p_avg_wake.z;

        p1_j.x = dot_func(v1, e1_j); p1_j.y = dot_func(v1, e2_j); p1_j.z = 0.0;
        p2_j.x = dot_func(v2, e1_j); p2_j.y = dot_func(v2, e2_j); p2_j.z = 0.0;
        p3_j.x = dot_func(v3, e1_j); p3_j.y = dot_func(v3, e2_j); p3_j.z = 0.0;
        p4_j.x = dot_func(v4, e1_j); p4_j.y = dot_func(v4, e2_j); p4_j.z = 0.0;

        // Area
        vec1.x = v2.x - v1.x; vec1.y = v2.y - v1.y; vec1.z = v2.z - v1.z;
        vec2.x = v3.x - v1.x; vec2.y = v3.y - v1.y; vec2.z = v3.z - v1.z;

        area_j = 0.5 * norm_func(cross_func(vec1, vec2));

        vec1.x = v3.x - v1.x; vec1.y = v3.y - v1.y; vec1.z = v3.z - v1.z;
        vec2.x = v4.x - v1.x; vec2.y = v4.y - v1.y; vec2.z = v4.z - v1.z;

        area_j = area_j + 0.5 * norm_func(cross_func(vec1, vec2));

        // Max distance
        max_distance_j = 10 * 2 * sqrt(area_j / M_PI);

        for (j = 0; j < nf; j++)
        {

            // Point
            vec1.x = p_ctrl[3 * j] - p_avg_wake.x; vec1.y = p_ctrl[3 * j + 1] - p_avg_wake.y; vec1.z = p_ctrl[3 * j + 2] - p_avg_wake.z;

            p_ij.x = dot_func(vec1, e1_j);
            p_ij.y = dot_func(vec1, e2_j);
            p_ij.z = dot_func(vec1, e3_j);

            // Velocity
            vel_doublet = vel_doublet_sheet(n_sides_j, p_ij, e1_j, e2_j, e3_j, p1_j, p2_j, p3_j, p4_j, area_j, max_distance_j);

            Cij_x[i * nte + j] = vel_doublet.x;
            Cij_y[i * nte + j] = vel_doublet.y;
            Cij_z[i * nte + j] = vel_doublet.z;

        }
    }
}