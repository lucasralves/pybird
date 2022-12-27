import sys
from typing import List, NamedTuple
import numpy as np
import ctypes
import gmsh
import vtk

class FaceModel(NamedTuple):
    n: int
    vertices: List[int]

"""
    Corrige a lista de vértices da malha, retirando os ids dos pontos que foram
    utilizados somente para construção da geometria.

    Entradas:
    --------
    - vertices: lista com os vértices (x, y, z)
    - faces3: ids dos pontos das faces triangulares
    - faces4: ids dos pontos das faces quadrangulares
    - trailing_edge: lista com os ids dos pontos das curvas do bordo de fuga

    Saída:
    -----
    - vertices_out
    - faces3_out
    - faces4_out
    - trailing_edge_out
"""
def correct_vertices_ids(vertices: np.ndarray,
                         faces3: np.ndarray,
                         faces4: np.ndarray,
                         trailing_edge: List[np.ndarray]):
    
    # Cria os pares dos vértices no bordo de fuga
    te_ids = []

    for points in trailing_edge:
        for j in range(points.size - 1):
            te_ids.append([points[j], points[j + 1]])
    
    te_ids = np.asarray(te_ids)

    # Encontra os vértices corretos
    vertices_ids = []

    for id in range(vertices.shape[0]):
        if id in faces3 or id in faces4:
            vertices_ids.append(id)
    
    # Corrige os vértices das faces
    faces3_out = np.zeros_like(faces3, dtype=np.int32)
    faces4_out = np.zeros_like(faces4, dtype=np.int32)

    vertices_out = np.empty((len(vertices_ids), 3), dtype=np.double)

    for i in range(len(vertices_ids)):
        faces3_out[vertices_ids[i] == faces3, :] = i
        faces4_out[vertices_ids[i] == faces4, :] = i
        vertices_out[i, :] = vertices[vertices_ids[i], :]
    
    faces_out = []

    for face in faces4_out:
        faces_out.append(FaceModel(4, [face[0], face[1], face[2], face[3]]))
        
    for face in faces3_out:
        faces_out.append(FaceModel(3, [face[0], face[1], face[2]]))
    
    # Corrige os vértices do bordo de fuga
    for i in range(len(vertices_ids)):
        new_data[vertices_ids[i] == data] = i

    return

