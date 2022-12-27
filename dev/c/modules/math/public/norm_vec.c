#include <math.h>

#include "../../models/models.h"

double norm_vec(Vec3D a)
{
    return sqrt(a.x * a.x + a.y * a.y + a.z * a.z);
}