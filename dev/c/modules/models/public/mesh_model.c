typedef struct
{
    int n_v;
    int n_f;
    int n_te;
    int n_w;
    Vec3D *vertices;
    Face *faces;
    VerticesConnection *vertices_connection;
    TrailingEdge *trailing_edge;
} Mesh;