from Tkinter import *
from peewee import *
from StartScreen import StartScreen
from User import User

if __name__ == "__main__":
    db = MySQLDatabase('headset', host='localhost', user='jbenua', passwd='jbenua')
    root = Tk()
    root.title("Mood detector")
    user = User()
    #user.read_data() # current session raw from headset, here or later
    ss = StartScreen(root, db, user)
    root.after(500, ss.design)
    root.mainloop()


