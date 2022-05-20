from pybird.gui.stores.store import Store

from pybird.gui.widgets.input_widget import InputWidget
from pybird.gui.widgets.scroll_widget import ScrollWidget

class HeadInputComponent(ScrollWidget):

    def __init__(self, store: Store) -> None:

        self.store = store

        children = [
            InputWidget(
                title='l19:  ',
                onChanged=self.store.head.floatInputWrapper('l19'),
                initialValue=self.store.geo.data['l19'],
            ),
            InputWidget(
                title='l20:  ',
                onChanged=self.store.head.floatInputWrapper('l20'),
                initialValue=self.store.geo.data['l20'],
            ),
        ]

        super().__init__(children)
        return