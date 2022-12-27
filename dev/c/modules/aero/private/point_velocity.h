#ifndef AERO_POINT_VELOCITY_H
#define AERO_POINT_VELOCITY_H

#include "../../models/models.h"

Vec3D point_velocity(Vec3D p, Mesh *mesh, Aero *aero, int wake_id, int print);

#include "point_velocity.c"

#endif