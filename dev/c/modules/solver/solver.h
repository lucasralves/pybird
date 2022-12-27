#ifndef SOLVER_H
#define SOLVER_H

#include "../models/models.h"

/*
    Inicializa as variáveis
*/
void init_linear_solver(int n_f, Solver *solver);
void init_non_linear_solver(int n_f, int n_te, Solver *solver);

/*
    Monta o sistema linear e calcula a força dos dipolos
*/
void calc_surface_doublet_strength(Mesh mesh, Aero aero, Solver solver);

/*
    Calcula a força dos dipolos utilizando o método
    de Newton para resolver sistemas não lineares
*/
void calc_surface_wake_doublet_strength(Mesh *mesh, Aero *aero);

/*
    Libera as variáveis alocadas manualmente
*/
void end_linear_solver(Solver *solver);
void end_non_linear_solver(Solver *solver);

#include "public/init_linear_solver.c"
#include "public/init_non_linear_solver.c"
#include "public/calc_surface_doublet_strength.c"
#include "public/calc_surface_wake_doublet_strength.c"
#include "public/end_linear_solver.c"
#include "public/end_non_linear_solver.c"

#endif