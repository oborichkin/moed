import sys
import math
from PyQt5.QtWidgets import QApplication
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg

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
    y1 = [a*t + b for t in x]
    p1 = win.addPlot(title="1", y=y1)

    a = -a
    y2 = [a*t + b for t in x]
    p2 = win.addPlot(title="2", y=y2)

    win.nextRow()

    alpha = 0.005
    beta = 1
    y3 = [beta * math.e ** (alpha * t) for t in x]
    p3 = win.addPlot(title="3", y=y3)

    alpha = -alpha
    y4 = [beta * math.e ** (alpha * t) for t in x]
    p4 = win.addPlot(title="4", y=y4)

    win.nextRow()
    y5 = [*y1[:500], *y2[500:750], *y3[750:1001]]
    p5 = win.addPlot(title="5", y=y5)


    sys.exit(app.exec_())

if __name__ == '__main__':
   window()