#include <stdio.h>

#include "modules/models/models.h"
#include "modules/mesh/mesh.h"
#include "modules/aero/aero.h"
#include "modules/solver/solver.h"

void main(int n_v,
          int n_f3,
          int n_f4,
          int n_te,
          int n_w,
          double delta_t,
          double vertices[],
          int faces3[],
          int faces4[],
          int trailing_edge[],
          double trailing_edge_points[],
          double freestream,
          double alpha,
          double beta,
          double source[],
          double doublet[],
          double vel_x[],
          double vel_y[],
          double vel_z[],
          double cp[],
          double transpiration[])
{

    printf(" > Aerodynamic Solver\n");

    /* Initialize */
    printf("   - Initializing modules\n");
    Mesh mesh;
    Aero aero;
    Solver solver;

    init_mesh(n_v, n_f3, n_f4, n_te, n_w, vertices, faces3, faces4, trailing_edge, &mesh);
    init_aero(mesh, freestream, alpha, beta, delta_t, &aero);
    init_linear_solver(mesh.n_f, &solver);

    /* Solve without wake */
    printf("   - Solving doublet without wake\n");
    calc_surface_doublet_strength(mesh, aero, solver);
    end_linear_solver(&solver);

    /* Create wake */
    // init_non_linear_solver(mesh.n_f, mesh.n_te, &solver);

    printf("   - Solving doublet with wake\n");
    calc_aero_params(&mesh, &aero);

    for (int wake_id = 0; wake_id < n_w - 1; wake_id++)
    {
        printf("     * Section: %d/%d\n", wake_id + 1, n_w - 1);
        update_wake(&mesh, &aero, wake_id);
        calc_surface_wake_doublet_strength(&mesh, &aero);
    }

    /* Calculate parameters */
    printf("   - Calculating surface parameters\n");
    calc_aero_params(&mesh, &aero);
    calc_vertices_params(&mesh, &aero, source, doublet, vel_x, vel_y, vel_z, cp, transpiration);

    /* Assign trailing edge parameters */
    assign_te_points(mesh, trailing_edge_points);

    /* End */
    end_mesh(&mesh);
    end_aero(mesh.n_te, &aero);
    // end_non_linear_solver(&solver);

}