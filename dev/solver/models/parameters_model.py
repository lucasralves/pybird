from typing import NamedTuple
from numpy import ndarray

class ParametersModel(NamedTuple):
    source_f: ndarray
    doublet_f: ndarray
    vel_f: ndarray
    cp_f: ndarray
    transpiration_f: ndarray
    source_v: ndarray
    doublet_v: ndarray
    vel_v: ndarray
    cp_v: ndarray
    transpiration_v: ndarray