import vtk
import numpy as np
from typing import List

from py.models import FaceModel

def create_surface(vertices: np.ndarray,
                   faces: List[FaceModel],
                   pd: vtk.vtkPolyData,
                   points: vtk.vtkPoints):

    cells = vtk.vtkCellArray()

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
    
    pd.SetPolys(cells)

    return

def create_wake(wake: np.ndarray,
                n_v: int,
                pd: vtk.vtkPolyData,
                points: vtk.vtkPoints):

    # (n_te, n_w, 2, 3)
    n_te = wake.shape[0]
    n_w = wake.shape[1]

    for i in range(n_te):

        for j in range(n_w):
            points.InsertNextPoint(wake[i, j, 0, 0], wake[i, j, 0, 1], wake[i, j, 0, 2])
        
        for j in range(n_w):
            points.InsertNextPoint(wake[i, j, 1, 0], wake[i, j, 1, 1], wake[i, j, 1, 2])
    
    lines = vtk.vtkCellArray()

    for i in range(2 * n_te):

        polyLine = vtk.vtkPolyLine()
        polyLine.GetPointIds().SetNumberOfIds(n_w)

        for j in range(n_w):
            polyLine.GetPointIds().SetId(j, n_v + i * n_w + j)

        lines.InsertNextCell(polyLine)

    pd.SetLines(lines)

    return

def add_scalar_param(name: str,
                     vals: np.ndarray,
                     wake_size: int,
                     pd: vtk.vtkPolyData):

    param = vtk.vtkFloatArray()
    param.SetName(name)

    for i in range(vals.shape[0]):
        param.InsertNextTuple1(vals[i])
    
    for i in range(wake_size):
        param.InsertNextTuple1(np.mean(vals))
    
    pd.GetPointData().AddArray(param)

    return

def add_vector_param(name: str,
                     vals_x: np.ndarray,
                     vals_y: np.ndarray,
                     vals_z: np.ndarray,
                     wake_size: int,
                     pd: vtk.vtkPolyData):

    param = vtk.vtkFloatArray()
    param.SetNumberOfComponents(3)
    param.SetName(name)

    for i in range(vals_x.shape[0]):
        param.InsertNextTuple3(vals_x[i], vals_y[i], vals_z[i])
    
    for i in range(wake_size):
        param.InsertNextTuple3(np.mean(vals_x), np.mean(vals_y), np.mean(vals_z))
    
    pd.GetPointData().AddArray(param)

    return

def create_vtp_file(vertices: np.ndarray,
                    faces: List[FaceModel],
                    sol: List[np.ndarray]):

    pd = vtk.vtkPolyData()
    points = vtk.vtkPoints()
    pd.SetPoints(points)

    create_surface(vertices, faces, pd, points)
    create_wake(sol[7], vertices.shape[0], pd, points)
    add_scalar_param('source', sol[0], sol[7].size, pd)
    add_scalar_param('doublet', sol[1], sol[7].size, pd)
    add_scalar_param('cp', sol[5], sol[7].size, pd)
    add_scalar_param('transpiration', sol[6], sol[7].size, pd)
    add_vector_param('velocity', sol[2], sol[3], sol[4], sol[7].size, pd)

    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName('{}.vtp'.format('case'))
    writer.SetInputData(pd)
    writer.Write()

    return
