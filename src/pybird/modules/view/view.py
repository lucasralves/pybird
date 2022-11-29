from abc import ABC
import vtk

from pybird.modules.mesh.mesh import Mesh
from pybird.modules.helpers import warnings

class VIEW_ABS(ABC):

    def __init__(self, mesh: Mesh) -> None:
        """Stores the mesh"""
        pass
    
    def gen_vtp_file(self, filename: str) -> None:
        """Create a vtk file"""
        pass

class View(VIEW_ABS):

    def __init__(self, mesh: Mesh, verbose: bool) -> None:
        self.__mesh = mesh
        self.__verbose = verbose
        return
    
    def gen_vtp_file(self, filename: str) -> None:

        warnings.title('Creating vtk file', self.__verbose)

        pd = vtk.vtkPolyData()

        points = vtk.vtkPoints()
        cells = vtk.vtkCellArray()

        for vertice in self.__mesh.vertices:
            points.InsertNextPoint(vertice[0], vertice[1], vertice[2])

        for face in self.__mesh.faces:
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
        
        trailing_edge = vtk.vtkFloatArray()
        trailing_edge.SetName('trailing-edge')

        for i in range(self.__mesh.vertices.shape[0]):
            if i in self.__mesh.trailing_edge[:, 0] or i in self.__mesh.trailing_edge[:, 1]:
                trailing_edge.InsertNextTuple1(1.0)
            else:
                trailing_edge.InsertNextTuple1(0.0)

        pd.SetPoints(points)
        pd.SetPolys(cells)
        pd.GetPointData().AddArray(trailing_edge)

        writer = vtk.vtkXMLPolyDataWriter()
        writer.SetFileName('{}.vtp'.format(filename))
        writer.SetInputData(pd)
        writer.Write()
        
        return