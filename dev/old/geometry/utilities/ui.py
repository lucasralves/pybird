import sys
from dataclasses import dataclass
from typing import Any, List, TypeVar, Union, Callable, Optional

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QComboBox, QTabWidget, QScrollArea, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton, QDialog
from PyQt5 import QtGui

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from matplotlib.backend_bases import MouseButton
from matplotlib.figure import Figure

from numpy import arccos, asarray, cos, cross, linspace, sin
from numpy.linalg import norm

from pybird.geometry.utilities.constants import Vector

############################################################
# Widgets
############################################################
StretchColumn = TypeVar('StretchColumn')

class ColumnWidget(QWidget):
    
    def __init__(self, children: List[Union[QWidget, StretchColumn]], width: float = None) -> None:
        super().__init__()

        vbox = QVBoxLayout()

        for i in children:
            if i == StretchColumn:
                vbox.addStretch()
            else:
                vbox.addWidget(i)
        
        self.setLayout(vbox)

        if width: self.setFixedWidth(width)

        return

StretchRow = TypeVar('StretchRow')

class RowWidget(QWidget):
    
    def __init__(self, children: List[Union[QWidget, StretchRow]], scale: List[int] = None) -> None:
        super().__init__()

        hbox = QHBoxLayout()

        for i in range(len(children)):
            if children[i] == StretchRow:
                hbox.addStretch()
            else:
                if scale is not None:
                    hbox.addWidget(children[i], scale[i])
                else:
                    hbox.addWidget(children[i])
        
        self.setLayout(hbox)

        return

class InputWidget(QWidget):

    def __init__(self, title: str, onChanged: Callable[[str], None], initialValue: Optional[float] = None, isFloat: bool = True) -> None:
        super().__init__()

        # Set size
        self.setMaximumWidth(185)

        # Label
        label = QLabel(title)

        # Input field
        line = QLineEdit()
        line.textChanged.connect(onChanged)
        if isFloat: line.setValidator(QtGui.QDoubleValidator())
        line.setText(str(initialValue) if initialValue is not None else None)

        # Row
        vbox = QHBoxLayout(self)
        vbox.addWidget(label)
        vbox.addWidget(line)
        vbox.addStretch()
        
        return

class ButtonWidget(QPushButton):

    def __init__(self, title: str, onPressed: Callable[[None], None], width: float = None) -> None:
        super().__init__()

        self.setText(title)
        self.clicked.connect(onPressed)
        if width: self.setFixedWidth(width)

        return

@dataclass
class TabItem:
    item: QWidget
    name: str

class TabWidget(QTabWidget):

    def __init__(self, tabs: List[TabItem], width: float = None) -> None:
        super().__init__()

        # Set tabs
        for tab in tabs:
            self.addTab(tab.item, tab.name)
        
        if width: self.setFixedWidth(width)

        return

class ScrollWidget(QScrollArea):

    def __init__(self, children: List[QWidget]) -> None:
        super().__init__()

        self.setWidget(ColumnWidget(children=children))

        return

class DropdownWidget(QWidget):

    def __init__(self, title: str, items: List[str], initialValue: str, onChanged: Callable[[str], None]) -> None:
        super().__init__()

        self.onChanged = onChanged

        # Label
        label = QLabel(title)

        # Input field
        self.combo = QComboBox()
        self.combo.addItems(items)
        self.combo.currentIndexChanged.connect(self.onIndexChanged)
        self.combo.setCurrentText(initialValue)

        # Row
        vbox = QHBoxLayout(self)
        if title: vbox.addWidget(label)
        vbox.addWidget(self.combo)

        return
    
    def onIndexChanged(self, i: int) -> None:
        self.onChanged(self.combo.currentText())
        return

class DialogWidget(QDialog):

    def __init__(self, saveFilename: Callable[[str], None], save: Callable[[], None]) -> None:
        super().__init__()

        self.setWindowTitle('Save Geometry')

        vBox = QVBoxLayout()
        vBox.addWidget(InputWidget(
            title='File',
            onChanged=saveFilename,
            isFloat=False,
        ))
        vBox.addWidget(ButtonWidget(
            title='Save',
            onPressed=save
        ))

        self.setLayout(vBox)

        return

