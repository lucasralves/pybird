from pybird.geometry.utilities.data import Data
from pybird.geometry.utilities.head_final_params import HeadFinalParams

from pybird.geometry.utilities.wing_final_params import WingFinalParams
from pybird.geometry.utilities.body_final_params import BodyFinalParams
from pybird.geometry.utilities.tail_final_params import TailFinalParams


class Geometry:
    
    def __init__(self) -> None:
        self.data = Data()
        self.wing_params = WingFinalParams(self.data)
        self.body_params = BodyFinalParams(self.data, self.wing_params)
        self.tail_params = TailFinalParams(self.data, self.body_params)
        self.head_params = HeadFinalParams(self.data, self.body_params)
        