#include <stdio.h>
#include <stdlib.h>

#include "../../models/models.h"
#include "../../math/math.h"
#include "../private/tri_face_area.h"

void print_face(Face face)
{
    printf("# struct (Face):\n");
    printf("n_sides = %d\n", face.n_sides);
    printf("# v1, v2, v3, v4:\n");
    printf("v1 = %d\n", face.v1);
    printf("v2 = %d\n", face.v2);
    printf("v3 = %d\n", face.v3);
    printf("v4 = %d\n", face.v4);
    printf("# p1, p2, p3, p4:\n");
    printf("p1 = [%.2e, %.2e, %.2e]\n", face.p1.x, face.p1.y, face.p1.z);
    printf("p2 = [%.2e, %.2e, %.2e]\n", face.p2.x, face.p2.y, face.p2.z);
    printf("p3 = [%.2e, %.2e, %.2e]\n", face.p3.x, face.p3.y, face.p3.z);
    printf("p4 = [%.2e, %.2e, %.2e]\n", face.p4.x, face.p4.y, face.p4.z);
    printf("# e1, e2, e3:\n");
    printf("e1 = [%.2e, %.2e, %.2e]\n", face.e1.x, face.e1.y, face.e1.z);
    printf("e2 = [%.2e, %.2e, %.2e]\n", face.e2.x, face.e2.y, face.e2.z);
    printf("e3 = [%.2e, %.2e, %.2e]\n", face.e3.x, face.e3.y, face.e3.z);
    printf("p_ctrl = [%.2e, %.2e, %.2e]\n", face.p_ctrl.x, face.p_ctrl.y, face.p_ctrl.z);
    printf("p_avg = [%.2e, %.2e, %.2e]\n", face.p_avg.x, face.p_avg.y, face.p_avg.z);
    printf("area = %.2e\n", face.area);
    printf("max_distance = %.2e\n", face.max_distance);
}

void cross_vec(Vec3D p1, Vec3D p2, Vec3D *p)
{
    p->x = p1.y * p2.z - p1.z * p2.y;
    p->y = p1.z * p2.x - p1.x * p2.z;
    p->z = p1.x * p2.y - p1.y * p2.x;
}