class TopViewChart(QWidget):

    def __init__(self, p1_e: Vector, p2_e: Vector, p3_e: Vector, p4_e: Vector,
                       p1_d: Vector, p2_d: Vector, p3_d: Vector, p4_d: Vector,
                       c1_e: Vector, c2_e: Vector, c3_e: Vector, c4_e: Vector,
                       c1_d: Vector, c2_d: Vector, c3_d: Vector, c4_d: Vector,
                       sumToValue: Callable):
        super().__init__()

        self.sumToValue = sumToValue

        self.vertices = [
            p1_e, p2_e, p3_e, p4_e,
            p1_d, p2_d, p3_d, p4_d,
            c1_e, c2_e, c3_e, c4_e,
            c1_d, c2_d, c3_d, c4_d
        ]
        self.curves = [
            [0, 8, 9, 1],
            [2, 10, 11, 3],
            [4, 12, 13, 5],
            [6, 14, 15, 7]
        ]
        self.allow = [8, 9, 10, 11, 12, 13, 14, 15]

        self.id = None
        self.fig, self.ax = plt.subplots(1,1,figsize=(9.0,8.0),sharex=True)
        self.ax.set_aspect("equal")

        self.plot()

        self.fig.canvas.mpl_connect('motion_notify_event', self.on_move)
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
  
        self.canvas = FigureCanvas(self.fig)

        layout = QHBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        return
    
    def updateValues(self, p1_e: Vector, p2_e: Vector, p3_e: Vector, p4_e: Vector,
                           p1_d: Vector, p2_d: Vector, p3_d: Vector, p4_d: Vector,
                           c1_e: Vector, c2_e: Vector, c3_e: Vector, c4_e: Vector,
                           c1_d: Vector, c2_d: Vector, c3_d: Vector, c4_d: Vector,) -> None:
        self.vertices = [
            p1_e, p2_e, p3_e, p4_e,
            p1_d, p2_d, p3_d, p4_d,
            c1_e, c2_e, c3_e, c4_e,
            c1_d, c2_d, c3_d, c4_d
        ]
        self.plot()
        return
  
    # action called by the push button
    def plot(self):

        self.fig.clear()
        self.ax = self.fig.add_subplot()
        self.ax.set_aspect("equal")

        # self.fig.tight_layout(h_pad=2, w_pad=2)
        self.fig.subplots_adjust(bottom=0.05, right=0.99, top=0.95, left=0.1)

        # Create bezier curves
        for curve in self.curves:

            verts = []
            codes = []

            curve_type = Path.CURVE3 if len(curve) == 3 else Path.CURVE4
            
            for i in range(len(curve)):
                verts.append( (self.vertices[curve[i]][0], self.vertices[curve[i]][1]) )
                codes.append( Path.MOVETO if i == 0 else curve_type )
                if i == 0 or i == len(curve) - 1:
                    self.ax.scatter(self.vertices[curve[i]][0], self.vertices[curve[i]][1], color='blue')
                else:
                    self.ax.scatter(self.vertices[curve[i]][0], self.vertices[curve[i]][1], color='red')

            
            xs, ys = zip(*verts)
            self.ax.plot(xs, ys, '--', lw=1, color='grey', ms=10)

            path = Path(verts, codes)
            patch = patches.PathPatch(path, facecolor='none', lw=2)
            self.ax.add_patch(patch)
        
        self.ax.plot([self.vertices[1][0], self.vertices[2][0]], [self.vertices[1][1], self.vertices[2][1]], 'k--')
        self.ax.plot([self.vertices[5][0], self.vertices[6][0]], [self.vertices[5][1], self.vertices[6][1]], 'k--')
        self.ax.plot([self.vertices[0][0], self.vertices[4][0]], [self.vertices[0][1], self.vertices[4][1]], 'k--')
        self.ax.plot([self.vertices[3][0], self.vertices[7][0]], [self.vertices[3][1], self.vertices[7][1]], 'k--')

        self.ax.set_title('Top')
        self.ax.grid()
        self.fig.canvas.draw()

        return
    
    def find_point_id(self, x: float, y: float) -> int:
        for i in range(len(self.vertices)):
            if -1e-2 < (x - self.vertices[i][0]) < 1e-2 and -1e-2 < (y - self.vertices[i][1]) < 1e-2:
                if i in self.allow:
                    return i
                else:
                    return None
        return None
    
    def on_click(self, event) -> None:
        if event.inaxes is not None and event.button is MouseButton.LEFT:
            self.id = self.find_point_id(event.xdata, event.ydata)
        return
    
    def on_release(self, event) -> None:
        if event.button is MouseButton.LEFT:
            self.id = None
        return

    def on_move(self, event) -> None:
        if self.id is not None:
            dx = event.xdata - self.vertices[self.id][0]
            dy = event.ydata - self.vertices[self.id][1]

            if self.id <= 11:
                sym_id = self.id + 4
            else:
                sym_id = self.id - 4
            self.vertices[self.id] = [self.vertices[self.id][0] + dx, self.vertices[self.id][1] + dy, self.vertices[self.id][2]]
            self.vertices[sym_id] = [self.vertices[sym_id][0] + dx, self.vertices[sym_id][1] - dy, self.vertices[sym_id][2]]

            # Update class values
            if self.id == 15:
                self.sumToValue('delta7', dx)
                self.sumToValue('delta8', -dy)

            if self.id == 14:
                self.sumToValue('delta5', dx)
                self.sumToValue('delta6', -dy)

            if self.id == 13:
                self.sumToValue('delta3', dx)
                self.sumToValue('delta4', -dy)

            if self.id == 12:
                self.sumToValue('delta1', dx)
                self.sumToValue('delta2', -dy)

            if self.id == 11:
                self.sumToValue('delta7', dx)
                self.sumToValue('delta8', dy)

            if self.id == 10:
                self.sumToValue('delta5', dx)
                self.sumToValue('delta6', dy)

            if self.id == 9:
                self.sumToValue('delta3', dx)
                self.sumToValue('delta4', dy)

            if self.id == 8:
                self.sumToValue('delta1', dx)
                self.sumToValue('delta2', dy)

            self.ax.clear()
            self.plot()
            self.fig.canvas.draw()
        return

