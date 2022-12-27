#ifndef AERO_H
#define AERO_H

#include "../models/models.h"

/*
    Inicializa as variáveis
*/
void init_aero(Mesh mesh,
               double freestream,
               double alpha,
               double beta,
               double delta_t,
               Aero *aero);

/*
    Calcula a velocidade nos vértices da esteira e
    atualiza a posição dos vértices
*/
void update_wake(Mesh *mesh, Aero *aero, int wake_id);

/*
    Calcula os parâmetros abaixo nas faces:
     - velocidade (x, y, z)
     - transpiração
     - coeficiente de pressão (cp)
*/
void calc_aero_params(Mesh *mesh, Aero *aero);

/*
    Calcula os parâmetros abaixo nas faces:
     - velocidade (x, y, z)
     - transpiração
     - coeficiente de pressão (cp)
*/
void velocity_list(double point_list[],
                   double vel_list[],
                   int n,
                   Mesh *mesh,
                   Aero *aero,
                   int wake_id);

/*
    Libera as variáveis alocadas manualmente
*/
void end_aero(int n_te, Aero *aero);

#include "public/init_aero.c"
#include "public/calc_aero_params.c"
#include "public/update_wake.c"
#include "public/velocity_list.c"
#include "public/end_aero.c"

#endif