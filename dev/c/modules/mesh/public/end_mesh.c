#include <stdlib.h>

#include "../../models/models.h"

void end_mesh(Mesh *mesh)
{

    int i;

    free(mesh->vertices);

    free(mesh->faces);

    for (i = 0; i < mesh->n_v; i++) free(mesh->vertices_connection[i].faces);

    free(mesh->vertices_connection);

    for (i = 0; i < mesh->n_te; i++)
    {
        free(mesh->trailing_edge[i].filament1);
        free(mesh->trailing_edge[i].filament2);
    }

    free(mesh->trailing_edge);

}