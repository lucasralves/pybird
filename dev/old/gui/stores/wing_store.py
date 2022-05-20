from math import pi
from typing import Callable

from pybird.geometry.geometry import Geometry

class WingStore:
    
    def __init__(self, geo: Geometry) -> None:
        self.geo = geo
        
        self.side = 'Left'
        self.x1 = .0
        self.y1 = .0
        self.z1 = .0
        self.y2 = .0
        self.z2 = .0
        self.x3 = .0
        self.z3 = .0
        self.rootProfile = None
        self.middleProfile = None
        self.tipProfile = None
        return
    
    def floatInputWrapper(self, key: str) -> Callable[[str], None]:
        def wrapper(value: str) -> None:
            self.geo.updateValue(key, float(value))
            return
        return wrapper
    
    def updateRootProfile(self, value: str) -> None:
        self.rootProfile = value
        return
    
    def updateMiddleProfile(self, value: str) -> None:
        self.middleProfile = value
        return
    
    def updateTipProfile(self, value: str) -> None:
        self.tipProfile = value
        return
    
    def updateSide(self, value: str) -> None:
        self.side = value
        return
    
    def updateX1Angle(self, value: str) -> None:
        self.x1 = float(value if value != '' else '0.0')
        return
    
    def updateY1Angle(self, value: str) -> None:
        self.y1 = float(value if value != '' else '0.0')
        return
    
    def updateZ1Angle(self, value: str) -> None:
        self.z1 = float(value if value != '' else '0.0')
        return
    
    def updateY2Angle(self, value: str) -> None:
        self.y2 = float(value if value != '' else '0.0')
        return
    
    def updateZ2Angle(self, value: str) -> None:
        self.z2 = float(value if value != '' else '0.0')
        return
    
    def updateX3Angle(self, value: str) -> None:
        self.x3 = float(value if value != '' else '0.0')
        return
    
    def updateZ3Angle(self, value: str) -> None:
        self.z3 = float(value if value != '' else '0.0')
        return
    
    def updateWingAngles(self) -> None:
        
        side = 'left' if self.side == 'Left' else 'right'

        if -1e-8 > self.x1 or self.x1 > 1e-8: self.geo.addRotation('x1', self.x1, side)
        if -1e-8 > self.y1 or self.y1 > 1e-8: self.geo.addRotation('y1', self.y1, side)
        if -1e-8 > self.z1 or self.z1 > 1e-8: self.geo.addRotation('z1', self.z1, side)

        if -1e-8 > self.y2 or self.y2 > 1e-8: self.geo.addRotation('y2', self.y2, side)
        if -1e-8 > self.z2 or self.z2 > 1e-8: self.geo.addRotation('z2', self.z2, side)

        if -1e-8 > self.x3 or self.x3 > 1e-8: self.geo.addRotation('x3', self.x3, side)
        if -1e-8 > self.z3 or self.z3 > 1e-8: self.geo.addRotation('z3', self.z3, side)
        return
    
    def updateWingFoils(self) -> None:

        return