def create_mesh(foilname: str,
                span: float = 5,
                n_span: int = 20,
                n_chord_1: int = 20,
                n_chord_2: int = 5,
                n_chord_3: int = 12,
                coef_le: float = 3.0,
                coef_te: float = 1.1):
    
    def __vertices_pairs(a: List[int]) -> List[List[int]]:
        
        l = []
        for i in range(len(a) - 1):
            l.append([a[i], a[i + 1]])
        
        return l

    foil = np.loadtxt(foilname)

    n_1 = int(foil.shape[0] / 5)
    n_2 = int(n_1 * 1.5)
    n_3 = foil.shape[0] - n_2 - 1
    n_4 = foil.shape[0] - n_1 - 1

    point_1 = foil[0, :]
    point_2 = foil[n_1, :]
    point_3 = foil[n_2, :]
    point_4 = foil[n_3, :]
    point_5 = foil[n_4, :]

    curve_1 = foil[1:n_1, :]
    curve_2 = foil[n_1 + 1:n_2, :]
    curve_3 = foil[n_2 + 1:n_3, :]
    curve_4 = foil[n_3 + 1:n_4, :]
    curve_5 = foil[n_4 + 1:-1, :]

    gmsh.initialize()
    gmsh.option.setNumber('General.Verbosity', 1)

    p1_e = gmsh.model.geo.add_point(point_1[0], point_1[1], - span / 2)
    p2_e = gmsh.model.geo.add_point(point_2[0], point_2[1], - span / 2)
    p3_e = gmsh.model.geo.add_point(point_3[0], point_3[1], - span / 2)
    p4_e = gmsh.model.geo.add_point(point_4[0], point_4[1], - span / 2)
    p5_e = gmsh.model.geo.add_point(point_5[0], point_5[1], - span / 2)

    p1_d = gmsh.model.geo.add_point(point_1[0], point_1[1], span / 2)
    p2_d = gmsh.model.geo.add_point(point_2[0], point_2[1], span / 2)
    p3_d = gmsh.model.geo.add_point(point_3[0], point_3[1], span / 2)
    p4_d = gmsh.model.geo.add_point(point_4[0], point_4[1], span / 2)
    p5_d = gmsh.model.geo.add_point(point_5[0], point_5[1], span / 2)

    l1 = gmsh.model.geo.add_line(p1_e, p1_d)
    l2 = gmsh.model.geo.add_line(p2_e, p2_d)
    l3 = gmsh.model.geo.add_line(p3_e, p3_d)
    l4 = gmsh.model.geo.add_line(p4_e, p4_d)
    l5 = gmsh.model.geo.add_line(p5_e, p5_d)

    c1_e = gmsh.model.geo.add_polyline([p1_e] + [gmsh.model.geo.add_point(p[0], p[1], - span / 2) for p in curve_1] + [p2_e])
    c2_e = gmsh.model.geo.add_polyline([p2_e] + [gmsh.model.geo.add_point(p[0], p[1], - span / 2) for p in curve_2] + [p3_e])
    c3_e = gmsh.model.geo.add_polyline([p3_e] + [gmsh.model.geo.add_point(p[0], p[1], - span / 2) for p in curve_3] + [p4_e])
    c4_e = gmsh.model.geo.add_polyline([p4_e] + [gmsh.model.geo.add_point(p[0], p[1], - span / 2) for p in curve_4] + [p5_e])
    c5_e = gmsh.model.geo.add_polyline([p5_e] + [gmsh.model.geo.add_point(p[0], p[1], - span / 2) for p in curve_5] + [p1_e])

    c1_d = gmsh.model.geo.add_polyline([p1_d] + [gmsh.model.geo.add_point(p[0], p[1], span / 2) for p in curve_1] + [p2_d])
    c2_d = gmsh.model.geo.add_polyline([p2_d] + [gmsh.model.geo.add_point(p[0], p[1], span / 2) for p in curve_2] + [p3_d])
    c3_d = gmsh.model.geo.add_polyline([p3_d] + [gmsh.model.geo.add_point(p[0], p[1], span / 2) for p in curve_3] + [p4_d])
    c4_d = gmsh.model.geo.add_polyline([p4_d] + [gmsh.model.geo.add_point(p[0], p[1], span / 2) for p in curve_4] + [p5_d])
    c5_d = gmsh.model.geo.add_polyline([p5_d] + [gmsh.model.geo.add_point(p[0], p[1], span / 2) for p in curve_5] + [p1_d])

    cl1 = gmsh.model.geo.addCurveLoop([-l1, c1_e, l2, -c1_d])
    cl2 = gmsh.model.geo.addCurveLoop([-l2, c2_e, l3, -c2_d])
    cl3 = gmsh.model.geo.addCurveLoop([-l3, c3_e, l4, -c3_d])
    cl4 = gmsh.model.geo.addCurveLoop([-l4, c4_e, l5, -c4_d])
    cl5 = gmsh.model.geo.addCurveLoop([-l5, c5_e, l1, -c5_d])

    s1 = gmsh.model.geo.add_surface_filling([cl1])
    s2 = gmsh.model.geo.add_surface_filling([cl2])
    s3 = gmsh.model.geo.add_surface_filling([cl3])
    s4 = gmsh.model.geo.add_surface_filling([cl4])
    s5 = gmsh.model.geo.add_surface_filling([cl5])

    gmsh.model.geo.synchronize()

    gmsh.model.mesh.set_transfinite_curve(l1, n_span)
    gmsh.model.mesh.set_transfinite_curve(l2, n_span)
    gmsh.model.mesh.set_transfinite_curve(l3, n_span)
    gmsh.model.mesh.set_transfinite_curve(l4, n_span)
    gmsh.model.mesh.set_transfinite_curve(l5, n_span)

    gmsh.model.mesh.set_transfinite_curve(c1_e, n_chord_3, 'Progression', coef_te)
    gmsh.model.mesh.set_transfinite_curve(c5_e, n_chord_3, 'Progression', - coef_te)

    gmsh.model.mesh.set_transfinite_curve(c2_e, n_chord_2)
    gmsh.model.mesh.set_transfinite_curve(c4_e, n_chord_2)

    gmsh.model.mesh.set_transfinite_curve(c3_e, n_chord_1, 'Bump', - coef_le)

    gmsh.model.mesh.set_transfinite_curve(c1_d, n_chord_3, 'Progression', coef_te)
    gmsh.model.mesh.set_transfinite_curve(c5_d, n_chord_3, 'Progression', - coef_te)

    gmsh.model.mesh.set_transfinite_curve(c2_d, n_chord_2)
    gmsh.model.mesh.set_transfinite_curve(c4_d, n_chord_2)

    gmsh.model.mesh.set_transfinite_curve(c3_d, n_chord_1, 'Bump', - coef_le)

    gmsh.model.mesh.set_transfinite_surface(s1)
    gmsh.model.mesh.set_transfinite_surface(s2)
    gmsh.model.mesh.set_transfinite_surface(s3)
    gmsh.model.mesh.set_transfinite_surface(s4)
    gmsh.model.mesh.set_transfinite_surface(s5)

    gmsh.model.mesh.set_recombine(2, s1)
    # gmsh.model.mesh.set_recombine(2, s2)
    gmsh.model.mesh.set_recombine(2, s3)
    gmsh.model.mesh.set_recombine(2, s4)
    gmsh.model.mesh.set_recombine(2, s5)

    gmsh.model.mesh.generate(2)

    # if "-nopopup" not in sys.argv:
    #     gmsh.fltk.initialize()
    #     while gmsh.fltk.isAvailable():
    #         gmsh.fltk.wait()
    
    # Get data
    data = gmsh.model.mesh.get_nodes()
    all_vertices = data[1].reshape((data[0].size, 3))

    gmsh.model.mesh.create_faces()

    data = gmsh.model.mesh.get_all_faces(4)
    faces_4 = data[1].reshape((data[0].size, 4)).astype(np.int32) - 1

    data = gmsh.model.mesh.get_all_faces(3)
    faces_3 = data[1].reshape((data[0].size, 3)).astype(np.int32) - 1

    # Remove unused vertices
    vertices_ids = []

    for id in range(all_vertices.shape[0]):
        if id in faces_3 or id in faces_4:
            vertices_ids.append(id)

    new_faces_3 = np.zeros_like(faces_3, dtype=np.int32)
    new_faces_4 = np.zeros_like(faces_4, dtype=np.int32)

    vertices = np.empty((len(vertices_ids), 3), dtype=np.double)

    for i in range(len(vertices_ids)):
        new_faces_3[vertices_ids[i] == faces_3] = i
        new_faces_4[vertices_ids[i] == faces_4] = i
        vertices[i, :] = all_vertices[vertices_ids[i], :]

    # Create faces obj
    faces = []

    for face in new_faces_4:
        faces.append(FaceModel(4, [face[0], face[1], face[2], face[3]]))
        
    for face in new_faces_3:
        faces.append(FaceModel(3, [face[0], face[1], face[2]]))
    
    # Trailing edge
    trailing_edge = gmsh.model.add_physical_group(1, [l1])
    data = gmsh.model.mesh.get_nodes_for_physical_group(1, trailing_edge)[0] - 1

    new_data = np.zeros_like(data, dtype=np.int32)

    for i in range(len(vertices_ids)):
        new_data[vertices_ids[i] == data] = i
    
    trailing_edge = np.asarray(__vertices_pairs(new_data))

    gmsh.finalize()

    return [vertices, faces, trailing_edge]

