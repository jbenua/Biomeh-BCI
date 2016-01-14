import unittest
from modules.login import Login
from modules import User
from PyQt4.QtGui import *
import sys

TEST_USERNAME = "TestUsername"


class LoginDialogTests(unittest.TestCase):
    def setUp(self):
        super().setUp()
        QApplication(sys.argv)
        self.login_ = Login()
        User.db.connect()
        User.users.create(username=TEST_USERNAME, passwd="")
        User.db.close()
        self.to_remove = [TEST_USERNAME]

    def tearDown(self):
        super().tearDown()
        User.db.connect()
        for user_to_remove in self.to_remove:
            User.users.delete().where(
                User.users.username == user_to_remove).execute()
        User.db.close()

    def test_login(self):
        """login works well"""
        logged_in = self.login_.log_in(TEST_USERNAME, "")
        self.assertTrue(logged_in, msg="Error simply logging in")

    def test_incorrect_pair(self):
        """no user with this username or u-p pair"""
        username = '1' * 20
        logged_in = self.login_.log_in(username, '')
        self.assertFalse(
            logged_in,
            msg="Succeded logging in with incorrect pair login-password")

    def test_no_login(self):
        """no username occured in required field"""
        username = '1' * 20
        logged_in = self.login_.log_in(username, '')
        self.assertFalse(
            logged_in,
            msg="Succeded logging in with incorrect pair login-password")

    def test_sign_up(self):
        """sign up works well"""
        username = '1' * 20
        signed_up = self.login_.sign_up(username, '')
        self.assertTrue(signed_up, msg="Error signing up")
        self.to_remove.append(username)

    def test_sign_up_empty_login(self):
        """cannot sign up without login"""
        signed_up = self.login_.sign_up('', '')
        self.assertFalse(signed_up, msg="Succeded signing up with empty login")

    def test_sign_up_existing_login(self):
        """error if user already exists"""
        signed_up = self.login_.sign_up(TEST_USERNAME, '')
        self.assertFalse(signed_up, msg="Created account twice")
