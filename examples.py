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


# p2 = win.addPlot(title="Multiple curves")
# a = np.random.normal(size=100)
# b = np.random.normal(size=110) + 5
# c = np.random.normal(size=120) + 10
# p2.plot(a, pen=(100, 100, 255, 50), name="Red curve")
# p2.plot(b, pen=(100, 100, 255, 50), name="Green curve")
# p2.plot(c, pen=(100, 100, 255, 50), name="Blue curve")


# p2.plot(a, pen=(100, 100, 255, 50), name="Red curve")
# p2.plot(a, pen=(100, 100, 255, 50), name="Red curve")
# p2.plot(b, pen=(100, 100, 255, 50), name="Green curve")

# p2.showGrid(x=True)


# p3 = win.addPlot(title="Multiple curves")
# a = np.random.normal(size=100)
# b = np.random.normal(size=110) + 5
# c = np.random.normal(size=120) + 10
# p3.plot(a, pen=(100, 100, 255, 50), name="Red curve")
# p3.plot(b, pen=(100, 100, 255, 50), name="Green curve")
# p3.plot(c, pen=(100, 100, 255, 50), name="Blue curve")


# p3.plot(a, pen=(100, 100, 255, 50), name="Red curve")
# p3.plot(a, pen=(100, 100, 255, 50), name="Red curve")
# p3.plot(b, pen=(100, 100, 255, 50), name="Green curve")

# p3.showGrid(x=True)


from b_data import data  # 2100 - ...
from m_data import data as data1  # 2400 - ...
from j_data import data as data2 # 3900 - 5300
from l_data import data as data3  # 4200 - 4600
from s_data1 import data as data5  # 2760 - 3500
 
datas = [
    (data, 2200, 2600, (255, 255, 0)),
    (data1, 2420, 2820, (0, 255, 255)),
    (data2, 4000, 4400, (255, 0, 255)),
    (data3, 4150, 4550, (255, 0, 0)),
    (data5, 2895, 3295, (0, 255, 0))
]
plots = {}

row = 0
for key in datas[0][0]:
    if key == 'unknown':
        plot = win.addPlot(title=key)
        if row > 1:
            win.nextRow()
            row = 0
        else:
            row += 1
        plots[key] = plot
for d, rangea, rangeb, color in datas:
    for key in d:
        if key == 'unknown':
            plots[key].plot(np.array(d[key][rangea:rangeb]), pen=color, name="curve")


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1):
       QApplication.instance().exec_()