class SideViewChart(QWidget):

    def __init__(self, p5: Vector, p6: Vector, p7: Vector, p8: Vector,
                       p9: Vector, p10: Vector, p11: Vector, p12: Vector,
                       c5: Vector, c6: Vector, c7: Vector, c8: Vector, c9: Vector, c10: Vector,
                       c11: Vector, c12: Vector, c13: Vector, c14: Vector, c15: Vector, c16: Vector,
                       sumToValue: Callable):
        super().__init__()

        self.sumToValue = sumToValue

        self.vertices = [
            p5, p6, p7, p8,
            p9, p10, p11, p12,
            c5, c6, c7, c8, c9, c10,
            c11, c12, c13, c14, c15, c16,
        ]
        self.curves = [
            [0, 8, 9, 1],
            [1, 10, 11, 2],
            [2, 12, 13, 3],
            [4, 14, 15, 5],
            [5, 16, 17, 6],
            [6, 18, 19, 7]
        ]
        self.allow = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

        self.id = None
        self.fig, self.ax = plt.subplots(1,1,figsize=(9.0,8.0),sharex=True)
        self.ax.set_aspect("equal")

        self.plot()

        self.fig.canvas.mpl_connect('motion_notify_event', self.on_move)
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
  
        self.canvas = FigureCanvas(self.fig)

        layout = QHBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        return
    
    def updateValues(self, p5: Vector, p6: Vector, p7: Vector, p8: Vector,
                       p9: Vector, p10: Vector, p11: Vector, p12: Vector,
                       c5: Vector, c6: Vector, c7: Vector, c8: Vector, c9: Vector, c10: Vector,
                       c11: Vector, c12: Vector, c13: Vector, c14: Vector, c15: Vector, c16: Vector,) -> None:
        self.vertices = [
            p5, p6, p7, p8,
            p9, p10, p11, p12,
            c5, c6, c7, c8, c9, c10,
            c11, c12, c13, c14, c15, c16,
        ]
        self.plot()
        return
  
    # action called by the push button
    def plot(self):

        self.fig.clear()
        self.ax = self.fig.add_subplot()
        self.ax.set_aspect("equal")

        # self.fig.tight_layout(h_pad=2, w_pad=2)
        self.fig.subplots_adjust(bottom=0.05, right=0.99, top=0.95, left=0.1)

        # Create bezier curves
        for curve in self.curves:

            verts = []
            codes = []

            curve_type = Path.CURVE3 if len(curve) == 3 else Path.CURVE4
            
            for i in range(len(curve)):
                verts.append( (self.vertices[curve[i]][0], self.vertices[curve[i]][2]) )
                codes.append( Path.MOVETO if i == 0 else curve_type )
                if i == 0 or i == len(curve) - 1:
                    self.ax.scatter(self.vertices[curve[i]][0], self.vertices[curve[i]][2], color='blue')
                else:
                    self.ax.scatter(self.vertices[curve[i]][0], self.vertices[curve[i]][2], color='red')

            
            xs, ys = zip(*verts)
            self.ax.plot(xs, ys, '--', lw=1, color='grey', ms=10)

            path = Path(verts, codes)
            patch = patches.PathPatch(path, facecolor='none', lw=2)
            self.ax.add_patch(patch)
        
        self.ax.plot([self.vertices[0][0], self.vertices[4][0]], [self.vertices[0][2], self.vertices[4][2]], 'k--')
        self.ax.plot([self.vertices[3][0], self.vertices[7][0]], [self.vertices[3][2], self.vertices[7][2]], 'k--')
        
        self.ax.set_title('Side')
        self.ax.grid()
        self.fig.canvas.draw()

        return
    
    def find_point_id(self, x: float, y: float) -> int:
        for i in range(len(self.vertices)):
            if -1e-2 < (x - self.vertices[i][0]) < 1e-2 and -1e-2 < (y - self.vertices[i][2]) < 1e-2:
                if i in self.allow:
                    return i
                else:
                    return None
        return None
    
    def on_click(self, event) -> None:
        if event.inaxes is not None and event.button is MouseButton.LEFT:
            self.id = self.find_point_id(event.xdata, event.ydata)
        return
    
    def on_release(self, event) -> None:
        if event.button is MouseButton.LEFT:
            self.id = None
        return

    def on_move(self, event) -> None:
        if self.id is not None:
            dx = event.xdata - self.vertices[self.id][0]
            dz = event.ydata - self.vertices[self.id][2]
            
            self.vertices[self.id] = [self.vertices[self.id][0] + dx, self.vertices[self.id][1], self.vertices[self.id][2] + dz]

            # Update class values
            if self.id == 19:
                self.sumToValue('delta31', dx)
                self.sumToValue('delta32', -dz)
            
            if self.id == 18:
                self.sumToValue('delta29', dx)
                self.sumToValue('delta30', -dz)
            
            if self.id == 17:
                self.sumToValue('delta27', dx)
                self.sumToValue('delta28', -dz)
            
            if self.id == 16:
                self.sumToValue('delta25', dx)
                self.sumToValue('delta26', -dz)
            
            if self.id == 15:
                self.sumToValue('delta23', dx)
                self.sumToValue('delta24', -dz)

            if self.id == 14:
                self.sumToValue('delta21', dx)
                self.sumToValue('delta22', -dz)

            if self.id == 13:
                self.sumToValue('delta19', dx)
                self.sumToValue('delta20', dz)

            if self.id == 12:
                self.sumToValue('delta17', dx)
                self.sumToValue('delta18', dz)

            if self.id == 11:
                self.sumToValue('delta15', dx)
                self.sumToValue('delta16', dz)

            if self.id == 10:
                self.sumToValue('delta13', dx)
                self.sumToValue('delta14', dz)

            if self.id == 9:
                self.sumToValue('delta11', dx)
                self.sumToValue('delta12', dz)

            if self.id == 8:
                self.sumToValue('delta9', dx)
                self.sumToValue('delta10', dz)

            self.ax.clear()
            self.plot()
            self.fig.canvas.draw()
        return

