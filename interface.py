__author__ = 'jbenua'

from Tkinter import *
from StartScreen import StartScreen
from User import User

if __name__ == "__main__":
    root = Tk()
    root.title("Mood detector")
    user = User()
    ss = StartScreen(root, user)
    root.mainloop()


