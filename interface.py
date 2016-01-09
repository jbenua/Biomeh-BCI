from Tkinter import *
from StartScreen import StartScreen
from User import User

if __name__ == "__main__":
    root = Tk()
    root.iconbitmap(bitmap="Gameicon.ico")
    root.title("Mood detector")
    user = User()
    ss = StartScreen(root, user)
    root.mainloop()
