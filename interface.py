from tkinter import *
from StartScreen import StartScreen
from User import User


if __name__ == "__main__":
    root = Tk()
    img = PhotoImage(file='Gameicon1.png')
    root.tk.call('wm', 'iconphoto', root._w, img)
    root.title("Mood detector")
    user = User()
    ss = StartScreen(root, user)
    root.mainloop()
