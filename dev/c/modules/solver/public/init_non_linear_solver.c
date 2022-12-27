#include <stdlib.h>

#include "../../models/models.h"

void init_non_linear_solver(int n_f, int n_te, Solver *solver)
{

    int i, j;

    solver->non_linear.n = n_f + n_te;
    solver->non_linear.na = solver->non_linear.n * solver->non_linear.n;
    solver->non_linear.lhs = (double*)malloc(solver->linear.na * sizeof(double));
    solver->non_linear.i_lhs = (int*)malloc(solver->linear.na * sizeof(int));
    solver->non_linear.j_lhs = (int*)malloc(solver->linear.na * sizeof(int));
    solver->non_linear.rhs = (double*)malloc(solver->linear.n * sizeof(double));
    solver->non_linear.x = (double*)malloc(solver->linear.n * sizeof(double));
    
    for (i = 0; i < solver->non_linear.n; i++)
    {
        for (j = 0; j < solver->non_linear.n; j++)
        {
            solver->non_linear.i_lhs[i * solver->non_linear.n + j] = i;
            solver->non_linear.j_lhs[i * solver->non_linear.n + j] = j;
        }
    }
}