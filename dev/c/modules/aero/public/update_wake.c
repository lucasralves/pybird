#include <math.h>
#include <stdlib.h>

#include "../../models/models.h"
#include "../private/induced_velocity.h"
#include "../../mesh/private/tri_face_area.h"
#include "../private/point_velocity.h"

/*
    Calcula a velocidade em um vértice do bordo de fuga.
*/
Vec3D te_vertice_velocity(int v_id, Mesh *mesh, Aero *aero)
{

    // return aero->freestream;

    int i;

    Vec3D vel;

    vel.x = 0.0;
    vel.y = 0.0;
    vel.z = 0.0;

    for (i = 0; i < mesh->vertices_connection[v_id].n; i++)
    {
        vel.x = vel.x + aero->vel[mesh->vertices_connection[v_id].faces[i]].x;
        vel.y = vel.y + aero->vel[mesh->vertices_connection[v_id].faces[i]].y;
        vel.z = vel.z + aero->vel[mesh->vertices_connection[v_id].faces[i]].z;
    }

    vel.x = vel.x / mesh->vertices_connection[v_id].n;
    vel.y = vel.y / mesh->vertices_connection[v_id].n;
    vel.z = vel.z / mesh->vertices_connection[v_id].n;

    return vel;

}

typedef struct
{
    Vec3D *filament1;
    Vec3D *filament2;
} WakeDisplacement;

void update_wake(Mesh *mesh, Aero *aero, int wake_id)
{

    int i, j;

    Vec3D vel1, vel2;

    WakeDisplacement *wake_disp;
    wake_disp = (WakeDisplacement*)malloc(mesh->n_te * sizeof(WakeDisplacement));

    for (i = 0; i < mesh->n_te; i++)
    {
        wake_disp[i].filament1 = (Vec3D*)malloc((wake_id + 1) * sizeof(Vec3D));
        wake_disp[i].filament2 = (Vec3D*)malloc((wake_id + 1) * sizeof(Vec3D));
    }

    // Calculate velocity
    int print;
    for (i = 0; i < mesh->n_te; i++)
    {
        for (j = 0; j <= wake_id; j++)
        {
            if (j == 0) { // Trailing edge
                vel1 = te_vertice_velocity(mesh->trailing_edge[i].v1, mesh, aero);
                vel2 = te_vertice_velocity(mesh->trailing_edge[i].v2, mesh, aero);
            } else { // Wake sheet

                if (j == wake_id) {
                    print = 1;
                } else {
                    print = 0;
                }

                vel1 = point_velocity(mesh->trailing_edge[i].filament1[j], mesh, aero, j, print);
                vel2 = point_velocity(mesh->trailing_edge[i].filament2[j], mesh, aero, j, 0);
            }

            wake_disp[i].filament1[j].x = aero->delta_t * vel1.x;
            wake_disp[i].filament1[j].y = aero->delta_t * vel1.y;
            wake_disp[i].filament1[j].z = aero->delta_t * vel1.z;

            wake_disp[i].filament2[j].x = aero->delta_t * vel2.x;
            wake_disp[i].filament2[j].y = aero->delta_t * vel2.y;
            wake_disp[i].filament2[j].z = aero->delta_t * vel2.z;
        }
    }

    for (i = 0; i < mesh->n_te; i++)
    {
        for (j = wake_id; j >= 0; j--)
        {
            mesh->trailing_edge[i].filament1[j + 1].x = mesh->trailing_edge[i].filament1[j].x + wake_disp[i].filament1[j].x;
            mesh->trailing_edge[i].filament1[j + 1].y = mesh->trailing_edge[i].filament1[j].y + wake_disp[i].filament1[j].y;
            mesh->trailing_edge[i].filament1[j + 1].z = mesh->trailing_edge[i].filament1[j].z + wake_disp[i].filament1[j].z;

            mesh->trailing_edge[i].filament2[j + 1].x = mesh->trailing_edge[i].filament2[j].x + wake_disp[i].filament2[j].x;
            mesh->trailing_edge[i].filament2[j + 1].y = mesh->trailing_edge[i].filament2[j].y + wake_disp[i].filament2[j].y;
            mesh->trailing_edge[i].filament2[j + 1].z = mesh->trailing_edge[i].filament2[j].z + wake_disp[i].filament2[j].z;

        }
    }

    for (i = 0; i < mesh->n_te; i++)
    {
        free(wake_disp[i].filament1);
        free(wake_disp[i].filament2);
    }

    free(wake_disp);

    // Update position
    if (wake_id > 0)
    {
        for (i = 0; i < mesh->n_te; i++)
        {
            for (j = wake_id; j >= 0; j--)
            {
                aero->wake[i].area[wake_id] = aero->wake[i].area[wake_id - 1];
                aero->wake[i].circulation[wake_id] = aero->wake[i].circulation[wake_id - 1];
            }
        }
    }

}