from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog, QMessageBox
from . import User

LOGIN_UI = './ui/login_dialog.ui'


class Login():
    def display_error(self, error="Default error msg"):
        print(error)

    def sign_up(self, username, password):
        """create new user's account"""
        User.db.connect()
        if not username:
            self.display_error("Username is required")
            return False
        try:
            User.users.get(User.users.username == username)
            self.display_error("User already exists! Choose another username")
            return False
        except User.users.DoesNotExist:
            User.users.create(username=username, passwd=password)
            return True
        User.db.close()

    def log_in(self, username, password):
        """try to log into the system"""
        User.db.connect()
        try:
            User.users.get(
                User.users.username == username,
                User.users.passwd == password)
        except User.users.DoesNotExist:
            self.display_error("Incorrect pair user-password!")
            return False
        User.db.close()
        return True


class LoginDialog(QDialog, Login):
    logged = pyqtSignal()
    
    def __init__(self, current_user):
        QDialog.__init__(self)
        self.user = current_user
        uic.loadUi(LOGIN_UI, self)
        self.start_button.clicked.connect(self.on_start_button)

    def display_error(self, error="DEFAULT ERROR MSG"):
        QMessageBox.critical(self, "Error", error)

    def on_start_button(self):
        """start_button singal catched"""
        username = self.login_input.text()
        password = self.password_input.text()
        create_account = self.new_user_checkbox.isChecked()
        if create_account:
            # create account

            if not self.sign_up(username, password):
                return

        if not self.log_in(username, password):
            return
        self.user.fill_info(username, password)
        self.logged.emit()
        self.close()
        return
