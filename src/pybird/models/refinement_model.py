from typing import List, NamedTuple

class wing_section(NamedTuple):
    nodes: int
    ref_type: str = 'Progression'
    coef: float = 1.0

class wing(NamedTuple):
    sections: List[wing_section] = [ wing_section(10), wing_section(10), wing_section(3), wing_section(10), wing_section(10), wing_section(5)]
    n_chord_le: int = 10
    n_chord_te: int = 10
    coef_te: float = 1.0
    coef_le: float = 1.0

class body(NamedTuple):
    n_cross_body: int = 10
    coef_cross_body: float = 1.1
    n_head: int = 12
    coef_head: float = 1.1
    n_tail: int = 12
    coef_tail: float = 1.1

class head(NamedTuple):
    n_1: int = 10
    coef_1: float = 1.1
    n_2: int = 10
    coef_2: float = 1.1

class tail(NamedTuple):
    n_edge: int = 20
    coef_edge_le: float = 1.1
    coef_edge_te: float = 1.1
    coef_tip: float = 1.1
    n_1: int = 10
    n_2: int = 12

class model:
    
    def __init__(self, wing: wing,
                       body: body,
                       head: head,
                       tail: tail) -> None:
        
        assert len(wing.sections) == 6
        for i in wing.sections: assert i.ref_type in ['Progression', 'Bump', 'Beta']

        self.wing = wing
        self.body = body
        self.head = head
        self.tail = tail
        
        return