from typing import List
from numpy import ndarray, empty, double

from pybird.modules.solver.models.vertices_connection_model import VerticesConnectionModel

def get_scalar_vertices_values(nv: int, vertices_connection: VerticesConnectionModel, face_values: ndarray) -> ndarray:

    vertice_values = empty(nv, dtype=double)

    for i in range(nv):

        vertice_values[i] = .0

        for j in range(vertices_connection[i].n):
            vertice_values[i] = vertice_values[i] + face_values[vertices_connection[i].faces[j]] * vertices_connection[i].coefs[j]

    return vertice_values

def get_vector_vertices_values(nv: int, vertices_connection: List[VerticesConnectionModel], face_values: ndarray) -> ndarray:

    vertice_values = empty((nv, 3), dtype=double)

    for i in range(nv):

        vertice_values[i, :] = .0

        for j in range(vertices_connection[i].n):
            vertice_values[i, :] = vertice_values[i, :] + face_values[vertices_connection[i].faces[j], :] * vertices_connection[i].coefs[j]

    return vertice_values