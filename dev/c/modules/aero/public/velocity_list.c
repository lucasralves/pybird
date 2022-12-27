#include "../../models/models.h"
#include "../private/point_velocity.h"

void velocity_list(double point_list[],
                   double vel_list[],
                   int n,
                   Mesh *mesh,
                   Aero *aero,
                   int wake_id)
{

    int i;
    
    Vec3D vel, p;

    for (i = 0; i < n; i++)
    {
        p.x = point_list[3 * i];
        p.y = point_list[3 * i + 1];
        p.z = point_list[3 * i + 2];

        vel = point_velocity(p, mesh, aero, wake_id, 0);

        vel_list[3 * i] = vel.x;
        vel_list[3 * i + 1] = vel.y;
        vel_list[3 * i + 2] = vel.z;
    }

}