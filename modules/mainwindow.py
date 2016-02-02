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


class MainWindow(QMainWindow):
    def __init__(self, current_user):
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

        self._init_pixmaps()
        self.set_go_left()
        self.data_store = np.empty(100)
        self.plot = self.raw_data.plot(self.data_store, pen=(255, 0, 0))
        self.raw_data.setDownsampling(mode='peak')
        self.raw_data.setClipToView(True)

        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)

    def update(self):
        if sys.argv[1] == 'test':
            self.generate_data()
        else:
            self.read_data()
        self.timer.start(50)

    def generate_data(self):
        if self.ptr >= self.data_store.shape[0]:
            print("DOUBLE IT")
            tmp = self.data_store
            self.data_store = np.empty(self.data_store.shape[0] * 2)
            self.data_store[:tmp.shape[0]] = tmp
        self.data_store[self.ptr] = np.random.normal()
        self.ptr += 1
        self.plot.setData(self.data_store[:self.ptr])
        self.raw_data.setXRange(self.ptr-100, self.ptr)

    def read_data(self):
        raise NotImplementedError
