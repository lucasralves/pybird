#include <math.h>

#include "../../models/models.h"
#include "../../math/math.h"

void calc_aero_params(Mesh *mesh, Aero *aero)
{

    int i, j;

    double freestream_norm = sqrt(aero->freestream.x * aero->freestream.x + aero->freestream.y * aero->freestream.y + aero->freestream.z * aero->freestream.z);

    for (i = 0; i < mesh->n_f; i++)
    {

        aero->vel[i].x = aero->vel_array_source[i].x + aero->freestream.x;
        aero->vel[i].y = aero->vel_array_source[i].y + aero->freestream.y;
        aero->vel[i].z = aero->vel_array_source[i].z + aero->freestream.z;

        for (j = 0; j < mesh->n_f; j++)
        {
            aero->vel[i].x = aero->vel[i].x + aero->doublet[j] * aero->vel_matrix_doublet[i * mesh->n_f + j].x;
            aero->vel[i].y = aero->vel[i].y + aero->doublet[j] * aero->vel_matrix_doublet[i * mesh->n_f + j].y;
            aero->vel[i].z = aero->vel[i].z + aero->doublet[j] * aero->vel_matrix_doublet[i * mesh->n_f + j].z;
        }

        aero->cp[i] = 1 - sqrt(aero->vel[i].x * aero->vel[i].x + aero->vel[i].y * aero->vel[i].y + aero->vel[i].z * aero->vel[i].z) / freestream_norm;
    
        aero->transpiration[i] = dot_vec(aero->vel[i], mesh->faces[i].e3);
    
    }



}