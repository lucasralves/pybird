#include "../../models/models.h"
#include "induced_velocity.h"

Vec3D point_velocity(Vec3D p, Mesh *mesh, Aero *aero, int wake_id, int print)
{
    int i, j;

    Vec3D vel, vel_doublet, vel_source, vel_1, vel_2, vel_3, vel_4;

    vel.x = aero->freestream.x;
    vel.y = aero->freestream.y;
    vel.z = aero->freestream.z;

    // Surface vel
    for (j = 0; j < mesh->n_f; j++)
    {
        vel_doublet = vel_doublet_sheet(mesh->faces[j], p);
        vel_source = vel_source_sheet(mesh->faces[j], p, 0);

        vel.x = vel.x + aero->doublet[j] * vel_doublet.x + aero->source[j] * vel_source.x;
        vel.y = vel.y + aero->doublet[j] * vel_doublet.y + aero->source[j] * vel_source.y;
        vel.z = vel.z + aero->doublet[j] * vel_doublet.z + aero->source[j] * vel_source.z;
    }

    // Wake vel
    double area;

    for (i = 0; i < mesh->n_te; i++)
    {
        for (j = 0; j < wake_id; j++)
        {
            vel_1 = line_vortex(mesh->trailing_edge[i].filament2[j], mesh->trailing_edge[i].filament2[j + 1], p);
            vel_2 = line_vortex(mesh->trailing_edge[i].filament1[j + 1], mesh->trailing_edge[i].filament1[j], p);
            vel_3 = line_vortex(mesh->trailing_edge[i].filament1[j], mesh->trailing_edge[i].filament2[j], p);
            vel_4 = line_vortex(mesh->trailing_edge[i].filament2[j + 1], mesh->trailing_edge[i].filament1[j + 1], p);

            // printf("eps: [%.2e, %.2e, %.2e]; vel: [%.2e, %.2e, %.2e]\n", mesh->trailing_edge[i].filament2[j + 1].x - mesh->trailing_edge[i].filament1[j + 1].x, mesh->trailing_edge[i].filament2[j + 1].y - mesh->trailing_edge[i].filament1[j + 1].y, mesh->trailing_edge[i].filament2[j + 1].z - mesh->trailing_edge[i].filament1[j + 1].z, vel_4.x, vel_4.y, vel_4.z);
            
            // if (j == wake_id - 1) {} else {
            //     vel_4.x = 0.0; vel_4.y = 0.0; vel_4.z = 0.0;
            // }

            // if (print)
            // {
            //     printf("[%.2e, %.2e, %.2e]\n", vel_4.x, vel_4.y, vel_4.z);
            // }

            if (j == 0) {} else {
                vel_3.x = 0.0; vel_3.y = 0.0; vel_3.z = 0.0;
            }

            vel_1.x = 0.0; vel_1.y = 0.0; vel_1.z = 0.0;
            vel_2.x = 0.0; vel_2.y = 0.0; vel_2.z = 0.0;
            // vel_3.x = 0.0; vel_3.y = 0.0; vel_3.z = 0.0;
            vel_4.x = 0.0; vel_4.y = 0.0; vel_4.z = 0.0;

            vel_doublet.x = + vel_1.x + vel_2.x + vel_3.x + vel_4.x;
            vel_doublet.y = + vel_1.y + vel_2.y + vel_3.y + vel_4.y;
            vel_doublet.z = + vel_1.z + vel_2.z + vel_3.z + vel_4.z;

            // vel_doublet = quad_inertial_doublet_panel(mesh->trailing_edge[i].filament1[j], mesh->trailing_edge[i].filament2[j], mesh->trailing_edge[i].filament2[j + 1], mesh->trailing_edge[i].filament1[j + 1], p);
            area = tri_face_area(mesh->trailing_edge[i].filament1[j], mesh->trailing_edge[i].filament2[j], mesh->trailing_edge[i].filament2[j + 1]) + tri_face_area(mesh->trailing_edge[i].filament1[j], mesh->trailing_edge[i].filament2[j], mesh->trailing_edge[i].filament1[j + 1]);
            
            vel.x = vel.x + vel_doublet.x * aero->wake[i].circulation[j] * aero->wake[i].area[j] / (area + ZERO_ERROR);
            vel.y = vel.y + vel_doublet.y * aero->wake[i].circulation[j] * aero->wake[i].area[j] / (area + ZERO_ERROR);
            vel.z = vel.z + vel_doublet.z * aero->wake[i].circulation[j] * aero->wake[i].area[j] / (area + ZERO_ERROR);
        }
    }

    return vel;
}