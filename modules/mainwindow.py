from PyQt4 import uic
from PyQt4.QtGui import QMainWindow, QPixmap
from PyQt4.QtCore import QObject, SIGNAL

from .login import LoginDialog
import numpy as np
import pyqtgraph as pg
import sys

MAINWINDOW_UI = './ui/main_window.ui'
GO_LEFT_PIC = './img/go_left.png'
GO_RIGHT_PIC = './img/go_right.png'

SENSORS = {
    'f3': (0, 0, 255),
    'fc6': (0, 255, 255),
    'p7': (0, 0, 128),
    't8': (64, 0, 0),
    'f7': (128, 128, 0),
    'f8': (255, 255, 0),
    't7': (0, 128, 0),
    'p8': (255, 0, 0),
    'af4': (128, 0, 128),
    'f4': (0, 64, 0),
    'af3': (128, 0, 0),
    'o2': (0, 0, 64),
    'o1': (255, 0, 255),
    'fc5': (64, 64, 0),
    'x': (0, 128, 128),
    'y': (64, 0, 64),
    'unknown': (0, 255, 0)
}

# TODO: add curve- and timeout- and buffer size selectors
# add battery indicator 100 - 0


class MainWindow(QMainWindow):
    def __init__(self, current_user):
        self.sensors = list(SENSORS.keys())
        self.curves = {}
        self.data = {name: np.empty(100) for name in self.sensors}

        self.login_dialog = LoginDialog(current_user)
        QObject.connect(
            self.login_dialog, SIGNAL("logged()"), self._draw_main_window)
        QMainWindow.__init__(self)
        self.user = current_user
        uic.loadUi(MAINWINDOW_UI, self)
        self.errors.hide()
        self._log_in()
        self.ptr = 0

    def _log_in(self):
        self.login_dialog.show()
        self.login_dialog.exec_()

    def _init_pixmaps(self):
        self.left_pixmap = QPixmap(GO_LEFT_PIC).scaledToWidth(
            self.walking_man.width())
        self.right_pixmap = QPixmap(GO_RIGHT_PIC).scaledToWidth(
            self.walking_man.width())

    def set_go_left(self):
        self.walking_man.setPixmap(self.left_pixmap)

    def set_go_right(self):
        self.walking_man.setPixmap(self.right_pixmap)

    def _draw_main_window(self):
        self.show()

        # TODO: init sensors to show

        for sensor in self.sensors:
            self.curves[sensor] = self.raw_data.plot(
                self.data[sensor], pen=SENSORS[sensor], scale=100)
        print(len(self.curves))
        self._init_pixmaps()
        self.set_go_left()
        self.raw_data.setDownsampling(mode='peak')
        self.raw_data.setClipToView(True)
        self.raw_data.autoRange()
        self.raw_data.setXRange(-100, 0)

        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update_curves)

        # test sync

        self.timer1 = pg.QtCore.QTimer()
        self.timer1.timeout.connect(self.update_data)
        self.timer1.start(50)
        #
        self.timer.start(50)

    def update_curves(self):
        for sensor in self.curves:
            self.curves[sensor].setData(self.data[sensor][:self.ptr])
        self.raw_data.setXRange(self.ptr - 100, self.ptr)
        self.timer.start(50)

    def check_buffer(self):
        if self.ptr >= self.data[self.sensors[0]].shape[0]:
            for sensor in self.data:
                tmp = self.data[sensor]
                self.data[sensor] = np.empty(self.data[sensor].shape[0] * 2)
                self.data[sensor][:tmp.shape[0]] = tmp

    def update_data(self):
        self.check_buffer()
        if sys.argv[1] == 'test':
            self.generate_data()
        else:
            self.read_data()
        self.ptr += 1
        self.timer1.start(50)

    def generate_data(self):
        for shift, sensor in enumerate(self.data):
            self.data[sensor][self.ptr] = np.random.normal() + shift * 5
        self.raw_data.setYRange(-5, 85)

    def read_data(self):
        raise NotImplementedError
