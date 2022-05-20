from pybird.gui.stores.store import Store

from pybird.geometry.utilities.ui import ButtonWidget
from pybird.gui.widgets.dropdow_widget import DropdownWidget
from pybird.gui.widgets.input_widget import InputWidget
from pybird.gui.widgets.label_widget import LabelWidget
from pybird.gui.widgets.scroll_widget import ScrollWidget

class TailInputComponent(ScrollWidget):

    def __init__(self, store: Store) -> None:

        self.store = store

        children = [
            LabelWidget('Dimensions:'),
            InputWidget(
                title='l16:',
                onChanged=self.store.tail.floatInputWrapper('l16'),
                initialValue=self.store.geo.data['l16'],
            ),
            InputWidget(
                title='l17:',
                onChanged=self.store.tail.floatInputWrapper('l17'),
                initialValue=self.store.geo.data['l17'],
            ),
            InputWidget(
                title='l18:',
                onChanged=self.store.tail.floatInputWrapper('l18'),
                initialValue=self.store.geo.data['l18'],
            ),
            LabelWidget('Shape:'),
            DropdownWidget(
                items=['Rounded', 'Square', 'Pointed', 'V'],
                initialValue=self.store.geo.data['tail_shape'],
                onChanged=self.store.tail.stringInputWrapper('tail_shape'),
                width=185,
            ),
            LabelWidget('Rotation:'),
            InputWidget(
                title='x4:  ',
                onChanged=self.store.tail.updateX4Angle,
                initialValue=self.store.tail.x4,
            ),
            InputWidget(
                title='y4:  ',
                onChanged=self.store.tail.updateY4Angle,
                initialValue=self.store.tail.y4,
            ),
            InputWidget(
                title='z4:  ',
                onChanged=self.store.tail.updateZ4Angle,
                initialValue=self.store.tail.z4,
            ),
            ButtonWidget(
                title='Add Rotation',
                onPressed=self.store.tail.updateTail,
                width=185,
            ),
            ButtonWidget(
                title='Remove Rotations',
                onPressed=self.store.geo.removeTailRotations,
                width=185,
            ),
        ]

        super().__init__(children)
        return