from typing import Callable
from pybird.geometry.geometry import Geometry

class BodyStore:

    def __init__(self, geo: Geometry) -> None:
        self.geo = geo
        return
    
    def floatInputWrapper(self, key: str) -> Callable[[str], None]:
        def wrapper(value: str) -> None:
            self.geo.updateValue(key, float(value))
            return
        return wrapper