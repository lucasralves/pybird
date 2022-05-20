from PyQt5.QtWidgets import QWidget, QVBoxLayout

import matplotlib.pyplot as plt
import matplotlib.transforms as trans
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backend_bases import MouseButton
from matplotlib.path import Path
import matplotlib.patches as patches
from numpy import arccos, asarray
from numpy.linalg import norm
from math import pi

from pybird.geometry.geometry import Geometry

class TopChartWidget(QWidget):

    def __init__(self, geo: Geometry):
        super().__init__()

        self.geo = geo

        self.id = None
        self.fig, self.ax = plt.subplots(1,1,sharex=True)
        self.ax.set_aspect("equal")

        self.update()

        self.fig.canvas.mpl_connect('motion_notify_event', self.on_move)
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
  
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)

        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.allow = [8, 9, 10, 11, 12, 13, 14, 15, 26, 18, 29, 31, 32, 23, 35, 19, 24]

        return
    
    def update(self) -> None:
        print('update')
        self.vertices = asarray([
            # Body
            self.geo.params.p1_e, # 0
            self.geo.params.p2_e, # 1
            self.geo.params.p3_e, # 2
            self.geo.params.p4_e, # 3
            self.geo.params.p1_d, # 4
            self.geo.params.p2_d, # 5
            self.geo.params.p3_d, # 6
            self.geo.params.p4_d, # 7
            self.geo.params.c1_e, # 8
            self.geo.params.c2_e, # 9
            self.geo.params.c3_e, # 10
            self.geo.params.c4_e, # 11
            self.geo.params.c1_d, # 12
            self.geo.params.c2_d, # 13
            self.geo.params.c3_d, # 14
            self.geo.params.c4_d, # 15

            # Wing
            self.geo.params.p13_e, # 16
            self.geo.params.p14_e, # 17
            self.geo.params.p15_e, # 18
            self.geo.params.p16_e, # 19
            self.geo.params.p17_e, # 20
            self.geo.params.p13_d, # 21
            self.geo.params.p14_d, # 22
            self.geo.params.p15_d, # 23
            self.geo.params.p16_d, # 24
            self.geo.params.p17_d, # 25
            self.geo.params.c25_e, # 26
            self.geo.params.c26_e, # 27
            self.geo.params.c27_e, # 28
            self.geo.params.c28_e, # 29
            self.geo.params.c29_e, # 30
            self.geo.params.c30_e, # 31
            self.geo.params.c25_d, # 32
            self.geo.params.c26_d, # 33
            self.geo.params.c27_d, # 34
            self.geo.params.c28_d, # 35
            self.geo.params.c29_d, # 36
            self.geo.params.c30_d, # 37

            # Tail
            self.geo.params.p18, # 38
            self.geo.params.p19, # 39
            self.geo.params.p20_pointed if self.geo.data['tail_shape'] == 'Pointed' else self.geo.params.p20_rounded if self.geo.data['tail_shape'] == 'Rounded' else self.geo.params.p20_V if self.geo.data['tail_shape'] == 'V' else self.geo.params.p20_square, # 40
            self.geo.params.c31, # 41

            # Head
            self.geo.params.p21_e, # 42
            self.geo.params.p23,   # 43
            self.geo.params.p21_d, # 44
            self.geo.params.c32,   # 45
        ])
        self.plot()
        return

    def plot(self):

        self.fig.clear()
        self.ax = self.fig.add_subplot()
        self.ax.set_aspect("equal")
        self.fig.subplots_adjust(bottom=0.05, right=0.99, top=0.95, left=0.1)

        base = plt.gca().transData
        rot = trans.Affine2D().rotate_deg(90)

        # Bezier curves
        # Body
        path = Path(
            [self.vertices[0][:2], self.vertices[8][:2], self.vertices[9][:2], self.vertices[1][:2]],
            [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
        )
        patch = patches.PathPatch(path, facecolor='none', lw=2, transform=rot+base)
        self.ax.add_patch(patch)
        self.ax.plot([self.vertices[0][0], self.vertices[8][0], self.vertices[9][0], self.vertices[1][0]], [self.vertices[0][1], self.vertices[8][1], self.vertices[9][1], self.vertices[1][1]], '--', lw=1, color='grey', ms=10, transform=rot+base)
        
        path = Path(
            [self.vertices[2][:2], self.vertices[10][:2], self.vertices[11][:2], self.vertices[3][:2]],
            [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
        )
        patch = patches.PathPatch(path, facecolor='none', lw=2, transform=rot+base)
        self.ax.add_patch(patch)
        self.ax.plot([self.vertices[2][0], self.vertices[10][0], self.vertices[11][0], self.vertices[3][0]], [self.vertices[2][1], self.vertices[10][1], self.vertices[11][1], self.vertices[3][1]], '--', lw=1, color='grey', ms=10, transform=rot+base)
        
        path = Path(
            [self.vertices[4][:2], self.vertices[12][:2], self.vertices[13][:2], self.vertices[5][:2]],
            [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
        )
        patch = patches.PathPatch(path, facecolor='none', lw=2, transform=rot+base)
        self.ax.add_patch(patch)
        self.ax.plot([self.vertices[4][0], self.vertices[12][0], self.vertices[13][0], self.vertices[5][0]], [self.vertices[4][1], self.vertices[12][1], self.vertices[13][1], self.vertices[5][1]], '--', lw=1, color='grey', ms=10, transform=rot+base)
        
        path = Path(
            [self.vertices[6][:2], self.vertices[14][:2], self.vertices[15][:2], self.vertices[7][:2]],
            [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
        )
        patch = patches.PathPatch(path, facecolor='none', lw=2, transform=rot+base)
        self.ax.add_patch(patch)
        self.ax.plot([self.vertices[6][0], self.vertices[14][0], self.vertices[15][0], self.vertices[7][0]], [self.vertices[6][1], self.vertices[14][1], self.vertices[15][1], self.vertices[7][1]], '--', lw=1, color='grey', ms=10, transform=rot+base)
        
        # Tail
        if self.geo.data['tail_shape'] == 'Pointed' or self.geo.data['tail_shape'] == 'V' or self.geo.data['tail_shape'] == 'Square':
            path = Path(
                [self.vertices[3, :2], self.vertices[38, :2], self.vertices[40, :2], self.vertices[39, :2], self.vertices[7, :2]],
                [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.LINETO]
            )
            patch = patches.PathPatch(path, facecolor='none', lw=2, transform=rot+base)
            self.ax.add_patch(patch)
        else:
            # Arc
            v1 = self.vertices[38, :] - self.vertices[41, :]
            v2 = self.vertices[39, :] - self.vertices[41, :]
            radius = norm(v1)
            angle = arccos((v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]) / (radius * radius)) * 180 / pi
            diameter = 2 * radius
            patch = patches.Arc((self.vertices[41, 0], self.vertices[41, 1]), diameter, diameter, angle=180, theta1=-angle / 2, theta2=angle / 2, facecolor='none', lw=2, transform=rot+base)
            self.ax.add_patch(patch)

            # Lines
            path = Path(
                [self.vertices[3, :2], self.vertices[38, :2]],
                [Path.MOVETO, Path.LINETO]
            )
            patch = patches.PathPatch(path, facecolor='none', lw=2, transform=rot+base)
            self.ax.add_patch(patch)
            path = Path(
                [self.vertices[7, :2], self.vertices[39, :2]],
                [Path.MOVETO, Path.LINETO]
            )
            patch = patches.PathPatch(path, facecolor='none', lw=2, transform=rot+base)
            self.ax.add_patch(patch)
        
        # Head
        v1 = self.vertices[43, :] - self.vertices[45, :]
        v2 = self.vertices[42, :] - self.vertices[45, :]
        v3 = self.vertices[0, :] - self.vertices[45, :]
        angle1 = arccos((v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]) / (norm(v1) * norm(v2))) * 180 / pi
        angle2 = arccos((v3[0] * v2[0] + v3[1] * v2[1] + v3[2] * v2[2]) / (norm(v3) * norm(v2))) * 180 / pi

        diameter = self.geo.data['l20']
        patch = patches.Arc((self.vertices[45, 0], self.vertices[45, 1]), diameter, diameter, angle=0, theta1=angle1, theta2=angle1+angle2, facecolor='none', lw=2, transform=rot+base)
        self.ax.add_patch(patch)
        patch = patches.Arc((self.vertices[45, 0], self.vertices[45, 1]), diameter, diameter, angle=0, theta1=-angle1-angle2, theta2=-angle1, facecolor='none', lw=2, transform=rot+base)
        self.ax.add_patch(patch)

        path = Path(
            [self.vertices[42, :2], self.vertices[43, :2], self.vertices[44, :2]],
            [Path.MOVETO, Path.LINETO, Path.LINETO]
        )
        patch = patches.PathPatch(path, facecolor='none', lw=2, transform=rot+base)
        self.ax.add_patch(patch)

        # Wing
        path = Path(
            [self.vertices[1][:2], self.vertices[26][:2], self.vertices[16][:2]],
            [Path.MOVETO, Path.CURVE3, Path.CURVE3]
        )
        patch = patches.PathPatch(path, facecolor='none', lw=2, transform=rot+base)
        self.ax.add_patch(patch)
        self.ax.plot([self.vertices[1][0], self.vertices[26][0], self.vertices[16][0]], [self.vertices[1][1], self.vertices[26][1], self.vertices[16][1]], '--', lw=1, color='grey', ms=10, transform=rot+base)
        
        path = Path(
            [self.vertices[16][:2], self.vertices[27][:2], self.vertices[17][:2]],
            [Path.MOVETO, Path.CURVE3, Path.CURVE3]
        )
        patch = patches.PathPatch(path, facecolor='none', lw=2, transform=rot+base)
        self.ax.add_patch(patch)
        self.ax.plot([self.vertices[16][0], self.vertices[27][0], self.vertices[17][0]], [self.vertices[16][1], self.vertices[27][1], self.vertices[17][1]], '--', lw=1, color='grey', ms=10, transform=rot+base)
        
        path = Path(
            [self.vertices[17][:2], self.vertices[28][:2], self.vertices[18][:2]],
            [Path.MOVETO, Path.CURVE3, Path.CURVE3]
        )
        patch = patches.PathPatch(path, facecolor='none', lw=2, transform=rot+base)
        self.ax.add_patch(patch)
        self.ax.plot([self.vertices[17][0], self.vertices[28][0], self.vertices[18][0]], [self.vertices[17][1], self.vertices[28][1], self.vertices[18][1]], '--', lw=1, color='grey', ms=10, transform=rot+base)
        
        path = Path(
            [self.vertices[18][:2], self.vertices[29][:2], self.vertices[19][:2]],
            [Path.MOVETO, Path.CURVE3, Path.CURVE3]
        )
        patch = patches.PathPatch(path, facecolor='none', lw=2, transform=rot+base)
        self.ax.add_patch(patch)
        self.ax.plot([self.vertices[18][0], self.vertices[29][0], self.vertices[19][0]], [self.vertices[18][1], self.vertices[29][1], self.vertices[19][1]], '--', lw=1, color='grey', ms=10, transform=rot+base)
        
        path = Path(
            [self.vertices[19][:2], self.vertices[30][:2], self.vertices[20][:2]],
            [Path.MOVETO, Path.CURVE3, Path.CURVE3]
        )
        patch = patches.PathPatch(path, facecolor='none', lw=2, transform=rot+base)
        self.ax.add_patch(patch)
        self.ax.plot([self.vertices[19][0], self.vertices[30][0], self.vertices[20][0]], [self.vertices[19][1], self.vertices[30][1], self.vertices[20][1]], '--', lw=1, color='grey', ms=10, transform=rot+base)
        
        path = Path(
            [self.vertices[20][:2], self.vertices[31][:2], self.vertices[2][:2]],
            [Path.MOVETO, Path.CURVE3, Path.CURVE3]
        )
        patch = patches.PathPatch(path, facecolor='none', lw=2, transform=rot+base)
        self.ax.add_patch(patch)
        self.ax.plot([self.vertices[20][0], self.vertices[31][0], self.vertices[2][0]], [self.vertices[20][1], self.vertices[31][1], self.vertices[2][1]], '--', lw=1, color='grey', ms=10, transform=rot+base)
        
        path = Path(
            [self.vertices[5][:2], self.vertices[32][:2], self.vertices[21][:2]],
            [Path.MOVETO, Path.CURVE3, Path.CURVE3]
        )
        patch = patches.PathPatch(path, facecolor='none', lw=2, transform=rot+base)
        self.ax.add_patch(patch)
        self.ax.plot([self.vertices[5][0], self.vertices[32][0], self.vertices[21][0]], [self.vertices[5][1], self.vertices[32][1], self.vertices[21][1]], '--', lw=1, color='grey', ms=10, transform=rot+base)
        
        path = Path(
            [self.vertices[21][:2], self.vertices[33][:2], self.vertices[22][:2]],
            [Path.MOVETO, Path.CURVE3, Path.CURVE3]
        )
        patch = patches.PathPatch(path, facecolor='none', lw=2, transform=rot+base)
        self.ax.add_patch(patch)
        self.ax.plot([self.vertices[21][0], self.vertices[33][0], self.vertices[22][0]], [self.vertices[21][1], self.vertices[33][1], self.vertices[22][1]], '--', lw=1, color='grey', ms=10, transform=rot+base)
        
        path = Path(
            [self.vertices[20][:2], self.vertices[31][:2], self.vertices[2][:2]],
            [Path.MOVETO, Path.CURVE3, Path.CURVE3]
        )
        patch = patches.PathPatch(path, facecolor='none', lw=2, transform=rot+base)
        self.ax.add_patch(patch)
        self.ax.plot([self.vertices[20][0], self.vertices[31][0], self.vertices[2][0]], [self.vertices[20][1], self.vertices[31][1], self.vertices[2][1]], '--', lw=1, color='grey', ms=10, transform=rot+base)
        
        path = Path(
            [self.vertices[22][:2], self.vertices[34][:2], self.vertices[23][:2]],
            [Path.MOVETO, Path.CURVE3, Path.CURVE3]
        )
        patch = patches.PathPatch(path, facecolor='none', lw=2, transform=rot+base)
        self.ax.add_patch(patch)
        self.ax.plot([self.vertices[22][0], self.vertices[34][0], self.vertices[23][0]], [self.vertices[22][1], self.vertices[34][1], self.vertices[23][1]], '--', lw=1, color='grey', ms=10, transform=rot+base)
        
        path = Path(
            [self.vertices[23][:2], self.vertices[35][:2], self.vertices[24][:2]],
            [Path.MOVETO, Path.CURVE3, Path.CURVE3]
        )
        patch = patches.PathPatch(path, facecolor='none', lw=2, transform=rot+base)
        self.ax.add_patch(patch)
        self.ax.plot([self.vertices[23][0], self.vertices[35][0], self.vertices[24][0]], [self.vertices[23][1], self.vertices[35][1], self.vertices[24][1]], '--', lw=1, color='grey', ms=10, transform=rot+base)
        
        path = Path(
            [self.vertices[24][:2], self.vertices[36][:2], self.vertices[25][:2]],
            [Path.MOVETO, Path.CURVE3, Path.CURVE3]
        )
        patch = patches.PathPatch(path, facecolor='none', lw=2, transform=rot+base)
        self.ax.add_patch(patch)
        self.ax.plot([self.vertices[24][0], self.vertices[36][0], self.vertices[25][0]], [self.vertices[24][1], self.vertices[36][1], self.vertices[25][1]], '--', lw=1, color='grey', ms=10, transform=rot+base)
        
        path = Path(
            [self.vertices[25][:2], self.vertices[37][:2], self.vertices[6][:2]],
            [Path.MOVETO, Path.CURVE3, Path.CURVE3]
        )
        patch = patches.PathPatch(path, facecolor='none', lw=2, transform=rot+base)
        self.ax.add_patch(patch)
        self.ax.plot([self.vertices[25][0], self.vertices[37][0], self.vertices[6][0]], [self.vertices[25][1], self.vertices[37][1], self.vertices[6][1]], '--', lw=1, color='grey', ms=10, transform=rot+base)

        # Plot points
        # Body
        self.ax.scatter(self.vertices[0:8, 0], self.vertices[0:8, 1], color='green', transform=rot+base)
        self.ax.scatter(self.vertices[8:16, 0], self.vertices[8:16, 1], color='red', transform=rot+base)
        # # Wing
        self.ax.scatter(self.vertices[16:26, 0], self.vertices[16:26, 1], color='green', transform=rot+base)
        self.ax.scatter(self.vertices[26:38, 0], self.vertices[26:38, 1], color='red', transform=rot+base)
        # # Tail
        self.ax.scatter(self.vertices[38:41, 0], self.vertices[38:41, 1], color='green', transform=rot+base)
        if self.geo.data['tail_shape'] == 'Rounded': self.ax.scatter(self.vertices[41, 0], self.vertices[41, 1], color='red', transform=rot+base)
        # # Head
        self.ax.scatter(self.vertices[42:45, 0], self.vertices[42:45, 1], color='green', transform=rot+base)
        self.ax.scatter(self.vertices[45, 0], self.vertices[45, 1], color='red', transform=rot+base)

        self.ax.grid()
        self.fig.canvas.draw()

        return
    
    def find_point_id(self, x: float, y: float) -> int:
        x_new = y
        y_new = -x
        for i in range(len(self.vertices)):
            if -8e-3 < (x_new - self.vertices[i][0]) < 8e-3 and -8e-3 < (y_new - self.vertices[i][1]) < 8e-3:
                print(i)
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
            dx = -(self.vertices[self.id][0] - event.ydata)
            dy = -(self.vertices[self.id][1] + event.xdata)

            # Body
            if self.id in [8, 9, 10, 11, 12, 13, 14, 15]:
                if self.id in [8, 9, 10, 11]:
                    sym_id = self.id + 4
                else:
                    sym_id = self.id - 4
                self.vertices[self.id] = [self.vertices[self.id][0] + dx, self.vertices[self.id][1] + dy, self.vertices[self.id][2]]
                self.vertices[sym_id] = [self.vertices[sym_id][0] + dx, self.vertices[sym_id][1] - dy, self.vertices[sym_id][2]]

                if self.id == 15:
                    self.geo.sumToValue('delta7', dx)
                    self.geo.sumToValue('delta8', -dy)

                if self.id == 14:
                    self.geo.sumToValue('delta5', dx)
                    self.geo.sumToValue('delta6', -dy)

                if self.id == 13:
                    self.geo.sumToValue('delta3', dx)
                    self.geo.sumToValue('delta4', -dy)

                if self.id == 12:
                    self.geo.sumToValue('delta1', dx)
                    self.geo.sumToValue('delta2', -dy)

                if self.id == 11:
                    self.geo.sumToValue('delta7', dx)
                    self.geo.sumToValue('delta8', dy)

                if self.id == 10:
                    self.geo.sumToValue('delta5', dx)
                    self.geo.sumToValue('delta6', dy)

                if self.id == 9:
                    self.geo.sumToValue('delta3', dx)
                    self.geo.sumToValue('delta4', dy)

                if self.id == 8:
                    self.geo.sumToValue('delta1', dx)
                    self.geo.sumToValue('delta2', dy)

            # Wing
            if self.id == 19 or self.id == 24:
                x3_e = asarray(self.geo.data['x3_left'])
                x2_e = asarray(self.geo.data['x2_tip_left'])
                x_e = ((x2_e + x3_e) / norm(x2_e + x3_e))
                x3_d = asarray(self.geo.data['x3_right'])
                x2_d = asarray(self.geo.data['x2_tip_right'])
                x_d = ((x2_d + x3_d) / norm(x2_d + x3_d))
                
                if self.id == 25:
                    delta52_inc = -(x_e[0] * dx + x_e[1] * dy)
                else:
                    delta52_inc = -(x_d[0] * dx + x_d[1] * dy)
                
                self.vertices[19] = [self.vertices[19][0] - delta52_inc * x_e[0], self.vertices[19][1] - delta52_inc * x_e[1], self.vertices[19][2]]
                self.vertices[24] = [self.vertices[24][0] - delta52_inc * x_d[0], self.vertices[24][1] - delta52_inc * x_d[1], self.vertices[24][2]]

                self.vertices[20] = [self.vertices[20][0] - delta52_inc * x_e[0], self.vertices[20][1] - delta52_inc * x_e[1], self.vertices[20][2]]
                self.vertices[25] = [self.vertices[25][0] - delta52_inc * x_d[0], self.vertices[25][1] - delta52_inc * x_d[1], self.vertices[25][2]]

                self.vertices[30] = [0.5 * (self.vertices[19][0] + self.vertices[20][0]), 0.5 * (self.vertices[19][1] + self.vertices[20][1]), 0.5 * (self.vertices[19][2] + self.vertices[20][2])]
                self.vertices[36] = [0.5 * (self.vertices[24][0] + self.vertices[25][0]), 0.5 * (self.vertices[24][1] + self.vertices[25][1]), 0.5 * (self.vertices[24][2] + self.vertices[25][2])]

            if self.id == 26 or self.id == 32:

                x1_e = asarray(self.geo.data['x1_left'])
                x2_e = asarray(self.geo.data['x2_base_left'])
                x_e = (x1_e + x2_e) / norm(x1_e + x2_e)

                x1_d = asarray(self.geo.data['x1_right'])
                x2_d = asarray(self.geo.data['x2_base_right'])
                x_d = (x1_d + x2_d) / norm(x1_d + x2_d)
            
                if self.id == 26:
                    delta53_inc = x_e[0] * dx + x_e[1] * dy
                else:
                    delta53_inc = x_d[0] * dx + x_d[1] * dy
                
                self.vertices[26] = [self.vertices[26][0] + delta53_inc * x_e[0], self.vertices[26][1] + delta53_inc * x_e[1], self.vertices[26][2]]
                self.vertices[32] = [self.vertices[32][0] + delta53_inc * x_d[0], self.vertices[32][1] + delta53_inc * x_d[1], self.vertices[32][2]]

                self.geo.sumToValue('delta53', delta53_inc)

            if self.id == 18 or self.id == 23:

                x3_e = asarray(self.geo.data['x3_left'])
                x3_d = asarray(self.geo.data['x3_right'])
                y3_e = asarray(self.geo.data['y3_left'])
                y3_d = asarray(self.geo.data['y3_right'])

                if self.id == 18:
                    delta51_inc = -(x3_e[0] * dx + x3_e[1] * dy)
                    delta50_inc = (y3_e[0] * dx + y3_e[1] * dy)
                else:
                    delta51_inc = -(x3_d[0] * dx + x3_d[1] * dy)
                    delta50_inc = -(y3_d[0] * dx + y3_d[1] * dy)
                
                self.vertices[18] = [self.vertices[18][0] - delta51_inc * x3_e[0] + delta50_inc * y3_e[0], self.vertices[18][1] - delta51_inc * x3_e[1] + delta50_inc * y3_e[1], self.vertices[18][2]]
                self.vertices[23] = [self.vertices[23][0] - delta51_inc * x3_d[0] - delta50_inc * y3_d[0], self.vertices[23][1] - delta51_inc * x3_d[1] - delta50_inc * y3_d[1], self.vertices[23][2]]

                self.geo.sumToValue('delta51', delta51_inc)
                self.geo.sumToValue('delta50', delta50_inc)

            if self.id == 29 or self.id == 35:

                x3_e = asarray(self.geo.data['x3_left'])
                y3_e = asarray(self.geo.data['y3_left'])
                x3_d = asarray(self.geo.data['x3_right'])
                y3_d = asarray(self.geo.data['y3_right'])

                if self.id == 29:
                    delta55_inc = x3_e[0] * dx + x3_e[1] * dy
                    delta56_inc = y3_e[0] * dx + y3_e[1] * dy
                else:
                    delta55_inc = x3_d[0] * dx + x3_d[1] * dy
                    delta56_inc = -(y3_d[0] * dx + y3_d[1] * dy)
                
                self.vertices[29] = [self.vertices[29][0] + delta55_inc * x3_e[0] + delta56_inc * y3_e[0], self.vertices[29][1] + delta55_inc * x3_e[1] + delta56_inc * y3_e[1], self.vertices[29][2]]
                self.vertices[35] = [self.vertices[35][0] + delta55_inc * x3_d[0] - delta56_inc * y3_d[0], self.vertices[35][1] + delta55_inc * x3_d[1] - delta56_inc * y3_d[1], self.vertices[35][2]]
                
                self.geo.sumToValue('delta55', delta55_inc)
                self.geo.sumToValue('delta56', delta56_inc)

            if self.id == 31 or self.id == 37:

                x1_e = asarray(self.geo.data['x1_left'])
                x2_e = asarray(self.geo.data['x2_base_left'])
                y1_e = asarray(self.geo.data['y1_left'])
                y2_e = asarray(self.geo.data['y2_left'])
                x_e = (x1_e + x2_e) / norm(x1_e + x2_e)
                y_e = (y1_e + y2_e) / norm(y1_e + y2_e)

                x1_d = asarray(self.geo.data['x1_right'])
                x2_d = asarray(self.geo.data['x2_base_right'])
                y1_d = asarray(self.geo.data['y1_right'])
                y2_d = asarray(self.geo.data['y2_right'])
                x_d = (x1_d + x2_d) / norm(x1_d + x2_d)
                y_d = (y1_d + y2_d) / norm(y1_d + y2_d)
            
                if self.id == 31:
                    delta58_inc = x_e[0] * dx + x_e[1] * dy
                    delta59_inc = y_e[0] * dx + y_e[1] * dy
                else:
                    delta58_inc = x_d[0] * dx + x_d[1] * dy
                    delta59_inc = -(y_d[0] * dx + y_d[1] * dy)
                
                self.vertices[31] = [self.vertices[31][0] + delta58_inc * x_e[0] + delta59_inc * y_e[0], self.vertices[31][1] + delta58_inc * x_e[1] + delta59_inc * y_e[1], self.vertices[31][2]]
                self.vertices[37] = [self.vertices[37][0] + delta58_inc * x_d[0] - delta59_inc * y_d[0], self.vertices[37][1] + delta58_inc * x_d[1] - delta59_inc * y_d[1], self.vertices[37][2]]

                self.geo.sumToValue('delta58', delta58_inc)
                self.geo.sumToValue('delta59', delta59_inc)

            self.plot()
        return