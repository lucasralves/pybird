from dataclasses import dataclass
from typing import Any

from pybird.models.convert import to_class
from pybird.models import wing_model
from pybird.models import body_model
from pybird.models import head_model
from pybird.models import tail_model


@dataclass
class GeoModel:
    wing: wing_model.WingModel = wing_model.WingModel()
    body: body_model.BodyModel = body_model.BodyModel()
    head: head_model.HeadModel = head_model.HeadModel()
    tail: tail_model.TailModel = tail_model.TailModel()

def from_dict(obj: Any) -> GeoModel:
    assert isinstance(obj, dict)
    wing = wing_model.from_dict(obj.get("wing"))
    body = body_model.from_dict(obj.get("body"))
    head = head_model.from_dict(obj.get("head"))
    tail = tail_model.from_dict(obj.get("tail"))
    return GeoModel(wing, body, head, tail)

def to_dict(geo: GeoModel) -> dict:
    result: dict = {}
    result["wing"] = to_class(wing_model.WingModel, geo.wing, wing_model.to_dict)
    result["body"] = to_class(body_model.BodyModel, geo.body, body_model.to_dict)
    result["head"] = to_class(head_model.HeadModel, geo.head, head_model.to_dict)
    result["tail"] = to_class(tail_model.TailModel, geo.tail, tail_model.to_dict)
    return result
