#include <math.h>

#include "../../models/models.h"

double tri_face_area(Vec3D p1, Vec3D p2, Vec3D p3)
{

    Vec3D v1, v2, cross;

    v1.x = p2.x - p1.x;
    v1.y = p2.y - p1.y;
    v1.z = p2.z - p1.z;

    v2.x = p3.x - p1.x;
    v2.y = p3.y - p1.y;
    v2.z = p3.z - p1.z;

    cross.x = v1.y * v2.z - v1.z * v2.y;
    cross.y = v1.z * v2.x - v1.x * v2.z;
    cross.z = v1.x * v2.y - v1.y * v2.x;

    double norm;

    norm = sqrt(cross.x * cross.x + cross.y * cross.y + cross.z * cross.z);

    return 0.5 * norm;
}
