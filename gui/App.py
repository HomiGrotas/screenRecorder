from tkinter import Frame, LabelFrame, Label, Canvas, LEFT, Button, BOTH, StringVar, simpledialog, messagebox
from settings.assests import FONT_BIG, FONT_MEDIUM, FONT_SMALL, default_audio_name, default_video_name, default_time
from gui import WIDTH, HEIGHT
from recorders.VideoRecorder import VideoRecorderClass
from recorders.AudioRecorder import AudioRecorderClass


def record_video(**kwargs):
    """
    starts recording video
    :param kwargs: screen_size=SIZE, max_time=default_time, path=PATH, name="my_recording"
    :return: VideoRecorderClass object
    """
    r = VideoRecorderClass(**kwargs)
    r.start_recording()
    return r


def record_audio(**kwargs):
    """
    starts recording audio
    :param kwargs: max_time=default_time, path=PATH, name="my_audio"
    :return: AudioRecorderClass object
    """
    a = AudioRecorderClass(**kwargs)
    a.start_recording()
    return a


def time_to_int(time: str) -> int:
    """
    validates the time
    :param time: recording time
    :return: the time as int
    """
    hours = 'hour' in time
    time = float(time[6:time.find(' ', 6)])
    if hours:
        time *= 3600
    print(time)
    return time


def short_name(name: str) -> str:
    """
    :param name: the recording name in a sentence
    :return: recording name
    """
    return name[15:]


