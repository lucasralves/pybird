typedef struct
{
    int n_sides;
    int v1, v2, v3, v4;
    Vec3D p1, p2, p3, p4;
    Vec3D e1, e2, e3;
    Vec3D p_avg;
    Vec3D p_ctrl;
    double area;
    double max_distance;
} Face;