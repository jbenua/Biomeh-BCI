# -*- coding: utf-8 -*-
"""
This example demonstrates many of the 2D plotting capabilities
in pyqtgraph. All of the plots may be panned/scaled by dragging with 
the left/right mouse buttons. Right click on any plot to show a context menu.
"""
from PyQt5.QtWidgets import QApplication
import numpy as np
import pyqtgraph as pg

app = QApplication([])
win = pg.GraphicsWindow(title="Basic plotting examples")
win.setWindowTitle('pyqtgraph example: Plotting')

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)

p2 = win.addPlot(title="Multiple curves")
a = np.random.normal(size=100)
b = np.random.normal(size=110) + 5
c = np.random.normal(size=120) + 10
p2.plot(a, pen=(100, 100, 255, 50), name="Red curve")
p2.plot(b, pen=(100, 100, 255, 50), name="Green curve")
p2.plot(c, pen=(100, 100, 255, 50), name="Blue curve")


p2.plot(a, pen=(100, 100, 255, 50), name="Red curve")
p2.plot(a, pen=(100, 100, 255, 50), name="Red curve")
p2.plot(b, pen=(100, 100, 255, 50), name="Green curve")

p2.showGrid(x=True)


p3 = win.addPlot(title="Multiple curves")
a = np.random.normal(size=100)
b = np.random.normal(size=110) + 5
c = np.random.normal(size=120) + 10
p3.plot(a, pen=(100, 100, 255, 50), name="Red curve")
p3.plot(b, pen=(100, 100, 255, 50), name="Green curve")
p3.plot(c, pen=(100, 100, 255, 50), name="Blue curve")


p3.plot(a, pen=(100, 100, 255, 50), name="Red curve")
p3.plot(a, pen=(100, 100, 255, 50), name="Red curve")
p3.plot(b, pen=(100, 100, 255, 50), name="Green curve")

p3.showGrid(x=True)




## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1):
       QApplication.instance().exec_()
