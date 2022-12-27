#ifndef MESH_H
#define MESH_H

#include "../models/models.h"

/*
    Inicializa as variáveis
*/

void init_mesh(int n_v,
               int n_f3,
               int n_f4,
               int n_te,
               int n_w,
               double *vertices,
               int *faces3,
               int *faces4,
               int *trailing_edge,
               Mesh *mesh);

/*
    Calcula as variáveis abaixo nos vértices da malha:
     - fonte
     - dipolo
     - velocidade (x, y, z)
     - coeficiente de pressão (cp)
     - transpiração
*/
void calc_vertices_params(Mesh *mesh,
                          Aero *aero,
                          double source[],
                          double doublet[],
                          double vel_x[],
                          double vel_y[],
                          double vel_z[],
                          double cp[],
                          double transpiration[]);

/*
    Libera as variáveis alocadas manualmente
*/
void end_mesh(Mesh *mesh);

#include "public/init_mesh.c"
#include "public/calc_vertices_params.c"
#include "public/end_mesh.c"
#include "public/assign_te_points.c"

#endif