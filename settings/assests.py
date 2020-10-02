from tkinter import Tk
from os import environ
from settings.read_settings import Settings
from tkinter.font import Font

settings = Settings()

# --------------- #
# FILE VARIABLES  #
# --------------- #

# path
PATH = settings.get_setting_value("FILE VARIABLES", 'path')
if PATH == 'None':  # if there isn't a path by user
    PATH = environ["USERPROFILE"] + "\\Desktop\\"

# screen size - video recording
root = Tk()
SIZE = root.winfo_screenwidth(), root.winfo_screenheight()
del Tk, environ

# file ending
AUDIO_FILE_ENDING = settings.get_setting_value("FILE VARIABLES", 'audio_file_ending')
VIDEO_FILE_ENDING = settings.get_setting_value("FILE VARIABLES", 'video_file_ending')

default_time = int(settings.get_setting_value("FILE VARIABLES", 'default_time'))
default_audio_name = settings.get_setting_value("FILE VARIABLES", 'default_audio_name')
default_video_name = settings.get_setting_value("FILE VARIABLES", 'default_video_name')

# --------------- #
# GUI VARIABLES   #
# --------------- #

WIDTH = settings.get_setting_value("GUI VARIABLES", "width")
HEIGHT = settings.get_setting_value("GUI VARIABLES", "height")
if WIDTH == 'None':
    WIDTH = root.winfo_screenwidth()

if HEIGHT == 'None':
    HEIGHT = root.winfo_screenheight()

BIG = (WIDTH + HEIGHT) // 50
MEDIUM = (WIDTH + HEIGHT) // 100
SMALL = (WIDTH + HEIGHT) // 200

FONT_BIG = Font(family="Arial", size=BIG)
FONT_MEDIUM = Font(family="Arial", size=MEDIUM)
FONT_SMALL = Font(family="Arial", size=SMALL)

del BIG, MEDIUM, SMALL
