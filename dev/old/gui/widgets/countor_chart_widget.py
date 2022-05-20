from dataclasses import dataclass
from enum import Enum

from PyQt5.QtWidgets import QWidget, QHBoxLayout

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backend_bases import MouseButton

from pybird.geometry.geometry import Geometry
from pybird.geometry.utilities.constants import Vector

class CountorChartWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.id = None
        self.fig, self.ax = plt.subplots(1,1,sharex=True)
        self.ax.set_aspect("equal")

        self.update()

        self.fig.canvas.mpl_connect('motion_notify_event', self.on_move)
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
  
        self.canvas = FigureCanvas(self.fig)

        layout = QHBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        return
    
    def update(self) -> None:
        self.plot()
        return

    def plot(self):

        self.fig.clear()
        self.ax = self.fig.add_subplot()
        self.ax.set_aspect("equal")
        self.fig.subplots_adjust(bottom=0.05, right=0.99, top=0.95, left=0.1)

        self.ax.plot([0, 1, 2], [0, 2, 4])

        self.ax.set_title('Section 1')
        self.ax.grid()
        self.fig.canvas.draw()

        return
    
    def find_point_id(self, x: float, y: float) -> int:
        # for i in range(len(self.vertices)):
        #     if -1e-2 < (x - self.vertices[i][1]) < 1e-2 and -1e-2 < (y - self.vertices[i][2]) < 1e-2:
        #         if i in self.allow:
        #             return i
        #         else:
        #             return None
        return None
    
    def on_click(self, event) -> None:
        # if event.inaxes is not None and event.button is MouseButton.LEFT:
        #     self.id = self.find_point_id(event.xdata, event.ydata)
        return
    
    def on_release(self, event) -> None:
        # if event.button is MouseButton.LEFT:
        #     self.id = None
        return

    def on_move(self, event) -> None:
        # if self.id is not None:
        #     dy = event.xdata - self.vertices[self.id][1]
        #     dz = event.ydata - self.vertices[self.id][2]



        #     if self.id <= 7:
        #         sym_id = self.id + 4
        #     else:
        #         sym_id = self.id - 4
        #     self.vertices[self.id] = [self.vertices[self.id][0], self.vertices[self.id][1] + dy, self.vertices[self.id][2] + dz]
        #     self.vertices[sym_id] = [self.vertices[sym_id][0], self.vertices[sym_id][1] - dy, self.vertices[sym_id][2] + dz]

        #     # Update class values
        #     if self.id == 11:
        #         self.sumToValue('delta39', -dy)
        #         self.sumToValue('delta40', dz)

        #     if self.id == 10:
        #         self.sumToValue('delta37', -dy)
        #         self.sumToValue('delta38', dz)

        #     if self.id == 9:
        #         self.sumToValue('delta35', -dy)
        #         self.sumToValue('delta46', dz)

        #     if self.id == 8:
        #         self.sumToValue('delta33', -dy)
        #         self.sumToValue('delta34', dz)

        #     if self.id == 7:
        #         self.sumToValue('delta39', dy)
        #         self.sumToValue('delta40', dz)

        #     if self.id == 6:
        #         self.sumToValue('delta37', dy)
        #         self.sumToValue('delta38', dz)

        #     if self.id == 5:
        #         self.sumToValue('delta35', dy)
        #         self.sumToValue('delta36', dz)

        #     if self.id == 4:
        #         self.sumToValue('delta33', dy)
        #         self.sumToValue('delta34', dz)

        #     self.ax.clear()
        #     self.plot()
        #     self.fig.canvas.draw()
        return