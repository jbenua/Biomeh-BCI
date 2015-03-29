__author__ = 'jbenua'

import Tkinter as TkI
from ttk import *


class Result(object):
    def __init__(self, root, user):
        self.user = user
        self.user.print_all_info()
        self.db = user.db
        self.root = root
        self.tags_out = Frame(root)
        self.tag_line = Entry(self.tags_out, width=35)
        self.label = Label(self.tags_out, text="It's detected, that you feel much like...")
        self.btn = Button(self.tags_out, text="Save changes", command=self.upd_tags)
        self.label1 = Label(self.tags_out, text="(we can be wrong sometimes,\nso you can edit these tags)")
        self.tags = self.user.detect(self.db)
        self.exit_btn = Button(self.tags_out, text="Exit", command=self.exit)
        self.design()
        self.tags_out.pack()

    def design(self):
        self.root.geometry('250x250')
        s = ""
        for t in self.tags:
            s += t + ", "
        s = s[:s.rfind(",")]
        self.tag_line.insert(0, s)
        self.label.grid(row=0, column=0, padx=10, pady=20)
        self.tag_line.grid(row=1, column=0, padx=10, pady=20)  # WTF???
        self.label1.grid(row=2, column=0, padx=10, pady=10)
        self.btn.grid(row=3, column=0, padx=10)
        self.exit_btn.grid(row=4, column=0, padx=10, pady=10)

    def upd_tags(self):
        self.tags = self.tag_line.get().split(", ")
        frame3 = Frame(self.root)
        label3 = TkI.Label(frame3, text="Saved", fg="green")
        label3.pack()
        frame3.place(y=110, x=105)

    def save(self):
        self.db.connect()
        for t in self.tags:
            res = self.db.execute_sql("SELECT id FROM tags WHERE tag='" + t + "'")
            if res.rowcount == 0:
                self.db.execute_sql("INSERT INTO tags (tag) VALUE ('" + t + "')")
                res = self.db.execute_sql("SELECT LAST_INSERT_ID();")
                print "tag added: ('" + t + "')"
            for i in res:
                s="SELECT * FROM sessions WHERE raw_id='" + str(self.user.current_session_id) +\
                                           "' AND user_id='" + str(self.user.userid) + "' AND tag_id='" + str(i[0]) + "'"
                res1 = self.db.execute_sql(s)
                if res1.rowcount == 0:
                    ins = "INSERT INTO sessions (raw_id, user_id, tag_id) VALUES('" +\
                          str(self.user.current_session_id) + "', '" + str(self.user.userid) + "', '" + str(i[0]) + "')"
                    self.db.execute_sql(ins)

    def exit(self):
        if not self.tags and self.tags is not ['Nothing was read']:
            self.save()
        self.root.quit()