class SectionOneViewChart(QWidget):

    def __init__(self, p6: Vector, p2_e: Vector, p10: Vector, p2_d: Vector,
                       c17_e: Vector, c18_e: Vector, c19_e: Vector, c20_e: Vector,
                       c17_d: Vector, c18_d: Vector, c19_d: Vector, c20_d: Vector,
                       sumToValue: Callable):
        super().__init__()

        self.sumToValue = sumToValue

        self.vertices = [
            p6, p2_e, p10, p2_d,
            c17_e, c18_e, c19_e, c20_e,
            c17_d, c18_d, c19_d, c20_d,
        ]
        self.curves = [
            [0, 4, 5, 1],
            [1, 6, 7, 2],
            [2, 11, 10, 3],
            [3, 9, 8, 0]
        ]
        self.allow = [4, 5, 6, 7, 8, 9, 10, 11]

        self.id = None
        self.fig, self.ax = plt.subplots(1,1,figsize=(9.0,8.0),sharex=True)
        self.ax.set_aspect("equal")

        self.plot()

        self.fig.canvas.mpl_connect('motion_notify_event', self.on_move)
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
  
        self.canvas = FigureCanvas(self.fig)

        layout = QHBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        return
    
    def updateValues(self, p6: Vector, p2_e: Vector, p10: Vector, p2_d: Vector,
                           c17_e: Vector, c18_e: Vector, c19_e: Vector, c20_e: Vector,
                           c17_d: Vector, c18_d: Vector, c19_d: Vector, c20_d: Vector,) -> None:
        self.vertices = [
            p6, p2_e, p10, p2_d,
            c17_e, c18_e, c19_e, c20_e,
            c17_d, c18_d, c19_d, c20_d,
        ]
        self.plot()
        return
  
    # action called by the push button
    def plot(self):

        self.fig.clear()
        self.ax = self.fig.add_subplot()
        self.ax.set_aspect("equal")

        # self.fig.tight_layout(h_pad=2, w_pad=2)
        self.fig.subplots_adjust(bottom=0.05, right=0.99, top=0.95, left=0.1)

        # Create bezier curves
        for curve in self.curves:

            verts = []
            codes = []

            curve_type = Path.CURVE3 if len(curve) == 3 else Path.CURVE4
            
            for i in range(len(curve)):
                verts.append( (self.vertices[curve[i]][1], self.vertices[curve[i]][2]) )
                codes.append( Path.MOVETO if i == 0 else curve_type )
                if i == 0 or i == len(curve) - 1:
                    self.ax.scatter(self.vertices[curve[i]][1], self.vertices[curve[i]][2], color='blue')
                else:
                    self.ax.scatter(self.vertices[curve[i]][1], self.vertices[curve[i]][2], color='red')

            
            xs, ys = zip(*verts)
            self.ax.plot(xs, ys, '--', lw=1, color='grey', ms=10)

            path = Path(verts, codes)
            patch = patches.PathPatch(path, facecolor='none', lw=2)
            self.ax.add_patch(patch)

        self.ax.set_title('Section 1')
        self.ax.grid()
        self.fig.canvas.draw()

        return
    
    def find_point_id(self, x: float, y: float) -> int:
        for i in range(len(self.vertices)):
            if -1e-2 < (x - self.vertices[i][1]) < 1e-2 and -1e-2 < (y - self.vertices[i][2]) < 1e-2:
                if i in self.allow:
                    return i
                else:
                    return None
        return None
    
    def on_click(self, event) -> None:
        if event.inaxes is not None and event.button is MouseButton.LEFT:
            self.id = self.find_point_id(event.xdata, event.ydata)
        return
    
    def on_release(self, event) -> None:
        if event.button is MouseButton.LEFT:
            self.id = None
        return

    def on_move(self, event) -> None:
        if self.id is not None:
            dy = event.xdata - self.vertices[self.id][1]
            dz = event.ydata - self.vertices[self.id][2]



            if self.id <= 7:
                sym_id = self.id + 4
            else:
                sym_id = self.id - 4
            self.vertices[self.id] = [self.vertices[self.id][0], self.vertices[self.id][1] + dy, self.vertices[self.id][2] + dz]
            self.vertices[sym_id] = [self.vertices[sym_id][0], self.vertices[sym_id][1] - dy, self.vertices[sym_id][2] + dz]

            # Update class values
            if self.id == 11:
                self.sumToValue('delta39', -dy)
                self.sumToValue('delta40', dz)

            if self.id == 10:
                self.sumToValue('delta37', -dy)
                self.sumToValue('delta38', dz)

            if self.id == 9:
                self.sumToValue('delta35', -dy)
                self.sumToValue('delta46', dz)

            if self.id == 8:
                self.sumToValue('delta33', -dy)
                self.sumToValue('delta34', dz)

            if self.id == 7:
                self.sumToValue('delta39', dy)
                self.sumToValue('delta40', dz)

            if self.id == 6:
                self.sumToValue('delta37', dy)
                self.sumToValue('delta38', dz)

            if self.id == 5:
                self.sumToValue('delta35', dy)
                self.sumToValue('delta36', dz)

            if self.id == 4:
                self.sumToValue('delta33', dy)
                self.sumToValue('delta34', dz)

            self.ax.clear()
            self.plot()
            self.fig.canvas.draw()
        return

class SectionTwoViewChart(QWidget):

    def __init__(self, p7: Vector, p3_e: Vector, p11: Vector, p3_d: Vector,
                       c21_e: Vector, c22_e: Vector, c23_e: Vector, c24_e: Vector,
                       c21_d: Vector, c22_d: Vector, c23_d: Vector, c24_d: Vector,
                       sumToValue: Callable):
        super().__init__()

        self.sumToValue = sumToValue

        self.vertices = [
            p7, p3_e, p11, p3_d,
            c21_e, c22_e, c23_e, c24_e,
            c21_d, c22_d, c23_d, c24_d,
        ]
        self.curves = [
            [0, 4, 5, 1],
            [1, 6, 7, 2],
            [2, 11, 10, 3],
            [3, 9, 8, 0]
        ]
        self.allow = [4, 5, 6, 7, 8, 9, 10, 11]

        self.id = None
        self.fig, self.ax = plt.subplots(1,1,figsize=(9.0,8.0),sharex=True)
        self.ax.set_aspect("equal")

        self.plot()

        self.fig.canvas.mpl_connect('motion_notify_event', self.on_move)
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
  
        self.canvas = FigureCanvas(self.fig)

        layout = QHBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        return
    
    def updateValues(self, p7: Vector, p3_e: Vector, p11: Vector, p3_d: Vector,
                          c21_e: Vector, c22_e: Vector, c23_e: Vector, c24_e: Vector,
                          c21_d: Vector, c22_d: Vector, c23_d: Vector, c24_d: Vector,) -> None:
        self.vertices = [
            p7, p3_e, p11, p3_d,
            c21_e, c22_e, c23_e, c24_e,
            c21_d, c22_d, c23_d, c24_d,
        ]
        self.plot()
        return
  
    # action called by the push button
    def plot(self):

        self.fig.clear()
        self.ax = self.fig.add_subplot()
        self.ax.set_aspect("equal")

        # self.fig.tight_layout(h_pad=2, w_pad=2)
        self.fig.subplots_adjust(bottom=0.05, right=0.99, top=0.95, left=0.1)

        # Create bezier curves
        for curve in self.curves:

            verts = []
            codes = []

            curve_type = Path.CURVE3 if len(curve) == 3 else Path.CURVE4
            
            for i in range(len(curve)):
                verts.append( (self.vertices[curve[i]][1], self.vertices[curve[i]][2]) )
                codes.append( Path.MOVETO if i == 0 else curve_type )
                if i == 0 or i == len(curve) - 1:
                    self.ax.scatter(self.vertices[curve[i]][1], self.vertices[curve[i]][2], color='blue')
                else:
                    self.ax.scatter(self.vertices[curve[i]][1], self.vertices[curve[i]][2], color='red')

            
            xs, ys = zip(*verts)
            self.ax.plot(xs, ys, '--', lw=1, color='grey', ms=10)

            path = Path(verts, codes)
            patch = patches.PathPatch(path, facecolor='none', lw=2)
            self.ax.add_patch(patch)

        self.ax.set_title('Section 2')
        self.ax.grid()
        self.fig.canvas.draw()

        return
    
    def find_point_id(self, x: float, y: float) -> int:
        for i in range(len(self.vertices)):
            if -1e-2 < (x - self.vertices[i][1]) < 1e-2 and -1e-2 < (y - self.vertices[i][2]) < 1e-2:
                if i in self.allow:
                    return i
                else:
                    return None
        return None
    
    def on_click(self, event) -> None:
        if event.inaxes is not None and event.button is MouseButton.LEFT:
            self.id = self.find_point_id(event.xdata, event.ydata)
        return
    
    def on_release(self, event) -> None:
        if event.button is MouseButton.LEFT:
            self.id = None
        return

    def on_move(self, event) -> None:
        if self.id is not None:
            dy = event.xdata - self.vertices[self.id][1]
            dz = event.ydata - self.vertices[self.id][2]

            if self.id <= 7:
                sym_id = self.id + 4
            else:
                sym_id = self.id - 4
            self.vertices[self.id] = [self.vertices[self.id][0], self.vertices[self.id][1] + dy, self.vertices[self.id][2] + dz]
            self.vertices[sym_id] = [self.vertices[sym_id][0], self.vertices[sym_id][1] - dy, self.vertices[sym_id][2] + dz]

            # Update class values
            if self.id == 11:
                self.sumToValue('delta47', -dy)
                self.sumToValue('delta48', dz)

            if self.id == 10:
                self.sumToValue('delta45', -dy)
                self.sumToValue('delta46', dz)

            if self.id == 9:
                self.sumToValue('delta43', -dy)
                self.sumToValue('delta44', dz)

            if self.id == 8:
                self.sumToValue('delta41', -dy)
                self.sumToValue('delta42', dz)

            if self.id == 7:
                self.sumToValue('delta47', dy)
                self.sumToValue('delta48', dz)

            if self.id == 6:
                self.sumToValue('delta45', dy)
                self.sumToValue('delta46', dz)

            if self.id == 5:
                self.sumToValue('delta43', dy)
                self.sumToValue('delta44', dz)

            if self.id == 4:
                self.sumToValue('delta41', dy)
                self.sumToValue('delta42', dz)

            self.ax.clear()
            self.plot()
            self.fig.canvas.draw()
        return

