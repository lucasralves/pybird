from typing import List, NamedTuple

class WingSectionsRefinementModel(NamedTuple):
    nodes: int
    ref_type: str = 'Progression'
    coef: float = 1.0

class WingRefinementModel(NamedTuple):
    sections: List[WingSectionsRefinementModel] = [ WingSectionsRefinementModel(10), WingSectionsRefinementModel(10), WingSectionsRefinementModel(3), WingSectionsRefinementModel(10), WingSectionsRefinementModel(10), WingSectionsRefinementModel(5)]
    n_chord_le: int = 10
    n_chord_te: int = 10
    coef_te: float = 1.0
    coef_le: float = 1.0

class BodyRefinementModel(NamedTuple):
    n_cross_body: int = 10
    coef_cross_body: float = 1.1
    n_head: int = 12
    coef_head: float = 1.1
    n_tail: int = 12
    coef_tail: float = 1.1

class HeadRefinementModel(NamedTuple):
    n_1: int = 10
    coef_1: float = 1.1
    n_2: int = 10
    coef_2: float = 1.1

class TailRefinementModel(NamedTuple):
    n_edge: int = 20
    coef_edge_le: float = 1.1
    coef_edge_te: float = 1.1
    coef_tip: float = 1.1
    n_1: int = 10
    n_2: int = 12

class RefinementModel:
    
    def __init__(self, wing: WingRefinementModel,
                       body: BodyRefinementModel,
                       head: HeadRefinementModel,
                       tail: TailRefinementModel) -> None:
        
        assert len(wing.sections) == 6
        for i in wing.sections: assert i.ref_type in ['Progression', 'Bump', 'Beta']

        self.wing = wing
        self.body = body
        self.head = head
        self.tail = tail
        
        return