#include <stdlib.h>

#include "../../models/models.h"

void init_linear_solver(int n_f, Solver *solver)
{

    int i, j;

    solver->linear.n = n_f;
    solver->linear.na = n_f * n_f;
    solver->linear.lhs = (double*)malloc(solver->linear.na * sizeof(double));
    solver->linear.i_lhs = (int*)malloc(solver->linear.na * sizeof(int));
    solver->linear.j_lhs = (int*)malloc(solver->linear.na * sizeof(int));
    solver->linear.rhs = (double*)malloc(solver->linear.n * sizeof(double));
    solver->linear.x = (double*)malloc(solver->linear.n * sizeof(double));
    
    for (i = 0; i < solver->linear.n; i++)
    {
        for (j = 0; j < solver->linear.n; j++)
        {
            solver->linear.i_lhs[i * solver->linear.n + j] = i;
            solver->linear.j_lhs[i * solver->linear.n + j] = j;
        }
    }

}