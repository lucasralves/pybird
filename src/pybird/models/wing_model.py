from dataclasses import dataclass
from typing import Any, List

from pybird.models.convert import from_float, from_list, from_str, to_float

@dataclass
class WingModel:
    l0: float = None
    l1: float = None
    l2: float = None
    l3: float = None
    thetaRootY: int = None
    thetaRootZ: int = None
    theta1_e: int = None
    theta2_e: int = None
    theta3_e: int = None
    theta4_e: int = None
    theta5_e: int = None
    theta6_e: float = None
    theta7_e: float = None
    theta1_d: float = None
    theta2_d: float = None
    theta3_d: float = None
    theta4_d: float = None
    theta5_d: float = None
    theta6_d: float = None
    theta7_d: float = None
    h1: float = None
    h2: float = None
    h3: float = None
    h4: float = None
    h5: float = None
    h6: float = None
    h7: float = None
    delta1: float = None
    delta2: float = None
    delta3: float = None
    delta4: float = None
    delta5: float = None
    delta6: float = None
    delta7: float = None
    delta8: float = None
    delta9: float = None
    delta10: float = None
    foils: List[str] = None

def from_dict(obj: Any) -> WingModel:
    assert isinstance(obj, dict)
    l0 = from_float(obj.get("l0"))
    l1 = from_float(obj.get("l1"))
    l2 = from_float(obj.get("l2"))
    l3 = from_float(obj.get("l3"))
    thetaRootY = from_float(obj.get("thetaRootY"))
    thetaRootZ = from_float(obj.get("thetaRootZ"))
    theta1_e = from_float(obj.get("theta1e"))
    theta2_e = from_float(obj.get("theta2e"))
    theta3_e = from_float(obj.get("theta3e"))
    theta4_e = from_float(obj.get("theta4e"))
    theta5_e = from_float(obj.get("theta5e"))
    theta6_e = from_float(obj.get("theta6e"))
    theta7_e = from_float(obj.get("theta7e"))
    theta1_d = from_float(obj.get("theta1d"))
    theta2_d = from_float(obj.get("theta2d"))
    theta3_d = from_float(obj.get("theta3d"))
    theta4_d = from_float(obj.get("theta4d"))
    theta5_d = from_float(obj.get("theta5d"))
    theta6_d = from_float(obj.get("theta6d"))
    theta7_d = from_float(obj.get("theta7d"))
    h1 = from_float(obj.get("h1"))
    h2 = from_float(obj.get("h2"))
    h3 = from_float(obj.get("h3"))
    h4 = from_float(obj.get("h4"))
    h5 = from_float(obj.get("h5"))
    h6 = from_float(obj.get("h6"))
    h7 = from_float(obj.get("h7"))
    delta1 = from_float(obj.get("delta1"))
    delta2 = from_float(obj.get("delta2"))
    delta3 = from_float(obj.get("delta3"))
    delta4 = from_float(obj.get("delta4"))
    delta5 = from_float(obj.get("delta5"))
    delta6 = from_float(obj.get("delta6"))
    delta7 = from_float(obj.get("delta7"))
    delta8 = from_float(obj.get("delta8"))
    delta9 = from_float(obj.get("delta9"))
    delta10 = from_float(obj.get("delta10"))
    foils = from_list(from_str, obj.get("foils"))
    return WingModel(l0, l1, l2, l3, thetaRootY, thetaRootZ, theta1_e, theta2_e, theta3_e, theta4_e, theta5_e, theta6_e, theta7_e, theta1_d, theta2_d, theta3_d, theta4_d, theta5_d, theta6_d, theta7_d, h1, h2, h3, h4, h5, h6, h7, delta1, delta2, delta3, delta4, delta5, delta6, delta7, delta8, delta9, delta10, foils)

def to_dict(wing: WingModel) -> dict:
    result: dict = {}
    result["l0"] = to_float(wing.l0)
    result["l1"] = to_float(wing.l1)
    result["l2"] = to_float(wing.l2)
    result["l3"] = to_float(wing.l3)
    result["thetaRootY"] = to_float(wing.thetaRootY)
    result["thetaRootZ"] = to_float(wing.thetaRootZ)
    result["theta1e"] = to_float(wing.theta1_e)
    result["theta2e"] = to_float(wing.theta2_e)
    result["theta3e"] = to_float(wing.theta3_e)
    result["theta4e"] = to_float(wing.theta4_e)
    result["theta5e"] = to_float(wing.theta5_e)
    result["theta6e"] = to_float(wing.theta6_e)
    result["theta7e"] = to_float(wing.theta7_e)
    result["theta1d"] = to_float(wing.theta1_d)
    result["theta2d"] = to_float(wing.theta2_d)
    result["theta3d"] = to_float(wing.theta3_d)
    result["theta4d"] = to_float(wing.theta4_d)
    result["theta5d"] = to_float(wing.theta5_d)
    result["theta6d"] = to_float(wing.theta6_d)
    result["theta7d"] = to_float(wing.theta7_d)
    result["h1"] = to_float(wing.h1)
    result["h2"] = to_float(wing.h2)
    result["h3"] = to_float(wing.h3)
    result["h4"] = to_float(wing.h4)
    result["h5"] = to_float(wing.h5)
    result["h6"] = to_float(wing.h6)
    result["h7"] = to_float(wing.h7)
    result["delta1"] = to_float(wing.delta1)
    result["delta2"] = to_float(wing.delta2)
    result["delta3"] = to_float(wing.delta3)
    result["delta4"] = to_float(wing.delta4)
    result["delta5"] = to_float(wing.delta5)
    result["delta6"] = to_float(wing.delta6)
    result["delta7"] = to_float(wing.delta7)
    result["delta8"] = to_float(wing.delta8)
    result["delta9"] = to_float(wing.delta9)
    result["delta10"] = to_float(wing.delta10)
    result["foils"] = from_list(from_str, wing.foils)
    return result