def solve(vertices: np.ndarray, faces: List[FaceModel], trailing_edge: np.ndarray, freestream: float, alpha: float, beta: float):

    # Input
    n_v = vertices.shape[0]

    n_te = trailing_edge.shape[0]
    delta_t = 0.1
    n_w = int(1 / (freestream * delta_t))

    n_f4, n_f3 = 0, 0
    faces3, faces4 = [], []

    for face in faces:
        if face.n == 4:
            n_f4 += 1
            faces4.append(face.vertices)
        else:
            n_f3 += 1
            faces3.append(face.vertices)

    faces3 = np.asarray(faces3)
    faces4 = np.asarray(faces4)

    vertices = vertices.reshape(vertices.size)
    faces4 = faces4.reshape(faces4.size)
    faces3 = faces3.reshape(faces3.size)
    trailing_edge = trailing_edge.reshape(trailing_edge.size)
    wake_points = np.empty(6 * n_w * n_te, dtype=np.double)

    # Output
    source = np.empty(n_v, dtype=np.double)
    doublet = np.empty(n_v, dtype=np.double)
    vel_x = np.empty(n_v, dtype=np.double)
    vel_y = np.empty(n_v, dtype=np.double)
    vel_z = np.empty(n_v, dtype=np.double)
    cp = np.empty(n_v, dtype=np.double)
    transpiration = np.empty(n_v, dtype=np.double)

    # Library
    lib = ctypes.CDLL('./bin/libsolver.so')

    lib.main.argtypes = [
        ctypes.c_int,                       # n_v
        ctypes.c_int,                       # n_f3
        ctypes.c_int,                       # n_f4
        ctypes.c_int,                       # n_te
        ctypes.c_int,                       # n_w
        ctypes.c_double,                    # delta_t
        ctypes.POINTER(ctypes.c_double),    # vertices
        ctypes.POINTER(ctypes.c_int),       # faces3
        ctypes.POINTER(ctypes.c_int),       # faces4
        ctypes.POINTER(ctypes.c_int),       # trailing edge
        ctypes.POINTER(ctypes.c_double),    # trailing edge points
        ctypes.c_double,                    # freestream
        ctypes.c_double,                    # alpha
        ctypes.c_double,                    # beta
        ctypes.POINTER(ctypes.c_double),    # source
        ctypes.POINTER(ctypes.c_double),    # doublet
        ctypes.POINTER(ctypes.c_double),    # vel_x
        ctypes.POINTER(ctypes.c_double),    # vel_y
        ctypes.POINTER(ctypes.c_double),    # vel_z
        ctypes.POINTER(ctypes.c_double),    # cp
        ctypes.POINTER(ctypes.c_double),    # transpiration
    ]

    lib.main.restype = None

    lib.main(
        n_v,
        n_f3,
        n_f4,
        n_te,
        n_w,
        delta_t,
        np.ctypeslib.as_ctypes(vertices),
        np.ctypeslib.as_ctypes(faces3),
        np.ctypeslib.as_ctypes(faces4),
        np.ctypeslib.as_ctypes(trailing_edge),
        np.ctypeslib.as_ctypes(wake_points),
        float(freestream),
        float(alpha),
        float(beta),
        np.ctypeslib.as_ctypes(source),
        np.ctypeslib.as_ctypes(doublet),
        np.ctypeslib.as_ctypes(vel_x),
        np.ctypeslib.as_ctypes(vel_y),
        np.ctypeslib.as_ctypes(vel_z),
        np.ctypeslib.as_ctypes(cp),
        np.ctypeslib.as_ctypes(transpiration)
    )

    wake = np.empty((n_te, n_w, 2, 3), dtype=np.double)

    for i in range(n_te):

        index1 = i * 6 * n_w
        index2 = i * 6 * n_w + n_w
        index3 = i * 6 * n_w + 2 * n_w

        wake[i, :, 0, 0] = wake_points[index1:index1 + n_w]
        wake[i, :, 0, 1] = wake_points[index2:index2 + n_w]
        wake[i, :, 0, 2] = wake_points[index3:index3 + n_w]

        index1 = i * 6 * n_w + 3 * n_w
        index2 = i * 6 * n_w + 3 * n_w + n_w
        index3 = i * 6 * n_w + 3 * n_w + 2 * n_w

        wake[i, :, 1, 0] = wake_points[index1:index1 + n_w]
        wake[i, :, 1, 1] = wake_points[index2:index2 + n_w]
        wake[i, :, 1, 2] = wake_points[index3:index3 + n_w]
    
    import matplotlib.pyplot as plt

    ax = plt.figure().add_subplot(projection='3d')

    for i in range(2):
        for j in range(n_w):
            if i == 0:
                color = 'k'
                alpha = 0.5
            elif i == 1:
                color = 'r'
                alpha = 0.5
            else:
                color = 'g'
                alpha = 0.5
            ax.scatter(wake[i, j, 0, 0], wake[i, j, 0, 1], wake[i, j, 0, 2], color=color, alpha=alpha)
            ax.scatter(wake[i, j, 1, 0], wake[i, j, 1, 1], wake[i, j, 1, 2], color=color, alpha=alpha)
    
    plt.show()

    return [
        source,
        doublet,
        vel_x,
        vel_y,
        vel_z,
        cp,
        transpiration,
        wake,
    ]

