from dataclasses import dataclass
from json import dump, load
from typing import Any

from pybird.models import geo_model
from pybird.models.convert import from_str, to_class

@dataclass
class CaseModel:
    name: str = ''
    description: str = ''
    geo: geo_model.GeoModel = geo_model.GeoModel()

def from_dict(obj: Any) -> CaseModel:
    assert isinstance(obj, dict)
    name = from_str(obj.get("name"))
    description = from_str(obj.get("description"))
    geo = geo_model.from_dict(obj.get("geo"))
    return CaseModel(name, description, geo)

def to_dict(case: CaseModel) -> dict:
    result: dict = {}
    result["name"] = from_str(case.name)
    result["description"] = from_str(case.description)
    result["geo"] = to_class(geo_model.GeoModel, case.geo, geo_model.to_dict)
    return result

def from_file(file: str) -> CaseModel:
    f = open(file)
    data = load(f)
    f.close()
    return from_dict(data)
    
def to_file(case: CaseModel, file: str) -> None:
    out_file = open(file, "w") 
    dump(to_dict(case), out_file, indent=2)
    out_file.close()
    return
    