class App(Frame):
    """
    Gui application
    """
    def __init__(self, master):
        super().__init__(master=master)
        print(f"width: {WIDTH}, height: {HEIGHT}")

        # audio and variables as tkinter objects
        self.time = StringVar()
        self.audio_name = StringVar()
        self.video_name = StringVar()

        default_time_str = str(default_time)
        self.recordings = []  # list of the recordings
        self.time.set("time: " + default_time_str + ''.join(' ' for _ in range(38 - len(default_time_str))))
        # set recordings names
        self.audio_name.set("recording name: " + default_audio_name)
        self.video_name.set("recording name: " + default_video_name)

        # creates three frames - Main label, Audio frame and Video frame
        self._create_main_label_frame()
        self._create_recording_frame("Audio")
        self._create_recording_frame("Video")

        self.pack(fill=BOTH)

    def _create_main_label_frame(self):
        """
        creates the window's top
        :return: None
        """
        # frame for storage
        main_label_frame = Frame(master=self)
        main_label_frame.pack()

        # canvas for circle
        self.canvas = Canvas(master=main_label_frame, width=100, height=100)
        self.canvas.pack(side=LEFT)

        # create circle
        self.circle = self.canvas.create_oval(40, 25, 90, 70, outline="black", fill="red", width=6)

        # main label
        Label(master=main_label_frame, text="Recorder", font=FONT_BIG).pack()

    def _create_recording_frame(self, subject):
        """
        creates the recordings frames
        :param subject: Audio/ Video
        :return: None
        """
        rec_label_frame = LabelFrame(master=self, text=subject, font=FONT_MEDIUM, bd=5)
        left_side = Frame(master=rec_label_frame)

        # 4 buttons in a button frame
        buttons_frame = Frame(master=left_side)
        Button(master=buttons_frame, text=f"Record {subject}", height=2, width=13, font=FONT_SMALL,
               command=lambda: self._start_rec_by_subject(subject)).pack(side=LEFT, padx=10)

        Button(master=buttons_frame, text="Pause", height=2, width=10, font=FONT_SMALL,
               command=lambda: self._pause_recording(subject)).pack(side=LEFT, padx=10)

        Button(master=buttons_frame, text="Resume", height=2, width=10, font=FONT_SMALL,
               command=lambda: self._resume_recording(subject)).pack(side=LEFT, padx=10)

        Button(master=buttons_frame, text="Finish", height=2, width=10, font=FONT_SMALL,
               command=lambda: self._finish_rec_by_subject(subject)).pack(side=LEFT, padx=10)

        buttons_frame.pack(pady=30)
        left_side.pack(side=LEFT)

        # time and name labels
        self._create_time_and_name_labels(left_side, subject)

        rec_label_frame.pack(fill=BOTH, pady=30)

    def _create_time_and_name_labels(self, master, subject):
        """
        creates time and name labels and buttons
        :param master: recording frame
        :param subject: Audio/ Video
        :return: None
        """
        text_frame = Frame(master=master)

        # time label
        Label(master=text_frame, textvariable=self.time, font=FONT_SMALL).grid(row=0, column=0)

        # change time button
        Button(master=text_frame, text="Change", command=lambda: self._change_time()).grid(row=0, column=1)

        # name label
        Label(master=text_frame, font=FONT_SMALL,
              textvariable=self.audio_name if subject == 'Audio' else self.video_name).grid(row=1, column=0)

        # change name button
        Button(master=text_frame, text="Change", command=lambda: self._change_name(subject))\
            .grid(row=1, column=1, padx=30, pady=5)

        text_frame.pack(side=LEFT)

    def _recoding_beep(self):
        """
        changes the circle's color while recording
        :return:
        """
        if self.canvas.itemcget(self.circle, 'fill') == 'red':
            self.canvas.itemconfig(self.circle, fill="green")
        else:
            self.canvas.itemconfig(self.circle, fill="red")
        if any([r.is_recording() for r in self.recordings]):
            self.master.after(2000, lambda: self._recoding_beep())
        else:
            self.canvas.itemconfig(self.circle, fill="red")

    def _change_time(self):
        """
        changes the recordings time
        :return: None
        """
        msg = "Notice! if you don't write hours the time\nwill be calculated as seconds.\nEnter new time:"
        new_time = simpledialog.askstring(title="Change recording time", prompt=msg)

        # new_time has to be a digit bigger than 0
        while not new_time:
            msg = "Time must have a value. For example: 1 hours/ 1.5 hours/ 25 seconds"
            messagebox.showerror(title="ERROR", message=msg)
            new_time = simpledialog.askstring(title="Change recording time", prompt="Enter new time:")
        if new_time:
            self.time.set("time: " + new_time + ''.join(' ' for _ in range(42 - len(new_time))))

    def _change_name(self, subject):
        """
        changes recording name
        :param subject: Audio/ Video
        :return: None
        """
        new_name = simpledialog.askstring(title=f"Change {subject} name", prompt=f"New {subject} name:", maxvalue=20)
        if new_name:
            if subject == "Audio":
                self.audio_name.set("recording name: " + new_name + ''.join(' ' for _ in range(27 - len(new_name))))
            else:
                self.video_name.set("recording name: " + new_name + ''.join(' ' for _ in range(27 - len(new_name))))

    def _start_rec_by_subject(self, subject):
        """
        starts recording with parameters by subject
        :param subject: Audio/ Video
        :return: None
        """
        self.recording = True
        time = time_to_int(self.time.get())
        if subject == 'Audio':
            name = short_name(self.audio_name.get())
            self.recordings.append(record_audio(name=name, max_time=time))
        else:
            name = short_name(self.video_name.get())
            self.recordings.append(record_video(name=name, max_time=time))
        self._recoding_beep()
        print("Started recording " + subject)

    def _finish_rec_by_subject(self, subject):
        """
        finishes recording
        :param subject: Audio/ Video
        :return: None
        """
        rec_type = AudioRecorderClass if subject == 'Audio' else VideoRecorderClass
        recordings = list(filter(lambda r: r.is_recording() and isinstance(r, rec_type), self.recordings))
        if len(recordings) != 1:
            msg = f"There are multiple recordings right now.\n" \
                  f"Current recordings: {[r.get_path() for r in recordings]}\n" \
                  f"Please enter the index of the recording (1-{len(recordings)}):"

            ind = simpledialog.askinteger(title="Multiple recordings", prompt=msg) - 1
            recordings[ind].stop_pause()
            recordings[ind].finish()
        else:
            recordings[0].stop_pause()
            recordings[0].finish()

    def _pause_recording(self, subject):
        rec_type = AudioRecorderClass if subject == 'Audio' else VideoRecorderClass
        recordings = list(filter(lambda r: r.is_recording() and isinstance(r, rec_type), self.recordings))
        if len(recordings) != 1:
            msg = f"There are multiple recordings right now.\n" \
                  f"Current recordings: {[r.get_path() for r in recordings]}\n" \
                  f"Please enter the index of the recording (1-{len(recordings)}):"

            ind = simpledialog.askinteger(title="Multiple recordings", prompt=msg) - 1
            recordings[ind].pause()
        else:
            recordings[0].pause()
        print("paused")

    def _resume_recording(self, subject):
        rec_type = AudioRecorderClass if subject == 'Audio' else VideoRecorderClass
        recordings = list(filter(lambda r: r.is_recording() and isinstance(r, rec_type), self.recordings))
        if len(recordings) != 1:
            msg = f"There are multiple recordings right now.\n" \
                  f"Current recordings: {[r.get_path() for r in recordings]}\n" \
                  f"Please enter the index of the recording (1-{len(recordings)}):"

            ind = simpledialog.askinteger(title="Multiple recordings", prompt=msg) - 1
            recordings[ind].stop_pause()
        else:
            recordings[0].stop_pause()
        print("resumed")
