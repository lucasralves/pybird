#ifndef MATH_H
#define MATH_H

#include "../models/models.h"

double norm_vec(Vec3D a);
double dot_vec(Vec3D a, Vec3D b);
double abs_d(double a);
double division(double a, double b);

#include "public/norm_vec.c"
#include "public/dot_vec.c"
#include "public/abs_d.c"
#include "public/division.c"

#endif