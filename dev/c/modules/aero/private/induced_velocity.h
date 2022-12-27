#ifndef AERO_PRIVATE_INDUCED_VELOCITY_H
#define AERO_PRIVATE_INDUCED_VELOCITY_H

#include "../../models/models.h"

Vec3D vel_doublet_sheet(Face face, Vec3D p_ctrl);
Vec3D vel_source_sheet(Face face, Vec3D p_ctrl, int print);

#include "induced_velocity.c"

#endif