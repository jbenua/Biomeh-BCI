__author__ = 'jbenua'

from Tkinter import *
import Tkinter as TkI
from ttk import *
import User

class NewUserWin(object):
    def __init__(self, user, combo):
        self.combo = combo
        self.user = user
        self.nuser = Toplevel()
        self.nuser.iconbitmap(bitmap="Gameicon.ico")
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
            User.db.connect()
            try:
                res = User.users.get(User.users.username == u)
                print res.username
                self.u.bell()
                self.alert2.place(x=15, y=22)
            except User.users.DoesNotExist:
                p = self.p1.get()
                s = User.users.create(username=u, passwd=p)
                print "user added: ('" + u + "', '" + p + "')"
                self.combo['values'] += (u, )
                self.nuser.destroy()
            User.db.close()
        else:
            self.p2.bell()
            self.alert1.place(x=35, y=57)