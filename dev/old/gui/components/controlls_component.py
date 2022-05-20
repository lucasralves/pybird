from pybird.geometry.utilities.ui import ButtonWidget
from pybird.gui.stores.store import Store

from pybird.gui.widgets.column_widget import ColumnWidget

from pybird.gui.components.inputs_component import InputsComponents

class ControllsComponent(ColumnWidget):
    
    def __init__(self, store: Store) -> None:
        self.store = store
        children = [
            InputsComponents(store=store),
            ButtonWidget(
                title='Update Plots',
                onPressed=self.store.update.update,
                width=227,
            ),
            ButtonWidget(
                title='Save',
                onPressed=self.store.save.file,
                width=227,
            ),
        ]
        super().__init__(children)