Face create_quad_face(Vec3D v1, Vec3D v2, Vec3D v3, Vec3D v4, int v1_id, int v2_id, int v3_id, int v4_id, int index)
{

    /* Parametros */
    Vec3D vec_1, vec_2, vec_3, vec_4;
    Vec3D vec_0_local, vec_1_local, vec_2_local, vec_3_local, vec_4_local;
    double norm;

    /* Saída */
    Face face;

    /* Número de lados */
    face.n_sides = 4;

    /* Id dos vértices */
    face.v1 = v1_id;
    face.v2 = v2_id;
    face.v3 = v3_id;
    face.v4 = v4_id;

    /* Ponto central */
    face.p_avg.x = 0.25 * (v1.x + v2.x + v3.x + v4.x); face.p_avg.y = 0.25 * (v1.y + v2.y + v3.y + v4.y); face.p_avg.z = 0.25 * (v1.z + v2.z + v3.z + v4.z);

    /* Vetores unitários */

    // e3
    vec_1.x = v2.x - v4.x; vec_1.y = v2.y - v4.y; vec_1.z = v2.z - v4.z;
    vec_2.x = v3.x - v1.x; vec_2.y = v3.y - v1.y; vec_2.z = v3.z - v1.z;

    cross_vec(vec_1, vec_2, &vec_3);
    
    norm = norm_vec(vec_3);

    face.e3.x = vec_3.x / norm; face.e3.y = vec_3.y / norm; face.e3.z = vec_3.z / norm;
    
    // e1
    vec_1.x = 1.0; vec_1.y = 1.0; vec_1.z = 1.0;
    if (abs_d(face.e3.x) > 1e-2) {
        vec_1.x = - (face.e3.y * vec_1.y + face.e3.z * vec_1.z) / face.e3.x;
    } else {
        if (abs_d(face.e3.y) > 1e-2) {
            vec_1.y = - (face.e3.x * vec_1.x + face.e3.z * vec_1.z) / face.e3.y;
        } else {
            vec_1.z = - (face.e3.x * vec_1.x + face.e3.y * vec_1.y) / face.e3.z;
        }
    }
    norm = norm_vec(vec_1);

    face.e1.x = vec_1.x / norm; face.e1.y = vec_1.y / norm; face.e1.z = vec_1.z / norm;

    // e2
    cross_vec(face.e3, face.e1, &vec_2);
    norm = norm_vec(vec_2);
    
    face.e2.x = vec_2.x / norm; face.e2.y = vec_2.y / norm; face.e2.z = vec_2.z / norm;

    // Ponto de controle
    face.p_ctrl.x = face.p_avg.x + face.e3.x * 1e-8; face.p_ctrl.y = face.p_avg.y + face.e3.y * 1e-8; face.p_ctrl.z = face.p_avg.z + face.e3.z * 1e-8;

    // Pontos no plano
    vec_1.x = v1.x - face.p_avg.x; vec_1.y = v1.y - face.p_avg.y; vec_1.z = v1.z - face.p_avg.z;
    vec_2.x = v2.x - face.p_avg.x; vec_2.y = v2.y - face.p_avg.y; vec_2.z = v2.z - face.p_avg.z;
    vec_3.x = v3.x - face.p_avg.x; vec_3.y = v3.y - face.p_avg.y; vec_3.z = v3.z - face.p_avg.z;
    vec_4.x = v4.x - face.p_avg.x; vec_4.y = v4.y - face.p_avg.y; vec_4.z = v4.z - face.p_avg.z;

    vec_1_local.x = dot_vec(vec_1, face.e1); vec_1_local.y = dot_vec(vec_1, face.e2); vec_1_local.z = 0.0;
    vec_2_local.x = dot_vec(vec_2, face.e1); vec_2_local.y = dot_vec(vec_2, face.e2); vec_2_local.z = 0.0;
    vec_3_local.x = dot_vec(vec_3, face.e1); vec_3_local.y = dot_vec(vec_3, face.e2); vec_3_local.z = 0.0;
    vec_4_local.x = dot_vec(vec_4, face.e1); vec_4_local.y = dot_vec(vec_4, face.e2); vec_4_local.z = 0.0;

    vec_0_local.x = 0.25 * (vec_1_local.x + vec_2_local.x + vec_3_local.x + vec_4_local.x); vec_0_local.y = 0.25 * (vec_1_local.y + vec_2_local.y + vec_3_local.y + vec_4_local.y); vec_0_local.z = 0.25 * (vec_1_local.z + vec_2_local.z + vec_3_local.z + vec_4_local.z);

    face.p1.x = vec_1_local.x - vec_0_local.x; face.p1.y = vec_1_local.y - vec_0_local.y; face.p1.z = vec_1_local.z - vec_0_local.z;
    face.p2.x = vec_2_local.x - vec_0_local.x; face.p2.y = vec_2_local.y - vec_0_local.y; face.p2.z = vec_2_local.z - vec_0_local.z;
    face.p3.x = vec_3_local.x - vec_0_local.x; face.p3.y = vec_3_local.y - vec_0_local.y; face.p3.z = vec_3_local.z - vec_0_local.z;
    face.p4.x = vec_4_local.x - vec_0_local.x; face.p4.y = vec_4_local.y - vec_0_local.y; face.p4.z = vec_4_local.z - vec_0_local.z;

    /* Area */
    face.area = tri_face_area(face.p1, face.p2, face.p3) + tri_face_area(face.p1, face.p3, face.p4);

    /* Max. distance */
    face.max_distance = 10 * 2 * sqrt(face.area / M_PI);
    
    // if (index == 50)
    // {
    //     print_face(face);
    //     printf("vert1 = [%.3e, %.3e, %.3e]\n", v1.x, v1.y, v1.z);
    //     printf("vert2 = [%.3e, %.3e, %.3e]\n", v2.x, v2.y, v2.z);
    //     printf("vert3 = [%.3e, %.3e, %.3e]\n", v3.x, v3.y, v3.z);
    //     printf("vert4 = [%.3e, %.3e, %.3e]\n", v4.x, v4.y, v4.z);
    //     exit(0);
    // }

    return face;

}

