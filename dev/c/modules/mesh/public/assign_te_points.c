#include "../../models/models.h"

void assign_te_points(Mesh mesh, double trailing_edge_points[])
{

    int i, j;

    for (i = 0; i < mesh.n_te; i++)
    {
        for (j = 0; j < mesh.n_w; j++)
        {
            trailing_edge_points[i * 6 * mesh.n_w + j] = mesh.trailing_edge[i].filament1[j].x;
            trailing_edge_points[i * 6 * mesh.n_w + mesh.n_w + j] = mesh.trailing_edge[i].filament1[j].y;
            trailing_edge_points[i * 6 * mesh.n_w + 2 * mesh.n_w + j] = mesh.trailing_edge[i].filament1[j].z;

            trailing_edge_points[i * 6 * mesh.n_w + 3 * mesh.n_w + j] = mesh.trailing_edge[i].filament2[j].x;
            trailing_edge_points[i * 6 * mesh.n_w + 3 * mesh.n_w + mesh.n_w + j] = mesh.trailing_edge[i].filament2[j].y;
            trailing_edge_points[i * 6 * mesh.n_w + 3 * mesh.n_w + 2 * mesh.n_w + j] = mesh.trailing_edge[i].filament2[j].z;
        }
    }

}