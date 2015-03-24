__author__ = 'user'
import Tkinter as TkI
from ttk import *

# detect tags


class Result(object):
    def __init__(self, root, db, user):
        self.user = user
        self.db = db
        self.root = root
        self.tags_out = Frame(root)
        # self.tag_line = Text(self.tags_out, wrap=WORD, width=7)
        self.tag_line = Entry(self.tags_out, width=35)
        self.label = Label(self.tags_out, text="We detected, that you feel much like...")
        self.btn = Button(self.tags_out, text="Save changes", command=self.upd_tags)
        self.label1 = Label(self.tags_out, text="(we can be wrong sometimes,\nso you can edit these tags)")
        self.design()
        self.user.print_all_info()
        tags = self.user.detect(self.db)
        s = ""
        for t in tags:
            s += t + ", "
        s = s[:s.rfind(",")]
        self.tag_line.insert(0, s)
        self.tags_out.pack()

    def design(self):
        self.root.geometry('250x250')
        self.label.grid(row=0, column=0, padx=10, pady=20)
        self.tag_line.grid(row=1, column=0, padx=10, pady=20)  # WTF???
        self.label1.grid(row=2, column=0, padx=10, pady=10)
        self.btn.grid(row=3, column=0, padx=10)

    def upd_tags(self):
        s = self.tag_line.get().split(", ")
        print s
        frame3 = Frame(self.root)
        label3 = TkI.Label(frame3, text="Saved", fg="green")
        label3.pack()
        frame3.place(y=210, x=105)
        self.db.connect()
        for t in s:
            res = self.db.execute_sql("SELECT tag FROM tags WHERE tag='" + t + "'")
            if res.rowcount == 0:
                # add to main table too

                sq = "INSERT INTO tags (tag) VALUE ('" + t + "')"
                self.db.execute_sql(sq)
                print "tag added: ('" + t + "')"
        self.db.close()