class TailViewChart(QWidget):

    def __init__(self, p4_e: Vector, p4_d: Vector, p18: Vector, p19: Vector, p20: Vector, c31: Vector, tailShape: str):
        super().__init__()

        self.p4_e, self.p4_d, self.p18, self.p19, self.p20, self.c31 = p4_e, p4_d, p18, p19, p20, c31
        self.tailShape = tailShape

        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111, projection='3d')

        self.plot()

        layout = QHBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        return
    
    def updateValues(self, p4_e: Vector, p4_d: Vector, p18: Vector, p19: Vector, p20: Vector, c31: Vector, tailShape: str) -> None:
        self.p4_e, self.p4_d, self.p18, self.p19, self.p20, self.c31 = p4_e, p4_d, p18, p19, p20, c31
        self.tailShape = tailShape
        self.plot()
        return
  
    # action called by the push button
    def plot(self):

        self.fig.clear()
        self.ax = self.fig.add_subplot(111, projection='3d')

        self.fig.subplots_adjust(bottom=0.05, right=0.99, top=0.95, left=0.1)

        if self.tailShape == 'Rounded':
            self.plot_rounded()
        elif self.tailShape == 'Pointed' or self.tailShape == 'Square':
            self.plot_square_pointed()
        else:
            self.plot_V()

        center = [
            (self.p4_e[0] + self.p4_d[0] + self.p18[0] + self.p19[0]) / 4,
            (self.p4_e[1] + self.p4_d[1] + self.p18[1] + self.p19[1]) / 4,
            (self.p4_e[2] + self.p4_d[2] + self.p18[2] + self.p19[2]) / 4,
        ]

        max_dist = 0.7 * ((self.p4_e[0] - self.p19[0]) ** 2 + (self.p4_e[1] - self.p19[1]) ** 2 + (self.p4_e[2] - self.p19[2]) ** 2) ** 0.5

        self.ax.set_xlim(center[0] - max_dist, center[0] + max_dist)
        self.ax.set_ylim(center[1] - max_dist, center[1] + max_dist)
        self.ax.set_zlim(center[2] - max_dist, center[2] + max_dist)

        self.fig.canvas.draw()

        return
    
    def plot_rounded(self) -> None:

        v1 = asarray(self.p18) - asarray(self.c31)
        v1_norm = norm(v1)
        v1 = v1 / v1_norm

        v2 = asarray(self.p19) - asarray(self.c31)
        v2 = v2 / v1_norm

        n = cross(v1, v2)
        v3 = cross(n, v1)

        theta_max = arccos(v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2])
        theta = linspace(0, theta_max, num=50)

        coord_x = cos(theta) * v1_norm
        coord_y = sin(theta) * v1_norm

        arc_circle_x = []
        arc_circle_y = []
        arc_circle_z = []
        for i in range(50):
            arc_circle_x.append(coord_x[i] * v1[0] + coord_y[i] * v3[0] + self.c31[0])
            arc_circle_y.append(coord_x[i] * v1[1] + coord_y[i] * v3[1] + self.c31[1])
            arc_circle_z.append(coord_x[i] * v1[2] + coord_y[i] * v3[2] + self.c31[2])

        x = [self.p4_e[0], self.p18[0]] + arc_circle_x + [self.p19[0], self.p4_d[0]]
        y = [self.p4_e[1], self.p18[1]] + arc_circle_y + [self.p19[1], self.p4_d[1]]
        z = [self.p4_e[2], self.p18[2]] + arc_circle_z + [self.p19[2], self.p4_d[2]]

        self.ax.plot_trisurf(x, y, z)

        self.ax.scatter(self.p4_e[0], self.p4_e[1],self.p4_e[2], color='green')
        self.ax.scatter(self.p4_d[0], self.p4_d[1],self.p4_d[2], color='green')
        self.ax.scatter(self.p18[0], self.p18[1],self.p18[2], color='green')
        self.ax.scatter(self.p19[0], self.p19[1],self.p19[2], color='green')
        self.ax.scatter(self.c31[0], self.c31[1],self.c31[2], color='red')

        self.fig.canvas.draw()
        
        return
    
    def plot_square_pointed(self) -> None:
        x = [self.p4_e[0], self.p18[0], self.p20[0], self.p19[0], self.p4_d[0]]
        y = [self.p4_e[1], self.p18[1], self.p20[1], self.p19[1], self.p4_d[1]]
        z = [self.p4_e[2], self.p18[2], self.p20[2], self.p19[2], self.p4_d[2]]

        self.ax.plot_trisurf(x, y, z)

        self.ax.scatter(self.p4_e[0], self.p4_e[1],self.p4_e[2], color='green')
        self.ax.scatter(self.p4_d[0], self.p4_d[1],self.p4_d[2], color='green')
        self.ax.scatter(self.p18[0], self.p18[1],self.p18[2], color='green')
        self.ax.scatter(self.p19[0], self.p19[1],self.p19[2], color='green')

        self.fig.canvas.draw()

        return
    
    def plot_V(self) -> None:
        x1 = [self.p4_e[0], self.p18[0], self.p20[0]]
        y1 = [self.p4_e[1], self.p18[1], self.p20[1]]
        z1 = [self.p4_e[2], self.p18[2], self.p20[2]]

        x2 = [self.p4_e[0], self.p20[0], self.p4_d[0]]
        y2 = [self.p4_e[1], self.p20[1], self.p4_d[1]]
        z2 = [self.p4_e[2], self.p20[2], self.p4_d[2]]

        x3 = [self.p20[0], self.p19[0], self.p4_d[0]]
        y3 = [self.p20[1], self.p19[1], self.p4_d[1]]
        z3 = [self.p20[2], self.p19[2], self.p4_d[2]]

        self.ax.plot_trisurf(x1, y1, z1, color='C0')
        self.ax.plot_trisurf(x2, y2, z2, color='C0')
        self.ax.plot_trisurf(x3, y3, z3, color='C0')

        self.ax.scatter(self.p4_e[0], self.p4_e[1],self.p4_e[2], color='green')
        self.ax.scatter(self.p4_d[0], self.p4_d[1],self.p4_d[2], color='green')
        self.ax.scatter(self.p18[0], self.p18[1],self.p18[2], color='green')
        self.ax.scatter(self.p19[0], self.p19[1],self.p19[2], color='green')

        self.fig.canvas.draw()

        return

