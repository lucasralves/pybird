from pybird.gui.stores.store import Store

from pybird.gui.widgets.row_widget import RowWidget
from pybird.gui.widgets.tab_widget import TabItem, TabWidget
from pybird.gui.widgets.top_chart_widget import TopChartWidget
from pybird.gui.widgets.countor_chart_widget import CountorChartWidget

class ChartsComponent(TabWidget):
    
    def __init__(self, store: Store) -> None:

        self.store = store

        top = TopChartWidget(geo=self.store.geo)
        
        self.store.update.addTopFunc(top.update)

        tabs = [
            TabItem(
                name='Top',
                item=top,
            ),
            TabItem(
                name='Side',
                item=CountorChartWidget(),
            ),
            TabItem(
                name='Sections',
                item=RowWidget(
                    children=[
                        CountorChartWidget(),
                        CountorChartWidget(),
                    ],
                ),
            ),
            TabItem(
                name='3D',
                item=CountorChartWidget(),
            ),
        ]

        super().__init__(tabs)