from typing import List, NamedTuple

class VerticesConnectionModel(NamedTuple):
    n: int
    faces: List[int]
    coefs: List[float]