from recorders.VideoRecorder import VideoRecorderClass
from recorders.AudioRecorder import AudioRecorderClass
from gui.App import App
from gui import root

__author__ = "Nadav Shani"


def start_gui():
    App(root)
    root.mainloop()


def record_video():
    r = VideoRecorderClass(max_time=60)
    r.start_recording()


def record_audio():
    a = AudioRecorderClass(max_time=60)
    a.start_recording()


def main():
    start_gui()


if __name__ == "__main__":
    main()
