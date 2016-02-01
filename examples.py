import pyqtgraph.examples
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg

pyqtgraph.examples.run()

win = pg.GraphicsWindow()
win.setWindowTitle('pyqtgraph example: Scrolling Plots')

p4 = win.addPlot()
p4.setDownsampling(mode='peak')
p4.setClipToView(True)
curve_b = p4.plot(pen=(0, 0, 255))
curve_g = p4.plot(pen=(0, 255, 0))
curve_r = p4.plot(pen=(255, 0, 0))

data_b = np.empty(100)
data_g = np.empty(100)
data_r = np.empty(100)
ptr3 = 0

p4.setXRange(-200, 0)


def update():
    global data_b, data_g, data_r, ptr3
    data_b[ptr3] = np.random.normal()
    data_g[ptr3] = np.random.normal()+5
    data_r[ptr3] = np.random.normal()+10
    ptr3 += 1
    if ptr3 >= data_b.shape[0]:
        tmp = data_b
        data_b = np.empty(data_b.shape[0] * 2)
        data_b[:tmp.shape[0]] = tmp
        tmp = data_g
        data_g = np.empty(data_g.shape[0] * 2)
        data_g[:tmp.shape[0]] = tmp
        tmp = data_r
        data_r = np.empty(data_r.shape[0] * 2)
        data_r[:tmp.shape[0]] = tmp
    curve_b.setData(data_b[:ptr3])
    curve_g.setData(data_g[:ptr3])
    curve_r.setData(data_r[:ptr3])
    p4.setXRange(ptr3-200, ptr3)


timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)


if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
