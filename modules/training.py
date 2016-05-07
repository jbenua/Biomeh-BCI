from PyQt4 import uic
from PyQt4.QtGui import QDialog
import sys
from PyQt4.QtGui import *

UI = './ui/training.ui'


class TrainingDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi(UI, self)
        self.start_button.clicked.connect(self.on_start_button)
        self.stop_button.clicked.connect(self.on_stop_button)
        self.save_button.clicked.connect(self.on_ok)
        self.discard_button.clicked.connect(self.on_cancel)
        self.is_first_try = True

    def on_start_button(self):
        """start_button singal catched"""
        allowed = True
        if not self.is_first_try:
            reply = QMessageBox.question(
                self, 'Confirmation',
                "All the recorded data will be overwritten. Continue?",
                QMessageBox.Yes, QMessageBox.No)
            if reply != QMessageBox.Yes:
                allowed = False
        if allowed:
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            # start recording data

    def on_stop_button(self):
        """stop button signal catched"""
        self.is_first_try = False
        self.stop_button.setEnabled(False)
        self.start_button.setEnabled(True)
        # stop recording data

    def on_ok(self):
        """ok button clicked"""
        if not self.title_input.text():
            QMessageBox.critical(self, "Error", 'Incorrect user or password')
        else:
            pass
            # save data
            # close dialogf

    def on_cancel(self):
        """cancel button clicked"""
        if not self.is_first_try:
            reply = QMessageBox.question(
                self, 'Confirmation',
                "All the recorded data will be lost. Continue?",
                QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.close()


app = QApplication(sys.argv)
d = TrainingDialog()
d.show()
sys.exit(app.exec_())
