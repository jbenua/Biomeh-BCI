from PyQt4 import uic
from PyQt4.QtGui import QMainWindow, QPixmap
from PyQt4.QtCore import QObject, SIGNAL
from .login import LoginDialog

MAINWINDOW_UI = './ui/main_window.ui'
GO_LEFT_PIC = './img/go_left.png'
GO_RIGHT_PIC = './img/go_right.png'


class MainWindow(QMainWindow):
    def __init__(self, current_user):
        self.login_dialog = LoginDialog(current_user)
        QObject.connect(
            self.login_dialog, SIGNAL("logged()"), self.draw_main_window)

        QMainWindow.__init__(self)
        self.user = current_user
        uic.loadUi(MAINWINDOW_UI, self)
        self.errors.hide()
        self.log_in()

    def log_in(self):
        self.login_dialog.show()
        self.login_dialog.exec_()

    def draw_main_window(self):
        self.show()

        pixmap = QPixmap(GO_LEFT_PIC).scaledToWidth(self.walking_man.width())
        self.walking_man.setPixmap(pixmap)
        import numpy as np
        import pyqtgraph as pg

        data = np.random.normal(size=1000)
        self.raw_data.plot(data)