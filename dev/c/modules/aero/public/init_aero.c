#include <stdlib.h>
#include <math.h>

#include "../../models/models.h"
#include "../../math/math.h"

#include "../private/induced_velocity.h"

void init_aero(Mesh mesh,
               double freestream,
               double alpha,
               double beta,
               double delta_t,
               Aero *aero)
{

    int i, j;

    // Freestream
    double alpha_rad = alpha * M_PI / 180;
    double beta_rad = alpha * M_PI / 180;

    aero->freestream.x = freestream * cos(beta_rad) * cos(alpha_rad);
    aero->freestream.y = freestream * sin(beta_rad) * cos(alpha_rad);
    aero->freestream.z = freestream * sin(alpha_rad);

    // Fonte
    aero->source = (double*)malloc(mesh.n_f * sizeof(double));

    for (i = 0; i < mesh.n_f; i++)
    {
        aero->source[i] = - dot_vec(aero->freestream, mesh.faces[i].e3);
    }

    // Dipolo
    aero->doublet = (double*)malloc(mesh.n_f * sizeof(double));

    // Velocidade
    aero->vel = (Vec3D*)malloc(mesh.n_f * sizeof(Vec3D));

    // Coeficiente de pressão
    aero->cp = (double*)malloc(mesh.n_f * sizeof(double));

    // Transpiração
    aero->transpiration = (double*)malloc(mesh.n_f * sizeof(double));

    // Esteira
    aero->delta_t = delta_t;
    aero->wake = (Wake*)malloc(mesh.n_te * sizeof(Wake));

    for (i = 0; i < mesh.n_te; i++)
    {
        aero->wake[i].area = (double*)malloc((mesh.n_w - 1) * sizeof(double));
        aero->wake[i].circulation = (double*)malloc((mesh.n_w - 1) * sizeof(double));
    }

    // Velocidade induzida
    aero->vel_matrix_doublet = (Vec3D*)malloc(mesh.n_f * mesh.n_f * sizeof(Vec3D));
    aero->vel_array_source = (Vec3D*)malloc(mesh.n_f * sizeof(Vec3D));

    Vec3D vel_doublet, vel_source;

    int print;

    for (i = 0; i < mesh.n_f; i++)
    {
        
        aero->vel_array_source[i].x = 0.0;
        aero->vel_array_source[i].y = 0.0;
        aero->vel_array_source[i].z = 0.0;

        for (j = 0; j < mesh.n_f; j++)
        {
            
            if ((mesh.faces[j].n_sides == 3) && (i == j)) {
                print = 0;
            } else {
                print = 0;
            }
            
            vel_doublet = vel_doublet_sheet(mesh.faces[j], mesh.faces[i].p_ctrl);
            vel_source = vel_source_sheet(mesh.faces[j], mesh.faces[i].p_ctrl, print);
                        
            aero->vel_matrix_doublet[i * mesh.n_f + j].x = vel_doublet.x;
            aero->vel_matrix_doublet[i * mesh.n_f + j].y = vel_doublet.y;
            aero->vel_matrix_doublet[i * mesh.n_f + j].z = vel_doublet.z;

            aero->vel_array_source[i].x = aero->vel_array_source[i].x + aero->source[j] * vel_source.x;
            aero->vel_array_source[i].y = aero->vel_array_source[i].y + aero->source[j] * vel_source.y;
            aero->vel_array_source[i].z = aero->vel_array_source[i].z + aero->source[j] * vel_source.z;

        }

    }

}