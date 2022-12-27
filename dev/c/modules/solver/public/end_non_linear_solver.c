#include <stdlib.h>

#include "../../models/models.h"

void end_non_linear_solver(Solver *solver)
{
    free(solver->linear.lhs);
    free(solver->linear.i_lhs);
    free(solver->linear.j_lhs);
    free(solver->linear.rhs);
    free(solver->linear.x);
}