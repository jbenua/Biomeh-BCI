from tkinter import *
import tkinter as TkI
from tkinter.ttk import *
from NewUserWin import NewUserWin
from Result import Result
import User
import vk


def addifnew(u, p):
    try:
        User.users.get(User.users.username == u, User.users.passwd == p)
    except User.users.DoesNotExist:
        User.users.create(username=u, passwd=p)


class StartScreen(object):
    def __init__(self, root, user):
        self.u = ""
        self.p = ""
        self.user = user
        self.root = root
        self.soc_netw = False
        User.db.connect()
        u_res = User.users.select()
        list1 = []
        for i in u_res:
            if i.username != "vk":
                list1.append(i.username)
        User.db.close()
        self.start_frame = Frame(root)
        self.passwd = Entry(self.start_frame, show="*")
        self.combo = Combobox(self.start_frame, values=list1)
        self.nu = Button(
            self.start_frame, width=47, text="new user", command=self.new_u)
        self.start_btn = Button(
            self.start_frame, text="START", command=self.start)

        self.alertu = TkI.Label(
            self.start_frame, text="choose user or create a new one", fg="red")
        self.alertup = TkI.Label(
            self.start_frame, text="incorrect pair 'login-password'", fg="red")
        self.alertErr = TkI.Label(
            self.start_frame, text="error: device not found", fg="red")
        self.vk_alert = TkI.Label(self.start_frame, fg='red')

        self.loading = TkI.Label(
            self.start_frame, text="reading and analysing data...", fg='green')

        self.var = IntVar()
        self.chbox = TkI.Checkbutton(
            self.start_frame, text="sign in with", variable=self.var)

        imgPath = r"VK-Icon1.gif"
        photo = PhotoImage(file=imgPath)
        self.vk = Label(self.start_frame, image=photo)
        self.vk.image = photo

        self.design()
        self.start_frame.pack(pady=0)

    def design(self):
        Style().map(
            'TButton', background=[('pressed',  'green')],
            text=[('pressed', 'loading')])
        self.root.geometry('450x165')
        self.root.resizable(False, False)
        self.combo.set("Select user...")
        self.combo.grid(row=0, column=0, padx=10, pady=30, sticky=W)
        self.passwd.grid(row=0, column=1, padx=10, pady=30, sticky=W)
        self.nu.grid(
            row=1, column=0, columnspan=3, padx=10, pady=30, sticky="nw")
        self.start_btn.grid(
            row=0, column=2, rowspan=3, columnspan=2,
            padx=10, pady=30, sticky="nse")
        self.chbox.place(x=10, y=63)
        self.vk.place(x=100, y=60)

    def clear_errors(self):
        for i in [self.alertu, self.alertup, self.vk_alert, self.alertErr]:
            if i.winfo_x() != 0:
                i.place_forget()

    def start(self):
        self.clear_errors()
        print(self.var.get())
        self.u = self.combo.get()
        self.p = self.passwd.get()
        if self.u != "Select user...":
            if self.var.get() == 1:
                try:
                    self.user.vk = vk.API(
                        '4912863', self.u, self.p, scope='wall')
                    self.user.vk_token = self.user.vk.access_token
                    addifnew("vk", self.u)
                    self.var.set(0)
                    print("vk ok")
                    self.p = self.u
                    self.u = "vk"

                except Exception as err:
                    print("Error signing in!")
                    self.vk_alert.configure(text=err.args[0])
                    self.vk_alert.place(x=30, y=85)
                    return
            if self.var.get() == 0:
                User.db.connect()
                try:
                    print(self.u, self.p)
                    User.users.get(
                        User.users.username == self.u,
                        User.users.passwd == self.p)
                except:
                    self.alertup.place(x=70, y=85)
                    return

            self.user.fill_info(self.u, self.p)
            if self.user.read_data():
                self.show_results()
            else:
                # test
                # self.show_results()
                #
                self.alertErr.place(x=70, y=85)
                return
        else:
            self.start_btn.bell()
            self.alertu.place(x=70, y=85)

    def show_results(self):
        Result(self.root, self.user)
        self.start_frame.destroy()

    def new_u(self):
        a = NewUserWin(self.user, self.combo)
        a.nuser.mainloop()