def create_vtp_file(vertices: np.ndarray,
                    faces: List[FaceModel],
                    trailing_edge: np.ndarray,
                    wake: np.ndarray,
                    source: np.ndarray,
                    doublet: np.ndarray,
                    vel_x: np.ndarray,
                    vel_y: np.ndarray,
                    vel_z: np.ndarray,
                    cp: np.ndarray,
                    transpiration: np.ndarray):

    pd = vtk.vtkPolyData()

    points = vtk.vtkPoints()
    cells = vtk.vtkCellArray()

    # Surface
    for vertice in vertices:
        points.InsertNextPoint(vertice[0], vertice[1], vertice[2])
    
    for face in faces:
        if face.n == 3:
            cell = vtk.vtkTriangle()
            cell.GetPointIds().SetId(0, face.vertices[0])
            cell.GetPointIds().SetId(1, face.vertices[1])
            cell.GetPointIds().SetId(2, face.vertices[2])
        else:
            cell = vtk.vtkQuad()
            cell.GetPointIds().SetId(0, face.vertices[0])
            cell.GetPointIds().SetId(1, face.vertices[1])
            cell.GetPointIds().SetId(2, face.vertices[2])
            cell.GetPointIds().SetId(3, face.vertices[3])
        
        cells.InsertNextCell(cell)
    
    pd.SetPoints(points)
    pd.SetPolys(cells)
    
    # Wake
    for i in range(len(wake[:, 0, 0, 0])):
        for j in range(len(wake[0, :, 0, 0])):
            points.InsertNextPoint(wake[i, j, 0, 0], wake[i, j, 0, 1], wake[i, j, 0, 2])
    
    for i in range(len(wake[:, 0, 0, 0])):
        for j in range(len(wake[0, :, 0, 0])):
            points.InsertNextPoint(wake[i, j, 1, 0], wake[i, j, 1, 1], wake[i, j, 1, 2])
    
    n_v = vertices.shape[0]

    lines = vtk.vtkCellArray()

    # (n_te, n_w, 2, 3)
    for i in range(2 * len(wake[:, 0, 0, 0])):
        polyLine = vtk.vtkPolyLine()
        polyLine.GetPointIds().SetNumberOfIds(len(wake[0, :, 0, 0]))
        for j in range(len(wake[0, :, 0, 0])):
            polyLine.GetPointIds().SetId(j, n_v + j)
        lines.InsertNextCell(polyLine)

    pd.SetLines(lines)
    
    if trailing_edge is not None:
    
        trailing_edge_data = vtk.vtkFloatArray(); trailing_edge_data.SetName('trailing-edge')
        source_data = vtk.vtkFloatArray(); source_data.SetName('source')
        doublet_data = vtk.vtkFloatArray(); doublet_data.SetName('doublet')
        vel_data = vtk.vtkFloatArray(); vel_data.SetNumberOfComponents(3); vel_data.SetName('velocity')
        cp_data = vtk.vtkFloatArray(); cp_data.SetName('cp')
        transpiration_data = vtk.vtkFloatArray(); transpiration_data.SetName('transpiration')

        for i in range(vertices.shape[0]):
            
            if i in trailing_edge[:, 0] or i in trailing_edge[:, 1]:
                trailing_edge_data.InsertNextTuple1(1.0)
            else:
                trailing_edge_data.InsertNextTuple1(0.0)
            
            source_data.InsertNextTuple1(source[i])
            doublet_data.InsertNextTuple1(doublet[i])
            cp_data.InsertNextTuple1(cp[i])
            vel_data.InsertNextTuple3(vel_x[i], vel_y[i], vel_z[i])
            transpiration_data.InsertNextTuple1(transpiration[i])
        
        for i in range(int(wake.size / 3)):
            trailing_edge_data.InsertNextTuple1(0.5)
            source_data.InsertNextTuple1(np.mean(source))
            doublet_data.InsertNextTuple1(np.mean(doublet))
            cp_data.InsertNextTuple1(np.mean(cp))
            vel_data.InsertNextTuple3(np.mean(vel_x), np.mean(vel_y), np.mean(vel_z))
            transpiration_data.InsertNextTuple1(np.mean(transpiration))

    if trailing_edge is not None:
        pd.GetPointData().AddArray(trailing_edge_data)
        pd.GetPointData().AddArray(source_data)
        pd.GetPointData().AddArray(doublet_data)
        pd.GetPointData().AddArray(cp_data)
        pd.GetPointData().AddArray(vel_data)
        pd.GetPointData().AddArray(transpiration_data)

    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName('{}.vtp'.format('case'))
    writer.SetInputData(pd)
    writer.Write()

    return

if __name__ == '__main__':

    vertices, faces, trailing_edge = create_mesh(
        foilname='./data/NACA0009.dat',
        n_span=5,
        n_chord_1=10,
        n_chord_2=3,
        n_chord_3=4,
        coef_le=10.0,
    )

    freestream = 1
    alpha = 0.0
    beta = 0.0

    source, doublet, vel_x, vel_y, vel_z, cp, transpiration, wake = solve(vertices, faces, trailing_edge, freestream, alpha, beta)
    # source, doublet, vel_x, vel_y, vel_z, cp, transpiration = [None, None, None, None, None, None, None]

    create_vtp_file(vertices, faces, trailing_edge, wake, source, doublet, vel_x, vel_y, vel_z, cp, transpiration)