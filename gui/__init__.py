from settings.assests import WIDTH, HEIGHT, root
from tkinter import PhotoImage

WIDTH = int(WIDTH / 1.5)
HEIGHT = int(HEIGHT / 1.5)
root.iconphoto(True, PhotoImage(file="mom_icon.png"))

root.geometry(f"{WIDTH}x{HEIGHT}")
root.title("Record audio & video by Nadav Shani")
