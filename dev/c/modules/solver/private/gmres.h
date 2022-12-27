#ifndef SOLVER_PRIVATE_GMRES_H
#define SOLVER_PRIVATE_GMRES_H

void gmres(int n, int na, double *a, int *ia, int *ja, double *rhs, double *x);

#include "gmres.c"

#endif