import sys
import math
from PyQt5.QtWidgets import QApplication
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg

from moed.model import Model
from moed.io import IO

def window():
    app = QApplication(sys.argv)

    win = pg.GraphicsWindow(title="Test")
    win.resize(1000,600)
    win.setWindowTitle("test")
    pg.setConfigOption('background', 'k')
    pg.setConfigOption('foreground', 'w')
    pg.setConfigOptions(antialias=True)

    x = range(1, 1001, 1)
    a = 0.5
    b = 3
    alpha = 0.005
    beta = 1

    y1 = Model.linear(x, a, b)
    p1 = win.addPlot(title="1", y=y1)

    y2 = Model.linear(x, -a, b)
    p2 = win.addPlot(title="2", y=y2)

    win.nextRow()

    y3 = Model.exponential(x, alpha, beta)
    p3 = win.addPlot(title="3", y=y3)

    y4 = Model.exponential(x, -alpha, beta)
    p4 = win.addPlot(title="4", y=y4)

    win.nextRow()
    y5 = [*y1[:500], *y2[500:750], *y3[750:1001]]
    p5 = win.addPlot(title="5", y=y5)


    sys.exit(app.exec_())

if __name__ == '__main__':
   window()
