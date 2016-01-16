from tkinter import *
from StartScreen import StartScreen
from modules.User import User
import sys
from PyQt4.QtGui import *
from modules.mainwindow import MainWindow


ICON = "img/emotiv_icon.png"


if __name__ == "__main__":
    root = Tk()
    icon = PhotoImage(file=ICON)
    root.tk.call('wm', 'iconphoto', root._w, icon)
    root.title("Biomeh")
    user = User()
    ss = StartScreen(root, user)
    root.mainloop()

    # pyqt
    app = QApplication(sys.argv)
    main_window = MainWindow(user)

    sys.exit(app.exec_())
    # app.exec_()
    print("EXITING")
