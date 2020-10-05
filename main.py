from gui.App import App
from gui import root

__author__ = "Nadav Shani"


def start_gui():
    App(root)
    root.mainloop()


def main():
    start_gui()


if __name__ == "__main__":
    main()
