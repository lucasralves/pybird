from abc import ABC
import vtkmodules.all as vtk
from numpy import ndarray

class VIEW_ABS(ABC):

    def __init__(self, vt: ndarray, fc: ndarray) -> None:
        """Stores the mesh"""
        pass
    
    def gen_vtp_file(self, filename: str) -> None:
        """Create a vtk file"""
        pass

class View(VIEW_ABS):

    def __init__(self, vt: ndarray, fc: ndarray) -> None:
        self._vt = vt
        self._fc = fc
        return
    
    def gen_vtp_file(self, filename: str) -> None:

        pd = vtk.vtkPolyData()

        points = vtk.vtkPoints()
        cells = vtk.vtkCellArray()

        # Surface
        for vertice in self._vt:
            points.InsertNextPoint(vertice[0], vertice[1], vertice[2])

        for face in self._fc:
            if face[0] == 3:
                cell = vtk.vtkTriangle()
                cell.GetPointIds().SetId(0, face[1])
                cell.GetPointIds().SetId(1, face[2])
                cell.GetPointIds().SetId(2, face[3])
            else:
                cell = vtk.vtkQuad()
                cell.GetPointIds().SetId(0, face[1])
                cell.GetPointIds().SetId(1, face[2])
                cell.GetPointIds().SetId(2, face[3])
                cell.GetPointIds().SetId(3, face[4])
        
            cells.InsertNextCell(cell)
                    
        pd.SetPoints(points)
        pd.SetPolys(cells)

        writer = vtk.vtkXMLPolyDataWriter()
        writer.SetFileName('{}.vtp'.format(filename))
        writer.SetInputData(pd)
        writer.Write()
        
        return