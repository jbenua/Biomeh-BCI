__author__ = 'jbenua'

from Tkinter import *
import Tkinter as TkI
from ttk import *


class NewUserWin(object):
    def __init__(self, user, combo):
        self.combo = combo
        self.user = user
        self.db = user.db
        self.nuser = Toplevel()
        self.l1 = Label(self.nuser, text="Enter the username:")
        self.l2 = Label(self.nuser, text="Enter the password:")
        self.l3 = Label(self.nuser, text="Re-enter the password:")
        self.u = Entry(self.nuser)
        self.p1 = Entry(self.nuser, show="*")
        self.p2 = Entry(self.nuser, show="*")
        self.cr = Button(self.nuser, text="Create!", command=self.add_user)
        self.alert1 = TkI.Label(self.nuser, text="no match!", fg="red")
        self.alert2 = TkI.Label(self.nuser, text="user already exists!", fg="red")
        self.design()

    def design(self):
        self.nuser.title("Creating a user...")
        self.nuser.geometry('275x150')
        self.nuser.resizable(False, False)
        self.l1.grid(row=0, column=0, padx=5, pady=5)
        self.l2.grid(row=1, column=0, padx=5, pady=5)
        self.l3.grid(row=2, column=0, padx=5, pady=5)
        self.u.grid(row=0, column=1, padx=5, pady=5)
        self.p1.grid(row=1, column=1, padx=5, pady=5)
        self.p2.grid(row=2, column=1, padx=5, pady=5)
        self.cr.grid(row=3, column=0, columnspan=2, padx=30, pady=10, sticky="ew")
        self.nuser.grab_set()
        self.nuser.focus_force()

    def add_user(self):
        if self.p1.get() == self.p2.get():
            if self.alert1.winfo_x() != 0:
                self.alert1.place_forget()
            u = self.u.get()
            self.db.connect()
            res = self.db.execute_sql("SELECT username FROM users WHERE username='" + u + "'")
            if res.rowcount == 0:
                p = self.p1.get()
                s = "INSERT INTO users (username, passwd) VALUES ('" \
                    + u + "', '" + p + "')"
                self.db.execute_sql(s)
                print "user added: ('" + u + "', '" + p + "')"
                self.combo['values'] += (u, )
                self.nuser.destroy()
            else:
                self.u.bell()
                self.alert2.place(x=15, y=22)
            self.db.close()
        else:
            self.p2.bell()
            self.alert1.place(x=35, y=57)