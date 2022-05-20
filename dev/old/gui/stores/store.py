from pybird.geometry.geometry import Geometry
from pybird.gui.stores.body_store import BodyStore

from pybird.gui.stores.save_store import SaveStore
from pybird.gui.stores.tail_store import TailStore
from pybird.gui.stores.update_store import UpdateStore
from pybird.gui.stores.wing_store import WingStore
from pybird.gui.stores.head_store import HeadStore


class Store:

    def __init__(self, geo: Geometry) -> None:
        self.geo = geo
        self.head = HeadStore(geo=self.geo)
        self.body = BodyStore(geo=self.geo)
        self.wing = WingStore(geo=self.geo)
        self.tail = TailStore(geo=self.geo)
        self.update = UpdateStore()
        self.save = SaveStore(geo=self.geo)
        return