############################################################
# Controller
############################################################
class Controller:

    def __init__(self) -> None:
        self.tailX4Angle = None
        self.tailY4Angle = None
        self.tailZ4Angle = None

        self.tailFoil = None
        return
    
    def addTailFoil(self, file: str) -> None:
        self.tailFoil = file
        return
    
    def saveTailX4Rotation(self, value: str) -> None:
        self.tailX4Angle = float(value)
        return
    
    def saveTailY4Rotation(self, value: str) -> None:
        self.tailY4Angle = float(value)
        return
    
    def saveTailZ4Rotation(self, value: str) -> None:
        self.tailZ4Angle = float(value)
        return
    
    def tailApplyRotationWrapper(self, addRotation: Callable[[str, float], None], geo, tailUpdate: Callable) -> None:
        def wrapper():
            if self.tailX4Angle: addRotation('x4', self.tailX4Angle)
            if self.tailY4Angle: addRotation('y4', self.tailY4Angle)
            if self.tailZ4Angle: addRotation('z4', self.tailZ4Angle)

            self.tailX4Angle = None
            self.tailY4Angle = None
            self.tailZ4Angle = None

            tailUpdate(
                p4_e=geo.params.p4_e,
                p4_d=geo.params.p4_d,
                p18=geo.params.p18,
                p19=geo.params.p19,
                p20=geo.params.p20_square if geo.data['tail_shape'] == 'Square' else geo.params.p20_V if geo.data['tail_shape'] == 'V' else geo.params.p20_pointed,
                c31=geo.params.c31,
                tailShape=geo.data['tail_shape'],
            )

            return
        return wrapper

    def saveFilename(self, file: str) -> None:
        self.filename = file
        return

    def updateStringValueWrapper(self, key: str, func: Callable[[str, Any], None]) -> Callable:
        def wrapper(value: str):
            return func(key, value)
        return wrapper
    
    def updateFloatValueWrapper(self, key: str, func: Callable[[str, Any], None]) -> Callable:
        def wrapper(value: str):
            return func(key, float(value))
        return wrapper
    
    def saveWrapper(self, save: Callable[[str], None]) -> None:
        def wrapper():
            if self.filename: save(self.filename)
            return
        return wrapper
    
    def updatePlotWrapper(self, topBody: Callable,
                                sideBody: Callable,
                                geo,
                                secOneBody: Callable,
                                secTwoBody: Callable,
                                tail: Callable,) -> None:
        def wrapper():
            if self.tailFoil: geo.addTailFoil(self.tailFoil)
            tail(
                p4_e=geo.params.p4_e,
                p4_d=geo.params.p4_d,
                p18=geo.params.p18,
                p19=geo.params.p19,
                p20=geo.params.p20_square if geo.data['tail_shape'] == 'Square' else geo.params.p20_V if geo.data['tail_shape'] == 'V' else geo.params.p20_pointed,
                c31=geo.params.c31,
                tailShape=geo.data['tail_shape'],
            )
            topBody(
                p1_e=geo.params.p1_e,
                p2_e=geo.params.p2_e,
                p3_e=geo.params.p3_e,
                p4_e=geo.params.p4_e,
                p1_d=geo.params.p1_d,
                p2_d=geo.params.p2_d,
                p3_d=geo.params.p3_d,
                p4_d=geo.params.p4_d,
                c1_e=geo.params.c1_e,
                c2_e=geo.params.c2_e,
                c3_e=geo.params.c3_e,
                c4_e=geo.params.c4_e,
                c1_d=geo.params.c1_d,
                c2_d=geo.params.c2_d,
                c3_d=geo.params.c3_d,
                c4_d=geo.params.c4_d,
            )
            sideBody(
                p5=geo.params.p5,
                p6=geo.params.p6,
                p7=geo.params.p7,
                p8=geo.params.p8,
                p9=geo.params.p9,
                p10=geo.params.p10,
                p11=geo.params.p11,
                p12=geo.params.p12,
                c5=geo.params.c5,
                c6=geo.params.c6,
                c7=geo.params.c7,
                c8=geo.params.c8,
                c9=geo.params.c9,
                c10=geo.params.c10,
                c11=geo.params.c11,
                c12=geo.params.c12,
                c13=geo.params.c13,
                c14=geo.params.c14,
                c15=geo.params.c15,
                c16=geo.params.c16,
            )
            secOneBody(
                p6=geo.params.p6,
                p2_e=geo.params.p2_e,
                p2_d=geo.params.p2_d,
                p10=geo.params.p10,
                c17_e=geo.params.c17_e,
                c17_d=geo.params.c17_d,
                c18_e=geo.params.c18_e,
                c18_d=geo.params.c18_d,
                c19_e=geo.params.c19_e,
                c19_d=geo.params.c19_d,
                c20_e=geo.params.c20_e,
                c20_d=geo.params.c20_d,
            )
            secTwoBody(
                p7=geo.params.p7,
                p3_e=geo.params.p3_e,
                p3_d=geo.params.p3_d,
                p11=geo.params.p11,
                c21_e=geo.params.c21_e,
                c21_d=geo.params.c21_d,
                c22_e=geo.params.c22_e,
                c22_d=geo.params.c22_d,
                c23_e=geo.params.c23_e,
                c23_d=geo.params.c23_d,
                c24_e=geo.params.c24_e,
                c24_d=geo.params.c24_d,
            )
            return
        return wrapper
    
    def showSaveDialogWrapper(self, save: Callable[[], None]) -> None:
        def wrapper():
            dialog = DialogWidget(self.saveFilename, self.saveWrapper(save))
            dialog.exec()
            return
        return wrapper

