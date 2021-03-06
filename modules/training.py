from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
import sys
from PyQt5.QtWidgets import *

UI = './ui/training.ui'


class TrainingDialog(QDialog):
    def __init__(self, parent):
        self._buffer = []
        QDialog.__init__(self)
        uic.loadUi(UI, self)
        self.parent = parent
        self.parent.to_save = None
        self.begin = 0
        self.end = 0
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
            self.begin = self.parent.ptr

    def on_stop_button(self):
        """stop button signal catched"""
        self.is_first_try = False
        self.stop_button.setEnabled(False)
        self.start_button.setEnabled(True)
        self.end = self.parent.ptr

    def on_ok(self):
        """ok button clicked"""
        if not self.title_input.text():
            QMessageBox.critical(self, "Error", 'Title is required')
        else:
            self.parent.to_save = {
                'title': self.title_input.text(),
                'begin': self.begin,
                'end': self.end
            }
            self.close()

    def on_cancel(self):
        """cancel button clicked"""
        if not self.is_first_try:
            reply = QMessageBox.question(
                self, 'Confirmation',
                "All the recorded data will be lost. Continue?",
                QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    d = TrainingDialog()
    d.show()
    sys.exit(app.exec_())
