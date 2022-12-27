from typing import List
import numpy as np

from py.models import FaceModel

def correct_vertices_ids(vertices: np.ndarray, faces3: np.ndarray, faces4: np.ndarray, trailing_edge_list: List[np.ndarray]):
    
    # Saída
    vertices_out = []
    faces_out = []
    trailing_edge_out = []

    # Encontre os ids dos vértices utilizados na malha
    vertices_ids = []

    for id in range(vertices.shape[0]):

        is_in_f3 = id in faces3[:, 0] or id in faces3[:, 1] or id in faces3[:, 2]
        is_in_f4 = id in faces4[:, 0] or id in faces4[:, 1] or id in faces4[:, 2] or id in faces4[:, 3]

        if is_in_f3 or is_in_f4:
            vertices_ids.append(id)
    
    vertices_ids = np.asarray(vertices_ids)

    # Corrige os valores dos vértices
    for id in vertices_ids:
        vertices_out.append(vertices[id, :])

    # Corrige os valores das faces
    for face in faces3:
        id1 = int(np.argwhere(face[0] == vertices_ids)[0])
        id2 = int(np.argwhere(face[1] == vertices_ids)[0])
        id3 = int(np.argwhere(face[2] == vertices_ids)[0])
        faces_out.append(FaceModel(3, [id1, id2, id3]))
    
    for face in faces4:
        id1 = int(np.argwhere(face[0] == vertices_ids)[0])
        id2 = int(np.argwhere(face[1] == vertices_ids)[0])
        id3 = int(np.argwhere(face[2] == vertices_ids)[0])
        id4 = int(np.argwhere(face[3] == vertices_ids)[0])
        faces_out.append(FaceModel(4, [id1, id2, id3, id4]))
    
    # Corrige os valores do bordo de fuga
    for points in trailing_edge_list:

        new_points = []

        for i in range(len(points)):
            if i != 1:
                new_points.append(points[i])
        
        for i in range(len(new_points) - 1):
            id1 = int(np.argwhere(new_points[i] == vertices_ids)[0])
            id2 = int(np.argwhere(new_points[i + 1] == vertices_ids)[0])
            trailing_edge_out.append([id1, id2])

        id1 = int(np.argwhere(points[-1] == vertices_ids)[0])
        id2 = int(np.argwhere(points[1] == vertices_ids)[0])
        trailing_edge_out.append([id1, id2])
    
    # Converte para numpy array
    vertices_out = np.asarray(vertices_out)
    trailing_edge_out = np.asarray(trailing_edge_out)

    return [vertices_out, faces_out, trailing_edge_out]
