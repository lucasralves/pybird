from abc import ABC
import vtk
from numpy import mean

from pybird.modules.mesh.mesh import Mesh
from pybird.modules.helpers import warnings
from pybird.modules.solver.solver import Solver

class VIEW_ABS(ABC):

    def __init__(self, mesh: Mesh, solver: Solver, verbose: bool) -> None:
        """Stores the mesh"""
        pass
    
    def gen_vtp_file(self, filename: str) -> None:
        """Create a vtk file"""
        pass

class View(VIEW_ABS):

    def __init__(self, mesh: Mesh, solver: Solver, verbose: bool) -> None:
        self.__mesh = mesh
        self.__solver = solver
        self.__verbose = verbose
        return
    
    def gen_vtp_file(self, filename: str, show_wake: bool = False) -> None:

        warnings.title('Creating vtp file', self.__verbose)
        
        pd = vtk.vtkPolyData()

        points = vtk.vtkPoints()
        cells = vtk.vtkCellArray()

        for vertice in self.__mesh.vertices:
            points.InsertNextPoint(vertice[0], vertice[1], vertice[2])

        for i in range(self.__mesh.nf):
            if self.__mesh.faces[i, 0] == 3:
                cell = vtk.vtkTriangle()
                cell.GetPointIds().SetId(0, self.__mesh.faces[i, 1])
                cell.GetPointIds().SetId(1, self.__mesh.faces[i, 2])
                cell.GetPointIds().SetId(2, self.__mesh.faces[i, 3])
            else:
                cell = vtk.vtkQuad()
                cell.GetPointIds().SetId(0, self.__mesh.faces[i, 1])
                cell.GetPointIds().SetId(1, self.__mesh.faces[i, 2])
                cell.GetPointIds().SetId(2, self.__mesh.faces[i, 3])
                cell.GetPointIds().SetId(3, self.__mesh.faces[i, 4])
        
            cells.InsertNextCell(cell)
        
        trailing_edge = vtk.vtkFloatArray()
        trailing_edge.SetName('trailing-edge')

        if self.__solver.done:
            source = vtk.vtkFloatArray()
            source.SetName('source')

            doublet = vtk.vtkFloatArray()
            doublet.SetName('doublet')

            velocity = vtk.vtkFloatArray()
            velocity.SetNumberOfComponents(3)
            velocity.SetName('velocity')

            cp = vtk.vtkFloatArray()
            cp.SetName('cp')
            
            transpiration = vtk.vtkFloatArray()
            transpiration.SetName('transpiration')

        for i in range(self.__mesh.nv):
            if i in self.__mesh.trailing_edge[:, 0] or i in self.__mesh.trailing_edge[:, 1]:
                trailing_edge.InsertNextTuple1(1.0)
            else:
                trailing_edge.InsertNextTuple1(0.0)

            if self.__solver.done:
                source.InsertNextTuple1(self.__solver.source_v[i])
                doublet.InsertNextTuple1(self.__solver.doublet_v[i])
                velocity.InsertNextTuple3(self.__solver.vel_v[i, 0], self.__solver.vel_v[i, 1], self.__solver.vel_v[i, 2])
                cp.InsertNextTuple1(self.__solver.cp_v[i])
                transpiration.InsertNextTuple1(self.__solver.transpiration_v[i])
        
        # Wake
        if show_wake and self.__solver.done:

            for i in range(self.__mesh.nv_wake * self.__mesh.nw_wake):
                points.InsertNextPoint(self.__mesh.vertices_wake[i, 0], self.__mesh.vertices_wake[i, 1], self.__mesh.vertices_wake[i, 2])

            for i in range(self.__mesh.nv_wake * self.__mesh.nw_wake):
                source.InsertNextTuple1(mean(self.__solver.source_v))
                doublet.InsertNextTuple1(mean(self.__solver.doublet_v))
                velocity.InsertNextTuple3(mean(self.__solver.vel_v[:, 0]), mean(self.__solver.vel_v[:, 1]), mean(self.__solver.vel_v[:, 2]))
                cp.InsertNextTuple1(mean(self.__solver.cp_v))
                transpiration.InsertNextTuple1(mean(self.__solver.transpiration_v))
                trailing_edge.InsertNextTuple1(0.0)
            
            lines = vtk.vtkCellArray()

            for i in range(self.__mesh.nte_wake):

                polyLine1 = vtk.vtkPolyLine()
                polyLine1.GetPointIds().SetNumberOfIds(self.__mesh.nw_wake)

                polyLine2 = vtk.vtkPolyLine()
                polyLine2.GetPointIds().SetNumberOfIds(self.__mesh.nw_wake)

                for j in range(self.__mesh.nw_wake):
                    polyLine1.GetPointIds().SetId(j, self.__mesh.nv + self.__mesh.wake_ids[i, j, 0])
                    polyLine2.GetPointIds().SetId(j, self.__mesh.nv + self.__mesh.wake_ids[i, j, 1])
                
                lines.InsertNextCell(polyLine1)
                lines.InsertNextCell(polyLine2)
            
            for i in range(self.__mesh.nte_wake):
                for j in range(self.__mesh.nw_wake):
                    polyLine = vtk.vtkPolyLine()
                    polyLine.GetPointIds().SetNumberOfIds(2)
                    polyLine.GetPointIds().SetId(0, self.__mesh.nv + self.__mesh.wake_ids[i, j, 0])
                    polyLine.GetPointIds().SetId(1, self.__mesh.nv + self.__mesh.wake_ids[i, j, 1])
                    lines.InsertNextCell(polyLine)
            
            pd.SetLines(lines)
            
        pd.SetPoints(points)
        pd.SetPolys(cells)
        pd.GetPointData().AddArray(trailing_edge)

        if self.__solver.done:
            pd.GetPointData().AddArray(source)
            pd.GetPointData().AddArray(doublet)
            pd.GetPointData().AddArray(velocity)
            pd.GetPointData().AddArray(cp)
            pd.GetPointData().AddArray(transpiration)
        
            
        writer = vtk.vtkXMLPolyDataWriter()
        writer.SetFileName('{}.vtp'.format(filename))
        writer.SetInputData(pd)
        writer.Write()
        
        return