############################################################
# Main view
############################################################
class _MainWindow(QMainWindow):

    def __init__(self, geo) -> None:
        super().__init__()

        self.geo = geo
        self.controller = Controller()

        self.setWindowTitle('Geometry')
        self.setGeometry(0, 0, 1000, 600)

        topViewChart = TopViewChart(
            p1_e=self.geo.params.p1_e,
            p2_e=self.geo.params.p2_e,
            p3_e=self.geo.params.p3_e,
            p4_e=self.geo.params.p4_e,
            p1_d=self.geo.params.p1_d,
            p2_d=self.geo.params.p2_d,
            p3_d=self.geo.params.p3_d,
            p4_d=self.geo.params.p4_d,
            c1_e=self.geo.params.c1_e,
            c2_e=self.geo.params.c2_e,
            c3_e=self.geo.params.c3_e,
            c4_e=self.geo.params.c4_e,
            c1_d=self.geo.params.c1_d,
            c2_d=self.geo.params.c2_d,
            c3_d=self.geo.params.c3_d,
            c4_d=self.geo.params.c4_d,
            sumToValue=self.geo.sumToValue,
        )

        sideViewChart = SideViewChart(
            p5=self.geo.params.p5,
            p6=self.geo.params.p6,
            p7=self.geo.params.p7,
            p8=self.geo.params.p8,
            p9=self.geo.params.p9,
            p10=self.geo.params.p10,
            p11=self.geo.params.p11,
            p12=self.geo.params.p12,
            c5=self.geo.params.c5,
            c6=self.geo.params.c6,
            c7=self.geo.params.c7,
            c8=self.geo.params.c8,
            c9=self.geo.params.c9,
            c10=self.geo.params.c10,
            c11=self.geo.params.c11,
            c12=self.geo.params.c12,
            c13=self.geo.params.c13,
            c14=self.geo.params.c14,
            c15=self.geo.params.c15,
            c16=self.geo.params.c16,
            sumToValue=self.geo.sumToValue,
        )

        sectionOneViewChart = SectionOneViewChart(
            p6=self.geo.params.p6,
            p2_e=self.geo.params.p2_e,
            p2_d=self.geo.params.p2_d,
            p10=self.geo.params.p10,
            c17_e=self.geo.params.c17_e,
            c17_d=self.geo.params.c17_d,
            c18_e=self.geo.params.c18_e,
            c18_d=self.geo.params.c18_d,
            c19_e=self.geo.params.c19_e,
            c19_d=self.geo.params.c19_d,
            c20_e=self.geo.params.c20_e,
            c20_d=self.geo.params.c20_d,
            sumToValue=self.geo.sumToValue,
        )

        sectionTwoViewChart = SectionTwoViewChart(
            p7=self.geo.params.p7,
            p3_e=self.geo.params.p3_e,
            p3_d=self.geo.params.p3_d,
            p11=self.geo.params.p11,
            c21_e=self.geo.params.c21_e,
            c21_d=self.geo.params.c21_d,
            c22_e=self.geo.params.c22_e,
            c22_d=self.geo.params.c22_d,
            c23_e=self.geo.params.c23_e,
            c23_d=self.geo.params.c23_d,
            c24_e=self.geo.params.c24_e,
            c24_d=self.geo.params.c24_d,
            sumToValue=self.geo.sumToValue,
        )

        tailViewChart = TailViewChart(
            p4_e=self.geo.params.p4_e,
            p4_d=self.geo.params.p4_d,
            p18=self.geo.params.p18,
            p19=self.geo.params.p19,
            p20=self.geo.params.p20_square if self.geo.data['tail_shape'] == 'Square' else self.geo.params.p20_V if self.geo.data['tail_shape'] == 'V' else self.geo.params.p20_pointed,
            c31=self.geo.params.c31,
            tailShape=self.geo.data['tail_shape'],
        )

        self.setCentralWidget(
            RowWidget(
                children=[
                    ColumnWidget(
                        children=[
                            TabWidget(
                                tabs=[
                                    TabItem(
                                        name='Body',
                                        item=ScrollWidget(
                                            children=[
                                                InputWidget(
                                                    title='l1:  ',
                                                    onChanged=self.controller.updateFloatValueWrapper(
                                                        key='l1',
                                                        func=self.geo.updateValue,
                                                    ),
                                                    initialValue=self.geo.data['l1'],
                                                ),
                                                InputWidget(
                                                    title='l2:  ',
                                                    onChanged=self.controller.updateFloatValueWrapper(
                                                        key='l2',
                                                        func=self.geo.updateValue,
                                                    ),
                                                    initialValue=self.geo.data['l2'],
                                                ),
                                                InputWidget(
                                                    title='l3:  ',
                                                    onChanged=self.controller.updateFloatValueWrapper(
                                                        key='l3',
                                                        func=self.geo.updateValue,
                                                    ),
                                                    initialValue=self.geo.data['l3'],
                                                ),
                                                InputWidget(
                                                    title='l4:  ',
                                                    onChanged=self.controller.updateFloatValueWrapper(
                                                        key='l4',
                                                        func=self.geo.updateValue,
                                                    ),
                                                    initialValue=self.geo.data['l4'],
                                                ),
                                                InputWidget(
                                                    title='l5:  ',
                                                    onChanged=self.controller.updateFloatValueWrapper(
                                                        key='l5',
                                                        func=self.geo.updateValue,
                                                    ),
                                                    initialValue=self.geo.data['l5'],
                                                ),
                                                InputWidget(
                                                    title='l6:  ',
                                                    onChanged=self.controller.updateFloatValueWrapper(
                                                        key='l6',
                                                        func=self.geo.updateValue,
                                                    ),
                                                    initialValue=self.geo.data['l6'],
                                                ),
                                                InputWidget(
                                                    title='l7:  ',
                                                    onChanged=self.controller.updateFloatValueWrapper(
                                                        key='l7',
                                                        func=self.geo.updateValue,
                                                    ),
                                                    initialValue=self.geo.data['l7'],
                                                ),
                                                InputWidget(
                                                    title='l8:  ',
                                                    onChanged=self.controller.updateFloatValueWrapper(
                                                        key='l8',
                                                        func=self.geo.updateValue,
                                                    ),
                                                    initialValue=self.geo.data['l8'],
                                                ),
                                                InputWidget(
                                                    title='l9:  ',
                                                    onChanged=self.controller.updateFloatValueWrapper(
                                                        key='l9',
                                                        func=self.geo.updateValue,
                                                    ),
                                                    initialValue=self.geo.data['l9'],
                                                ),
                                                InputWidget(
                                                    title='l10:',
                                                    onChanged=self.controller.updateFloatValueWrapper(
                                                        key='l10',
                                                        func=self.geo.updateValue,
                                                    ),
                                                    initialValue=self.geo.data['l10'],
                                                ),
                                                InputWidget(
                                                    title='l11:',
                                                    onChanged=self.controller.updateFloatValueWrapper(
                                                        key='l11',
                                                        func=self.geo.updateValue,
                                                    ),
                                                    initialValue=self.geo.data['l11'],
                                                ),
                                                InputWidget(
                                                    title='l12:',
                                                    onChanged=self.controller.updateFloatValueWrapper(
                                                        key='l12',
                                                        func=self.geo.updateValue,
                                                    ),
                                                    initialValue=self.geo.data['l12'],
                                                ),
                                            ]
                                        ),
                                    ),
                                    TabItem(
                                        name='Wing',
                                        item=ColumnWidget(
                                            children=[],
                                        ),
                                    ),
                                    TabItem(
                                        name='Tail',
                                        item=ScrollWidget(
                                            children=[
                                                QLabel('Shape:'),
                                                DropdownWidget(
                                                    title=None,
                                                    items=['Rouded', 'Pointed', 'Square', 'V'],
                                                    onChanged=self.controller.updateStringValueWrapper('tail_shape', self.geo.updateValue),
                                                    initialValue=self.geo.data['tail_shape']
                                                ),
                                                QLabel('Airfoil:'),
                                                InputWidget(
                                                    title='File:',
                                                    onChanged=self.controller.addTailFoil,
                                                ),
                                                QLabel('Parameters:'),
                                                InputWidget(
                                                    title='l16:',
                                                    onChanged=self.controller.updateFloatValueWrapper(
                                                        key='l16',
                                                        func=self.geo.updateValue,
                                                    ),
                                                    initialValue=self.geo.data['l16'],
                                                ),
                                                InputWidget(
                                                    title='l17:',
                                                    onChanged=self.controller.updateFloatValueWrapper(
                                                        key='l17',
                                                        func=self.geo.updateValue,
                                                    ),
                                                    initialValue=self.geo.data['l17'],
                                                ),
                                                InputWidget(
                                                    title='l18:',
                                                    onChanged=self.controller.updateFloatValueWrapper(
                                                        key='l18',
                                                        func=self.geo.updateValue,
                                                    ),
                                                    initialValue=self.geo.data['l18'],
                                                ),
                                                QLabel('Rotations:'),
                                                InputWidget(
                                                    title='x4:',
                                                    onChanged=self.controller.saveTailX4Rotation,
                                                    initialValue=0.0,
                                                ),
                                                InputWidget(
                                                    title='y4:',
                                                    onChanged=self.controller.saveTailY4Rotation,
                                                    initialValue=0.0,
                                                ),
                                                InputWidget(
                                                    title='z4:',
                                                    onChanged=self.controller.saveTailZ4Rotation,
                                                    initialValue=0.0,
                                                ),
                                                ButtonWidget(
                                                    title='Add Rotation',
                                                    onPressed=self.controller.tailApplyRotationWrapper(self.geo.addRotation, self.geo, tailViewChart.updateValues),
                                                )
                                            ]
                                        ),
                                    ),
                                    TabItem(
                                        name='Head',
                                        item=ColumnWidget(
                                            children=[],
                                        ),
                                    ),
                                ],
                                width=227,
                            ),
                            ButtonWidget(
                                title='Update',
                                onPressed=self.controller.updatePlotWrapper(
                                    geo=self.geo,
                                    topBody=topViewChart.updateValues,
                                    sideBody=sideViewChart.updateValues,
                                    secOneBody=sectionOneViewChart.updateValues,
                                    secTwoBody=sectionTwoViewChart.updateValues,
                                    tail=tailViewChart.updateValues,
                                ),
                                width=227
                            ),
                            ButtonWidget(
                                title='Save',
                                onPressed=self.controller.showSaveDialogWrapper(self.geo.save),
                                width=227
                            ),
                        ],
                        width=250,
                    ),
                    TabWidget(
                        tabs=[
                            TabItem(
                                name='Body',
                                item=RowWidget(
                                    children=[
                                        ColumnWidget(
                                            children=[
                                                topViewChart,
                                                sideViewChart,
                                            ]
                                        ),
                                        ColumnWidget(
                                            children=[
                                                sectionOneViewChart,
                                                sectionTwoViewChart,
                                            ]
                                        ),
                                    ],
                                    scale=[3, 1]
                                ),
                            ),
                            TabItem(
                                name='Wing',
                                item=ColumnWidget(
                                    children=[],
                                ),
                            ),
                            TabItem(
                                name='Tail',
                                item=tailViewChart,
                            ),
                            TabItem(
                                name='Head',
                                item=ColumnWidget(
                                    children=[],
                                ),
                            ),
                        ]
                    ),
                ],
                scale=[1, 4],
            )
        )

############################################################
# External
############################################################
class UI:

    def __init__(self, geo) -> None:
        self.geo = geo
        return
    
    def show(self) -> None:
        app = QApplication(sys.argv)
        main = _MainWindow(self.geo)
        main.show()
        sys.exit(app.exec_())
        return