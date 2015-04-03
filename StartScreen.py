__author__ = 'jbenua'

from Tkinter import *
import Tkinter as TkI
from ttk import *
from NewUserWin import NewUserWin
from Result import Result
import User

class StartScreen(object):
    def __init__(self, root, user):
        self.user = user
        self.root = root
        User.db.connect()
        u_res = User.users.select()
        list1 = []
        for i in u_res:
            list1.append(i.username)
        User.db.close()
        self.start_frame = Frame(root)
        self.passwd = Entry(self.start_frame, show="*")
        self.combo = Combobox(self.start_frame, values=list1)
        self.nu = Button(self.start_frame, width=47, text="new user", command=self.new_u)
        self.start_btn = Button(self.start_frame, text="START", command=self.start)
        self.alertu = TkI.Label(self.start_frame, text="choose user or create a new one", fg="red")
        self.alertup = TkI.Label(self.start_frame, text="incorrect pair 'login-password'", fg="red")
        self.alertErr = TkI.Label(self.start_frame, text="error: device not found", fg="red")
        self.loading = TkI.Label(self.start_frame, text="reading and analysing data...", fg='green')
        self.design()
        self.start_frame.pack()

    def design(self):
        Style().map('TButton', background=[('pressed',  'green')], text=[('pressed', 'loading')])
        self.root.geometry('437x117')
        self.root.resizable(False, False)
        self.combo.set("Select user...")
        self.combo.grid(row=0, column=0, padx=10, pady=15, sticky=W)
        self.passwd.grid(row=0, column=1, padx=10, pady=15, sticky=W)
        self.nu.grid(row=1, column=0, columnspan=3, padx=10, pady=15, sticky="nw")
        self.start_btn.grid(row=0, column=2, rowspan=2, pady=15, sticky="nsew")

    def start(self):
        u = self.combo.get()
        p = self.passwd.get()
        if u != "Select user...":
            if self.alertu.winfo_x() != 0:
                self.alertu.place_forget()
            User.db.connect()
            try:
                res = User.users.get(User.users.username == u, User.users.passwd == p)
                self.user.fill_info(u, p)
                if self.user.read_data():
                    self.show_results()
                else:
                    # test
                    # self.show_results()
                    #
                    if self.alertup.winfo_x() != 0:
                       self.alertup.place_forget()
                    self.alertErr.place(x=70, y=42)
            except User.users.DoesNotExist():
                self.alertup.place(x=70, y=42)
            finally:
                User.db.close()
        else:
            self.start_btn.bell()
            self.alertu.place(x=70, y=42)

    def show_results(self):
        r = Result(self.root, self.user)
        # better hide
        self.start_frame.destroy()

    def new_u(self):
        a = NewUserWin(self.user, self.combo)
        a.nuser.mainloop()