Face create_tri_face(Vec3D v1, Vec3D v2, Vec3D v3, int v1_id, int v2_id, int v3_id, int index)
{

    /* Parametros */
    Vec3D vec_1, vec_2, vec_3;
    Vec3D vec_0_local, vec_1_local, vec_2_local, vec_3_local;
    double norm;

    /* Saída */
    Face face;

    /* Número de lados */
    face.n_sides = 3;

    /* Id dos vértices */
    face.v1 = v1_id;
    face.v2 = v2_id;
    face.v3 = v3_id;

    /* Ponto central */
    face.p_avg.x = (1.0 / 3.0) * (v1.x + v2.x + v3.x); face.p_avg.y = (1.0 / 3.0) * (v1.y + v2.y + v3.y); face.p_avg.z = (1.0 / 3.0) * (v1.z + v2.z + v3.z);

    /* Vetores unitários */

    // e3
    vec_1.x = v2.x - v1.x; vec_1.y = v2.y - v1.y; vec_1.z = v2.z - v1.z;
    vec_2.x = v3.x - v1.x; vec_2.y = v3.y - v1.y; vec_2.z = v3.z - v1.z;

    cross_vec(vec_1, vec_2, &vec_3);
    
    norm = norm_vec(vec_3);

    face.e3.x = vec_3.x / norm; face.e3.y = vec_3.y / norm; face.e3.z = vec_3.z / norm;
    
    // e1
    vec_1.x = 1.0; vec_1.y = 1.0; vec_1.z = 1.0;
    if (abs_d(face.e3.x) > 1e-2) {
        vec_1.x = - (face.e3.y * vec_1.y + face.e3.z * vec_1.z) / face.e3.x;
    } else {
        if (abs_d(face.e3.y) > 1e-2) {
            vec_1.y = - (face.e3.x * vec_1.x + face.e3.z * vec_1.z) / face.e3.y;
        } else {
            vec_1.z = - (face.e3.x * vec_1.x + face.e3.y * vec_1.y) / face.e3.z;
        }
    }
    norm = norm_vec(vec_1);

    face.e1.x = vec_1.x / norm; face.e1.y = vec_1.y / norm; face.e1.z = vec_1.z / norm;

    // e2
    cross_vec(face.e3, face.e1, &vec_2);
    norm = norm_vec(vec_2);
    
    face.e2.x = vec_2.x / norm; face.e2.y = vec_2.y / norm; face.e2.z = vec_2.z / norm;

    // Ponto de controle
    face.p_ctrl.x = face.p_avg.x + face.e3.x * 1e-8; face.p_ctrl.y = face.p_avg.y + face.e3.y * 1e-8; face.p_ctrl.z = face.p_avg.z + face.e3.z * 1e-8;

    // Pontos no plano
    vec_1.x = v1.x - face.p_avg.x; vec_1.y = v1.y - face.p_avg.y; vec_1.z = v1.z - face.p_avg.z;
    vec_2.x = v2.x - face.p_avg.x; vec_2.y = v2.y - face.p_avg.y; vec_2.z = v2.z - face.p_avg.z;
    vec_3.x = v3.x - face.p_avg.x; vec_3.y = v3.y - face.p_avg.y; vec_3.z = v3.z - face.p_avg.z;

    vec_1_local.x = dot_vec(vec_1, face.e1); vec_1_local.y = dot_vec(vec_1, face.e2); vec_1_local.z = 0.0;
    vec_2_local.x = dot_vec(vec_2, face.e1); vec_2_local.y = dot_vec(vec_2, face.e2); vec_2_local.z = 0.0;
    vec_3_local.x = dot_vec(vec_3, face.e1); vec_3_local.y = dot_vec(vec_3, face.e2); vec_3_local.z = 0.0;

    vec_0_local.x = (1.0 / 3.0) * (vec_1_local.x + vec_2_local.x + vec_3_local.x); vec_0_local.y = (1.0 / 3.0) * (vec_1_local.y + vec_2_local.y + vec_3_local.y); vec_0_local.z = (1.0 / 3.0) * (vec_1_local.z + vec_2_local.z + vec_3_local.z);

    face.p1.x = vec_1_local.x - vec_0_local.x; face.p1.y = vec_1_local.y - vec_0_local.y; face.p1.z = vec_1_local.z - vec_0_local.z;
    face.p2.x = vec_2_local.x - vec_0_local.x; face.p2.y = vec_2_local.y - vec_0_local.y; face.p2.z = vec_2_local.z - vec_0_local.z;
    face.p3.x = vec_3_local.x - vec_0_local.x; face.p3.y = vec_3_local.y - vec_0_local.y; face.p3.z = vec_3_local.z - vec_0_local.z;

    /* Area */
    face.area = tri_face_area(face.p1, face.p2, face.p3);

    /* Max. distance */
    face.max_distance = 10 * 2 * sqrt(face.area / M_PI);
    
    // if (index == 0)
    // {
    //     print_face(face);
    //     printf("vert1 = [%.3e, %.3e, %.3e]\n", v1.x, v1.y, v1.z);
    //     printf("vert2 = [%.3e, %.3e, %.3e]\n", v2.x, v2.y, v2.z);
    //     printf("vert3 = [%.3e, %.3e, %.3e]\n", v3.x, v3.y, v3.z);
    //     exit(0);
    // }

    return face;

}

