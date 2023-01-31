from pybird.models import case_model as _case_model
from pybird.modules.geo.geo import Geometry as _Geo
from pybird.modules.mesh.mesh import Mesh as _Mesh
from pybird.modules.view.view import View as _View

from pybird.models import refinement_model as refinement
from pybird.models.enums import TailShape

def init() -> None:
    """
    pybird.init()

    Initialize global parameters. This must be called before any call to the other
    functions.
    """
    global model
    model = _case_model.CaseModel()
    return

def load(file: str) -> None:
    """
    pybird.load(file)

    Upload the a file.case with the geometric parameters.

    Parameters:
    -----------
    - file: geometric parameters
    """
    new = _case_model.from_file(file)
    model.name = new.name
    model.description = new.description
    model.geo = new.geo
    return

def save(file: str) -> None:
    """
    pybird.save(file)

    Save a file.case with the geometric parameters.

    Parameters:
    -----------
    - file: output file
    """
    _case_model.to_file(model, file)
    return

def build(ref: refinement.model, view: bool = False) -> None:
    """
    pybird.build(ref, view=True)

    Save a file.case with the geometric parameters.

    Parameters:
    -----------
    - ref: mesh refinament information
    - view: show gmsh mesh
    """
    geo = _Geo(model.geo)
    geo.build()

    mesh = _Mesh(geo)
    mesh.build(ref, view)

    global vt
    vt = mesh.vertices
    vt[:, 0] = - vt[:, 0]
    vt[:, 1] = - vt[:, 1]

    global fc
    fc = mesh.faces

    global te
    te = mesh.trailing_edge

    return

def gen_vtk(file: str) -> None:
    """
    pybird.gen_vtk(file)

    Create a vtp file with the geometric and mesh information.

    Parameters:
    -----------
    - file: output file
    """
    view = _View(vt, fc)
    view.gen_vtp_file(file)
    return
