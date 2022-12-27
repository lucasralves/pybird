#include "../../models/models.h"
#include "../../math/math.h"

#include "../private/gmres.h"

void calc_surface_doublet_strength(Mesh mesh, Aero aero, Solver solver)
{

    int i, j;

    printf("     * Creating linear system\n");
    for (i = 0; i < mesh.n_f; i++)
    {
        solver.linear.x[i] = 0.0;
        solver.linear.rhs[i] = - dot_vec(aero.freestream, mesh.faces[i].e3) - dot_vec(aero.vel_array_source[i], mesh.faces[i].e3);
        for (j = 0; j < mesh.n_f; j++)
        {
            solver.linear.lhs[i * solver.linear.n + j] = dot_vec(aero.vel_matrix_doublet[i * solver.linear.n + j], mesh.faces[i].e3);
        }
    }
    
    printf("     * Solving linear system\n");
    gmres(solver.linear.n, solver.linear.na, solver.linear.lhs, solver.linear.i_lhs, solver.linear.j_lhs, solver.linear.rhs, solver.linear.x);

    for (i = 0; i < mesh.n_f; i++)
    {
        aero.doublet[i] = solver.linear.x[i];
    }
}