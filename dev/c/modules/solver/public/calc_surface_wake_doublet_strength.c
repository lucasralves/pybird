#include "../../models/models.h"
#include "../../mesh/private/tri_face_area.h"

void calc_surface_wake_doublet_strength(Mesh *mesh, Aero *aero)
{

    int i;

    for (i = 0; i < mesh->n_te; i++)
    {
        aero->wake[i].area[0] = tri_face_area(mesh->trailing_edge[i].filament1[0], mesh->trailing_edge[i].filament2[0], mesh->trailing_edge[i].filament2[1]) + tri_face_area(mesh->trailing_edge[i].filament1[0], mesh->trailing_edge[i].filament2[0], mesh->trailing_edge[i].filament1[1]);
        aero->wake[i].circulation[0] = - 5.0; // aero->doublet[mesh->trailing_edge[i].f1] - aero->doublet[mesh->trailing_edge[i].f2];
    }

}