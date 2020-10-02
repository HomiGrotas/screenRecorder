from tkinter import Frame, LabelFrame, Label, Canvas, LEFT, Button, BOTH, StringVar
from settings.assests import FONT_BIG, FONT_MEDIUM, FONT_SMALL, default_audio_name, default_video_name, default_time
from gui import WIDTH, HEIGHT


class App(Frame):
    def __init__(self, master):
        super().__init__(master=master)
        self.recording = False
        print(f"width: {WIDTH}, height: {HEIGHT}")

        # audio and variables
        self.time = StringVar()
        self.audio_name = StringVar()
        self.video_name = StringVar()

        self.time.set("time: " + str(default_time) + " seconds" + ''.join(' ' for _ in range(25)))
        self.audio_name.set("recording name: " + default_audio_name)
        self.video_name.set("recording name: " + default_video_name)

        # creates three frames - Main label, Audio frame and Video frame
        self._create_main_label_frame()
        self._create_recording_frame("Audio")
        self._create_recording_frame("Video")

        self.pack(fill=BOTH)
        self.start_recording_beep()

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
        rec_label_frame = LabelFrame(master=self, text=subject, font=FONT_MEDIUM, bd=5)
        left_side = Frame(master=rec_label_frame)

        # 3 buttons in a button frame
        #   ToDo: commands
        buttons_frame = Frame(master=left_side)
        Button(master=buttons_frame, text=f"Record {subject}", height=2, width=13, font=FONT_SMALL)\
            .pack(side=LEFT, padx=10)

        Button(master=buttons_frame, text="Stop", height=2, width=10, font=FONT_SMALL).pack(side=LEFT, padx=10)
        Button(master=buttons_frame, text="Finish", height=2, width=10, font=FONT_SMALL).pack(side=LEFT, padx=10)

        buttons_frame.pack(pady=30)
        left_side.pack(side=LEFT)

        # time and name labels
        self._create_time_and_name_labels(left_side, subject)

        rec_label_frame.pack(fill=BOTH, pady=30)

    def _create_time_and_name_labels(self, master, subject):
        text_frame = Frame(master=master)

        # time label
        Label(master=text_frame, textvariable=self.time, font=FONT_SMALL).grid(row=0, column=0)
        Button(master=text_frame, text="Change").grid(row=0, column=1)

        # name label
        Label(master=text_frame, font=FONT_SMALL,
              textvariable=self.audio_name if subject == 'Audio' else self.video_name).grid(row=1, column=0)

        Button(master=text_frame, text="Change").grid(row=1, column=1, padx=30, pady=5)

        text_frame.pack(side=LEFT)

    def _recoding_beep(self):
        if self.canvas.itemcget(self.circle, 'fill') == 'red':
            self.canvas.itemconfig(self.circle, fill="green")
        else:
            self.canvas.itemconfig(self.circle, fill="red")
        if self.recording:
            self.master.after(2000, self._recoding_beep)

    def start_recording_beep(self):
        self.recording = True
        self.master.after(1000, self._recoding_beep)
