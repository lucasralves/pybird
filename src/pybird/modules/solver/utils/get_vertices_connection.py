from typing import List
from numpy import argwhere, dot
from numpy.linalg import norm
from math import acos

from pybird.modules.mesh.mesh import Mesh
from pybird.modules.solver.models.vertices_connection_model import VerticesConnectionModel

def get_vertices_connection(mesh: Mesh) -> List[VerticesConnectionModel]:

    vertices_connection = []

    for v_id in range(mesh.nv):

        # Encontra as faces que se conectam com o v_id
        face_ids = [i[0] for i in argwhere((mesh.faces[:, 1] == v_id) | (mesh.faces[:, 2] == v_id) | (mesh.faces[:, 3] == v_id) | (mesh.faces[:, 4] == v_id))]

        # Encontra os ângulos
        angles = []

        for face_id in face_ids:
            
            if v_id == mesh.faces[face_id, 1]:
                
                v1 = mesh.vertices[mesh.faces[face_id, 2], :] - mesh.vertices[mesh.faces[face_id, 1], :]
                
                if mesh.faces[face_id, 0] == 3:
                    v2 = mesh.vertices[mesh.faces[face_id, 3], :] - mesh.vertices[mesh.faces[face_id, 1], :]
                else:
                    v2 = mesh.vertices[mesh.faces[face_id, 4], :] - mesh.vertices[mesh.faces[face_id, 1], :]

            elif v_id == mesh.faces[face_id, 2]:
                v1 = mesh.vertices[mesh.faces[face_id, 3], :] - mesh.vertices[mesh.faces[face_id, 2], :]
                v2 = mesh.vertices[mesh.faces[face_id, 1], :] - mesh.vertices[mesh.faces[face_id, 2], :]

            elif v_id == mesh.faces[face_id, 3]:

                v2 = mesh.vertices[mesh.faces[face_id, 2], :] - mesh.vertices[mesh.faces[face_id, 3], :]

                if mesh.faces[face_id, 0] == 3:
                    v1 = mesh.vertices[mesh.faces[face_id, 1], :] - mesh.vertices[mesh.faces[face_id, 3], :]
                else:
                    v1 = mesh.vertices[mesh.faces[face_id, 4], :] - mesh.vertices[mesh.faces[face_id, 3], :]

            else:
                v1 = mesh.vertices[mesh.faces[face_id, 1], :] - mesh.vertices[mesh.faces[face_id, 4], :]
                v2 = mesh.vertices[mesh.faces[face_id, 3], :] - mesh.vertices[mesh.faces[face_id, 4], :]
            
            angles.append(acos(dot(v1, v2) / (norm(v1) * norm(v2))))

        sum_angles = sum(angles)

        # Adiciona um modelo
        vertices_connection.append(
            VerticesConnectionModel(
                n=len(face_ids),
                faces=face_ids,
                coefs=[a / sum_angles for a in angles],
            )
        )
        
    return vertices_connection