void init_mesh(int n_v,
               int n_f3,
               int n_f4,
               int n_te,
               int n_w,
               double *vertices,
               int *faces3,
               int *faces4,
               int *trailing_edge,
               Mesh *mesh)
{

    int i, j;

    mesh->n_v = n_v;
    mesh->n_f = n_f3 + n_f4;
    mesh->n_te = n_te;
    mesh->n_w = n_w;

    mesh->vertices = (Vec3D*)malloc(mesh->n_v * sizeof(Vec3D));
    mesh->faces = (Face*)malloc(mesh->n_f * sizeof(Face));
    mesh->vertices_connection = (VerticesConnection*)malloc(mesh->n_v * sizeof(VerticesConnection));
    mesh->trailing_edge = (TrailingEdge*)malloc(mesh->n_te * sizeof(TrailingEdge));

    // Cria os vértices
    for (i = 0; i < n_v; i++)
    {
        mesh->vertices[i].x = vertices[3 * i];
        mesh->vertices[i].y = vertices[3 * i + 1];
        mesh->vertices[i].z = vertices[3 * i + 2];
    }

    // Cria as faces
    for (i = 0; i < n_f4; i++)
    {
        mesh->faces[i] = create_quad_face(
            mesh->vertices[faces4[4 * i]],
            mesh->vertices[faces4[4 * i + 1]],
            mesh->vertices[faces4[4 * i + 2]],
            mesh->vertices[faces4[4 * i + 3]],
            faces4[4 * i],
            faces4[4 * i + 1],
            faces4[4 * i + 2],
            faces4[4 * i + 3],
            i
        );
    }

    for (i = 0; i < n_f3; i++)
    {
        mesh->faces[n_f4 + i] = create_tri_face(
            mesh->vertices[faces3[3 * i]],
            mesh->vertices[faces3[3 * i + 1]],
            mesh->vertices[faces3[3 * i + 2]],
            faces3[3 * i],
            faces3[3 * i + 1],
            faces3[3 * i + 2],
            i);
    }

    // Cria a coneção entre os vértices
    int count;
    int *faces = (int*)malloc(300 * sizeof(int));

    for (i = 0; i < mesh->n_v; i++)
    {
        
        count = 0;

        for (j = 0; j < mesh->n_f; j++)
        {
            if (mesh->faces[j].n_sides == 4) {
                if ((i == mesh->faces[j].v1) || (i == mesh->faces[j].v2) || (i == mesh->faces[j].v3) || (i == mesh->faces[j].v4))
                {
                    faces[count] = j;
                    count++;
                }
            } else {
                if ((i == mesh->faces[j].v1) || (i == mesh->faces[j].v2) || (i == mesh->faces[j].v3))
                {
                    faces[count] = j;
                    count++;
                }
            }
            
        }

        mesh->vertices_connection[i].n = count;
        mesh->vertices_connection[i].faces = (int*)malloc(count * sizeof(int));

        for (j = 0; j < count; j++)
        {
            mesh->vertices_connection[i].faces[j] = faces[j];
        }

    }

    free(faces);

    // Cria a estrutura do bordo de fuga
    for (i = 0; i < mesh->n_te; i++)
    {

        // Vértices
        mesh->trailing_edge[i].v1 = trailing_edge[2 * i];
        mesh->trailing_edge[i].v2 = trailing_edge[2 * i + 1];

        // Filamentos da esteira
        mesh->trailing_edge[i].filament1 = (Vec3D*)malloc(mesh->n_w * sizeof(Vec3D));
        mesh->trailing_edge[i].filament2 = (Vec3D*)malloc(mesh->n_w * sizeof(Vec3D));

        mesh->trailing_edge[i].filament1[0].x = mesh->vertices[mesh->trailing_edge[i].v1].x;
        mesh->trailing_edge[i].filament1[0].y = mesh->vertices[mesh->trailing_edge[i].v1].y;
        mesh->trailing_edge[i].filament1[0].z = mesh->vertices[mesh->trailing_edge[i].v1].z;

        mesh->trailing_edge[i].filament2[0].x = mesh->vertices[mesh->trailing_edge[i].v2].x;
        mesh->trailing_edge[i].filament2[0].y = mesh->vertices[mesh->trailing_edge[i].v2].y;
        mesh->trailing_edge[i].filament2[0].z = mesh->vertices[mesh->trailing_edge[i].v2].z;
        
        // Faces
        mesh->trailing_edge[i].f1 = - 1;
        mesh->trailing_edge[i].f2 = - 1;

        for (j = 0; j < mesh->n_f; j++)
        {
            
            if (mesh->faces[j].n_sides == 4) {
                
                if ( ( (mesh->trailing_edge[i].v1 == mesh->faces[j].v1) || (mesh->trailing_edge[i].v1 == mesh->faces[j].v2) || (mesh->trailing_edge[i].v1 == mesh->faces[j].v3) || (mesh->trailing_edge[i].v1 == mesh->faces[j].v4) ) && ( (mesh->trailing_edge[i].v2 == mesh->faces[j].v1) || (mesh->trailing_edge[i].v2 == mesh->faces[j].v2) || (mesh->trailing_edge[i].v2 == mesh->faces[j].v3) || (mesh->trailing_edge[i].v2 == mesh->faces[j].v4) ) )
                {

                    if (mesh->trailing_edge[i].f1 == -1) {
                        mesh->trailing_edge[i].f1 = j;
                    } else {
                        mesh->trailing_edge[i].f2 = j;
                        break;
                    }

                }

            } else {

                if ( ( (mesh->trailing_edge[i].v1 == mesh->faces[j].v1) || (mesh->trailing_edge[i].v1 == mesh->faces[j].v2) || (mesh->trailing_edge[i].v1 == mesh->faces[j].v3) ) && ( (mesh->trailing_edge[i].v2 == mesh->faces[j].v1) || (mesh->trailing_edge[i].v2 == mesh->faces[j].v2) || (mesh->trailing_edge[i].v2 == mesh->faces[j].v3) ) )
                {

                    if (mesh->trailing_edge[i].f1 == -1) {
                        mesh->trailing_edge[i].f1 = j;
                    } else {
                        mesh->trailing_edge[i].f2 = j;
                        break;
                    }

                }

            }

        }

    }
}