typedef struct
{
    Vec3D freestream;
    double delta_t;
    double *source;
    double *doublet;
    Vec3D *vel;
    double *cp;
    double *transpiration;
    Wake *wake;
    Vec3D *vel_matrix_doublet;
    Vec3D *vel_array_source;
} Aero;