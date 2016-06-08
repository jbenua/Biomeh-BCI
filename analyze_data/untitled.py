# -*- coding: utf-8 -*-
"""
This example demonstrates many of the 2D plotting capabilities
in pyqtgraph. All of the plots may be panned/scaled by dragging with 
the left/right mouse buttons. Right click on any plot to show a context menu.
"""
from PyQt5.QtWidgets import QApplication
import numpy as np
import pyqtgraph as pg
SENSORS = {
    'f3': {
        'color': (0, 0, 255),
        'item': 'check_f3',
    },
    'fc6': {
        'color': (0, 255, 255),
        'item': 'check_fc6',
    },
    'p7': {
        'color': (0, 0, 128),
        'item': 'check_p7',
    },
    't8': {
        'color': (64, 0, 0),
        'item': 'check_t8',
    },
    'f7': {
        'color': (128, 128, 0),
        'item': 'check_f7',
    },
    'f8': {
        'color': (255, 255, 0),
        'item': 'check_f8',
    },
    't7': {
        'color': (0, 128, 0),
        'item': 'check_t7',
    },
    'p8': {
        'color': (255, 0, 0),
        'item': 'check_p8',
    },
    'af4': {
        'color': (128, 0, 128),
        'item': 'check_af4',
    },
    'f4': {
        'color': (0, 64, 0),
        'item': 'check_f4',
    },
    'af3': {
        'color': (128, 0, 0),
        'item': 'check_af3',
    },
    'o2': {
        'color': (0, 0, 64),
        'item': 'check_o2',
    },
    'o1': {
        'color': (255, 0, 255),
        'item': 'check_o1',
    },
    'fc5': {
        'color': (64, 64, 0),
        'item': 'check_fc5',
    },
    'x': {
        'color': (0, 128, 128),
        'item': 'check_x',
    },
    'y': {
        'color': (64, 0, 64),
        'item': 'check_y',
    },
    'unknown': {
        'color': (0, 255, 0),
        'item': 'check_un'
    }
}

app = QApplication([])
win = pg.GraphicsWindow(title="Basic plotting examples")
win.setWindowTitle('pyqtgraph example: Plotting')

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)


from b_data import data
from m_data import data as data1
from j_data import data as data2
from l_data import data as data3
from s_data import data as data4

datas = [data, data1, data2, data3, data4]

for d in datas:
    p1 = win.addPlot(title="first test")
    for key in d:
        p1.plot(np.array(d[key]), pen=SENSORS[key]['color'], name="curve")
    win.nextRow()

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1):
       QApplication.instance().exec_()
