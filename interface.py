from tkinter import *
from StartScreen import StartScreen
from User import User
import sys
from PyQt4 import uic, QtCore
from PyQt4.QtGui import *

ICON = "Gameicon1.png"


class LoginWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi('login_window.ui', self)
        self.error.hide()
        self.setWindowTitle('Mood detector')
        self.setWindowIcon(QIcon(ICON))
        self.resize(400, 155)
        self.connect(
            self.startButton, QtCore.SIGNAL('clicked()'), self.display_error)

    def sign_up(self):
        # display new user creation window
        print("IN SIGN UP")

    def display_error(self, error="HEY, I'M AN ERROR"):
        print(self.size())
        if not self.error.isVisible():
            self.resize(self.width(), self.height()+25)
        self.error.setText(error)
        self.error.show()


if __name__ == "__main__":
    root = Tk()
    img = PhotoImage(file='Gameicon1.png')
    root.tk.call('wm', 'iconphoto', root._w, img)
    root.title("Mood detector")
    user = User()
    ss = StartScreen(root, user)
    root.mainloop()

    # pyqt
    app = QApplication(sys.argv)

    window = LoginWindow()
    window.show()

    sys.exit(app.exec_())
