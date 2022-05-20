from pybird.gui.stores.store import Store

from pybird.gui.components.body_input_component import BodyInputComponent
from pybird.gui.components.head_input_component import HeadInputComponent
from pybird.gui.components.tail_input_component import TailInputComponent
from pybird.gui.components.wing_input_component import WingInputComponent

from pybird.gui.widgets.tab_widget import TabItem, TabWidget

class InputsComponents(TabWidget):
    
    def __init__(self, store: Store) -> None:

        self.store = store

        tabs = [
            TabItem(
                name='Body',
                item=BodyInputComponent(store=self.store),
            ),
            TabItem(
                name='Wing',
                item=WingInputComponent(store=self.store),
            ),
            TabItem(
                name='Tail',
                item=TailInputComponent(store=self.store),
            ),
            TabItem(
                name='Head',
                item=HeadInputComponent(store=self.store),
            ),
        ]

        super().__init__(tabs, 227)
        return