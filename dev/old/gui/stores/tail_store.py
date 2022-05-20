from math import pi
from typing import Callable

from pybird.geometry.geometry import Geometry

class TailStore:
    
    def __init__(self, geo: Geometry) -> None:
        self.geo = geo
        
        self.x4 = .0
        self.y4 = .0
        self.z4 = .0
        return
    
    def floatInputWrapper(self, key: str) -> Callable[[str], None]:
        def wrapper(value: str) -> None:
            self.geo.updateValue(key, float(value))
            return
        return wrapper
    
    def stringInputWrapper(self, key: str) -> Callable[[str], None]:
        def wrapper(value: str) -> None:
            self.geo.updateValue(key, value)
            return
        return wrapper
    
    def updateX4Angle(self, value: str) -> None:
        self.x4 = float(value)
        return
    
    def updateY4Angle(self, value: str) -> None:
        self.y4 = float(value)
        return
    
    def updateZ4Angle(self, value: str) -> None:
        self.z4 = float(value)
        return
    
    def updateTail(self) -> None:
        if -1e-16 > self.x4 or self.x4 > 1e-16: self.geo.addRotation('x4', self.x4)
        if -1e-16 > self.y4 or self.y4 > 1e-16: self.geo.addRotation('y4', self.y4)
        if -1e-16 > self.z4 or self.z4 > 1e-16: self.geo.addRotation('z4', self.z4)
        return