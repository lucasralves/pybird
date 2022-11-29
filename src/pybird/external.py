from dataclasses import dataclass
from json import dump, load
from typing import Any

from pybird.modules.geo.models.external import *
from pybird.modules.geo.geo import Geometry
from pybird.modules.mesh.mesh import Mesh
from pybird.modules.view.view import View

@dataclass
class CaseModel:
    """Contains the case information"""
    name: str
    description: str
    geo: GeoModel

    @staticmethod
    def from_dict(obj: Any) -> 'CaseModel':
        assert isinstance(obj, dict)
        name = convert.from_str(obj.get("name"))
        description = convert.from_str(obj.get("description"))
        geo = GeoModel.from_dict(obj.get("geo"))
        return CaseModel(name, description, geo)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = convert.from_str(self.name)
        result["description"] = convert.from_str(self.description)
        result["geo"] = convert.to_class(GeoModel, self.geo)
        return result
    
    @staticmethod
    def from_file(file: str) -> 'CaseModel':
        f = open(file)
        data = load(f)
        f.close()
        return CaseModel.from_dict(data)
    
    def to_file(self, file: str) -> None:
        out_file = open(file, "w") 
        dump(self.to_dict(), out_file, indent=2)
        out_file.close()
        return

class __model:
    """External class"""

    def __init__(self, name: str, description: str) -> None:
        geo = GeoModel(WingModel(), BodyModel(), HeadModel(), TailModel())
        self.info = CaseModel(name, description, geo)
        self.geo: Geometry = None
        self.mesh: Mesh = None
        self.view: View = None
        self.verbose: bool = False
        return

    def update_case(self) -> None:
        self.geo = Geometry(self.info.geo, self.verbose)
        self.mesh = Mesh(self.geo, self.verbose)
        self.view = View(self.mesh, self.verbose)
        return

    def save(self, filename: str) -> None:
        self.info.to_file(filename)
        return
    
    def load(self, filename: str) -> None:
        self.info = CaseModel.from_file(filename)
        self.update_case()
        return

def create_model(name: str = None, description: str = None) -> __model:
    return __model(name, description)