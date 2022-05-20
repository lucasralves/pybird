from pybird.geometry.utilities.ui import ButtonWidget
from pybird.gui.stores.store import Store

from pybird.gui.widgets.dropdow_widget import DropdownWidget
from pybird.gui.widgets.input_widget import InputWidget
from pybird.gui.widgets.label_widget import LabelWidget
from pybird.gui.widgets.scroll_widget import ScrollWidget

class WingInputComponent(ScrollWidget):

    def __init__(self, store: Store) -> None:

        self.store = store

        children = [
            LabelWidget('Dimensions:'),
            InputWidget(
                title='l13:  ',
                onChanged=self.store.wing.floatInputWrapper('l13'),
                initialValue=self.store.geo.data['l13'],
            ),
            InputWidget(
                title='l14:  ',
                onChanged=self.store.wing.floatInputWrapper('l14'),
                initialValue=self.store.geo.data['l14'],
            ),
            InputWidget(
                title='l15:  ',
                onChanged=self.store.wing.floatInputWrapper('l15'),
                initialValue=self.store.geo.data['l15'],
            ),
            LabelWidget('Rotation:'),
            DropdownWidget(
                items=['Left', 'Right'],
                initialValue='Left',
                onChanged=self.store.wing.updateSide,
                width=185,
            ),
            InputWidget(
                title='x1:  ',
                onChanged=self.store.wing.updateX1Angle,
                initialValue=self.store.wing.x1,
            ),
            InputWidget(
                title='y1:  ',
                onChanged=self.store.wing.updateY1Angle,
                initialValue=self.store.wing.y1,
            ),
            InputWidget(
                title='z1:  ',
                onChanged=self.store.wing.updateZ1Angle,
                initialValue=self.store.wing.z1,
            ),
            InputWidget(
                title='y2:  ',
                onChanged=self.store.wing.updateY2Angle,
                initialValue=self.store.wing.y2,
            ),
            InputWidget(
                title='z2:  ',
                onChanged=self.store.wing.updateZ2Angle,
                initialValue=self.store.wing.z2,
            ),
            InputWidget(
                title='x3:  ',
                onChanged=self.store.wing.updateX3Angle,
                initialValue=self.store.wing.x3,
            ),
            InputWidget(
                title='z3:  ',
                onChanged=self.store.wing.updateZ3Angle,
                initialValue=self.store.wing.z3,
            ),
            ButtonWidget(
                title='Add Rotation',
                onPressed=self.store.wing.updateWingAngles,
                width=185,
            ),
            ButtonWidget(
                title='Remove Rotations',
                onPressed=self.store.geo.removeWingRotations,
                width=185,
            ),
            LabelWidget('Profiles file:'),
            InputWidget(
                title='root:     ',
                onChanged=self.store.wing.updateRootProfile,
                initialValue=self.store.wing.rootProfile or '',
                isFloat=False,
            ),
            InputWidget('middle:',
                onChanged=self.store.wing.updateMiddleProfile,
                initialValue=self.store.wing.middleProfile or '',
                isFloat=False,
            ),
            InputWidget(
                title='tip:        ',
                onChanged=self.store.wing.updateTipProfile,
                initialValue=self.store.wing.tipProfile or '',
                isFloat=False,
            ),
            ButtonWidget(
                title='Add Airfoils',
                onPressed=self.store.wing.updateWingFoils,
                width=185,
            ),
        ]

        super().__init__(children)
        return