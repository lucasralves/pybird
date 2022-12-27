#include "../../models/models.h"

void calc_vertices_params(Mesh *mesh,
                          Aero *aero,
                          double source[],
                          double doublet[],
                          double vel_x[],
                          double vel_y[],
                          double vel_z[],
                          double cp[],
                          double transpiration[])
{

    int i, j;

    for (i = 0; i < mesh->n_v; i++)
    {

        source[i] = 0.0;
        doublet[i] = 0.0;
        vel_x[i] = 0.0;
        vel_y[i] = 0.0;
        vel_z[i] = 0.0;
        cp[i] = 0.0;
        transpiration[i] = 0.0;

        for (j = 0; j < mesh->vertices_connection[i].n; j++)
        {
            source[i] = source[i] + aero->source[mesh->vertices_connection[i].faces[j]];
            doublet[i] = doublet[i] + aero->doublet[mesh->vertices_connection[i].faces[j]];
            vel_x[i] = vel_x[i] + aero->vel[mesh->vertices_connection[i].faces[j]].x;
            vel_y[i] = vel_y[i] + aero->vel[mesh->vertices_connection[i].faces[j]].y;
            vel_z[i] = vel_z[i] + aero->vel[mesh->vertices_connection[i].faces[j]].z;
            cp[i] = cp[i] + aero->cp[mesh->vertices_connection[i].faces[j]];
            transpiration[i] = transpiration[i] + aero->transpiration[mesh->vertices_connection[i].faces[j]];
        }

        source[i] = source[i] / mesh->vertices_connection[i].n;
        doublet[i] = doublet[i] / mesh->vertices_connection[i].n;
        vel_x[i] = vel_x[i] / mesh->vertices_connection[i].n;
        vel_y[i] = vel_y[i] / mesh->vertices_connection[i].n;
        vel_z[i] = vel_z[i] / mesh->vertices_connection[i].n;
        cp[i] = cp[i] / mesh->vertices_connection[i].n;
        transpiration[i] = transpiration[i] / mesh->vertices_connection[i].n;

    }

}