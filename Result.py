from Tkinter import *
import Tkinter as TkI
from ttk import *
import User


class Result(object):
    def __init__(self, root, user):
        self.user = user
        self.user.print_all_info()
        self.root = root
        self.tags_out = Frame(root)
        self.tag_line = Entry(self.tags_out, width=35)
        self.label = Label(
            self.tags_out, text="It's detected, that you feel much like...")
        self.btn = Button(
            self.tags_out, text="Save changes in taglist",
            command=self.upd_tags)
        self.label1 = Label(
            self.tags_out,
            text="(we can be wrong sometimes,\nso you can edit these tags)")
        self.tags = self.user.detect()
        self.exit_btn = Button(
            self.tags_out, text="Exit", command=self.exit)
        self.vk_button = Button(
            self.tags_out, text="Post to my wall", command=self.post_to_vk)
        imgPath = r"VK-Icon1.gif"
        photo = PhotoImage(file=imgPath)
        self.vk_button.configure(compound=LEFT, image=photo)
        self.vk_button.image = photo
        self.vk_text = TkI.Text(
            self.tags_out, height=7, width=35, font='TkTextFont', wrap='word')
        self.design()
        self.tags_out.pack()

    def post_to_vk(self):
        self.root.geometry('250x400')
        str = "Hey! I've just used jbenua's coursework to detect my mood. " +\
            "It said, I feel like " + self.tag_line.get() + " #mooddetector"
        self.vk_text.insert(1.0, str)
        self.vk_text.grid(row=4, column=0, pady=10)
        for i in [self.vk_button, self.exit_btn]:
            i.place_forget()
        self.vk_button.configure(text="Send", command=self.send)
        self.vk_button.grid(row=5, column=0, pady=10)
        self.exit_btn.grid(row=6, column=0, pady=0)

    def send(self):
        curstr = self.vk_text.get('1.0', 'end')
        self.vk_text.grid_remove()
        print curstr
        try:
            self.root.geometry('250x300')
            self.user.vk.wall.post(message=curstr)
            for i in [self.vk_button, self.exit_btn]:
                i.place_forget()
            self.vk_button.configure(text="Done!", state='disabled')
            self.vk_button.grid(row=4, column=0, pady=10)
            self.exit_btn.grid(row=5, column=0, pady=10)
        except:
            print "err"

    def design(self):
        s = ""
        for t in self.tags:
            s += t + ", "
        s = s[:s.rfind(",")]
        self.tag_line.insert(0, s)
        self.label.grid(row=0, column=0, padx=10, pady=20)
        self.tag_line.grid(row=1, column=0, padx=10, pady=10)  # WTF???
        self.label1.grid(row=2, column=0, padx=10, pady=10)
        self.btn.grid(row=3, column=0, padx=10)
        if self.user.vk:
            self.root.geometry('250x300')
            self.vk_button.grid(row=4, column=0, pady=10)
            self.exit_btn.grid(row=5, column=0, pady=10)
        else:
            self.root.geometry('250x250')
            self.exit_btn.grid(row=4, column=0, pady=10)

    def upd_tags(self):
        self.tags = self.tag_line.get().split(", ")
        frame3 = Frame(self.root)
        label3 = TkI.Label(frame3, text="Saved", fg="green")
        label3.pack()
        frame3.place(y=94, x=105)

    def save(self):
        User.db.connect()
        for t in self.tags:
            try:
                res = User.tags.get(User.tags.tag == t).id
            except User.tags.DoesNotExist:
                res = User.tags.create(tag=t).id
                print "tag added: ('" + t + "')"
            try:
                User.sessions.get(
                    User.sessions.raw_id == str(self.user.current_session_id),
                    User.sessions.user_id == str(self.user.userid),
                    User.sessions.tag_id == str(res))
            except User.sessions.DoesNotExist:
                User.sessions.create(raw_id=str(self.user.current_session_id),
                                     user_id=str(self.user.userid),
                                     tag_id=str(res))
        User.db.close()

    def exit(self):
        if self.tags:
            self.save()
        self.root.quit()
