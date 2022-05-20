from pybird.gui.stores.store import Store

from pybird.gui.widgets.input_widget import InputWidget
from pybird.gui.widgets.scroll_widget import ScrollWidget

class BodyInputComponent(ScrollWidget):

    def __init__(self, store: Store) -> None:

        self.store = store

        children = [
            InputWidget(
                title='l1:  ',
                onChanged=self.store.body.floatInputWrapper('l1'),
                initialValue=self.store.geo.data['l1'],
            ),
            InputWidget(
                title='l2:  ',
                onChanged=self.store.body.floatInputWrapper('l2'),
                initialValue=self.store.geo.data['l2'],
            ),
            InputWidget(
                title='l3:  ',
                onChanged=self.store.body.floatInputWrapper('l3'),
                initialValue=self.store.geo.data['l3'],
            ),
            InputWidget(
                title='l4:  ',
                onChanged=self.store.body.floatInputWrapper('l4'),
                initialValue=self.store.geo.data['l4'],
            ),
            InputWidget(
                title='l5:  ',
                onChanged=self.store.body.floatInputWrapper('l5'),
                initialValue=self.store.geo.data['l5'],
            ),
            InputWidget(
                title='l6:  ',
                onChanged=self.store.body.floatInputWrapper('l6'),
                initialValue=self.store.geo.data['l6'],
            ),
            InputWidget(
                title='l7:  ',
                onChanged=self.store.body.floatInputWrapper('l7'),
                initialValue=self.store.geo.data['l7'],
            ),
            InputWidget(
                title='l8:  ',
                onChanged=self.store.body.floatInputWrapper('l8'),
                initialValue=self.store.geo.data['l8'],
            ),
            InputWidget(
                title='l9:  ',
                onChanged=self.store.body.floatInputWrapper('l9'),
                initialValue=self.store.geo.data['l9'],
            ),
            InputWidget(
                title='l10:',
                onChanged=self.store.body.floatInputWrapper('l10'),
                initialValue=self.store.geo.data['l10'],
            ),
            InputWidget(
                title='l11:',
                onChanged=self.store.body.floatInputWrapper('l11'),
                initialValue=self.store.geo.data['l11'],
            ),
            InputWidget(
                title='l12:',
                onChanged=self.store.body.floatInputWrapper('l12'),
                initialValue=self.store.geo.data['l12'],
            ),
        ]

        super().__init__(children)
        return