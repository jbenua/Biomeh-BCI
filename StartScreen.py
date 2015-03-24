__author__ = 'user'
from Tkinter import *
import Tkinter as TkI
from ttk import *

from NewUserWin import NewUserWin
from Result import Result


class StartScreen(object):
    def __init__(self, root, db, user):
        self.user = user
        self.root = root
        self.db = db
        self.db.connect()
        u_res = self.db.execute_sql("SELECT username FROM users")
        list1 = []
        for i in u_res:
            l = str(i).split("'")
            list1.append(l[1])
        self.db.close()
        self.start_frame = Frame(root)
        self.passwd = Entry(self.start_frame, show="*")
        self.combo = Combobox(self.start_frame, values=list1)
        self.nu = Button(self.start_frame, width=47, text="new user", command=self.new_u)
        self.start_btn = Button(self.start_frame, text="START", command=self.start)
        self.alertu = TkI.Label(self.start_frame, text="choose user or create a new one", fg="red")
        self.alertup = TkI.Label(self.start_frame, text="incorrect pair 'login-password'", fg="red")
        self.start_frame.pack()

    def design(self):
        self.root.geometry('437x117')
        self.root.resizable(False, False)
        self.combo.set("Select user...")
        self.combo.grid(row=0, column=0, padx=10, pady=15, sticky=W)
        self.passwd.grid(row=0, column=1, padx=10, pady=15, sticky=W)
        self.nu.grid(row=1, column=0, columnspan=3, padx=10, pady=15, sticky="nw")
        self.start_btn.grid(row=0, column=2, rowspan=2, pady=15, sticky="nsew")

    # hide, not destroy
    def start(self):
        u = self.combo.get()
        p = self.passwd.get()
        if u != "Select user...":
            if self.alertu.winfo_x() != 0:
                self.alertu.place_forget()
            self.db.connect()
            res = self.db.execute_sql("SELECT username, passwd FROM users WHERE username='"
                                      + u + "' AND passwd='" + p + "'")
            if res.rowcount == 1:
                self.user.fill_info(self.db, u, p)
                self.db.close()
                r = Result(self.root, self.db, self.user)
                # better hide
                self.start_frame.destroy()
            else:
                self.alertup.place(x=70, y=42)
        else:
            self.start_btn.bell()
            self.alertu.place(x=70, y=42)

    def new_u(self):
        a = NewUserWin(self.db, self.user, self.combo)
        a.nuser.mainloop()