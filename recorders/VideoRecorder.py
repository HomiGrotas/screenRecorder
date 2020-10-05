from cv2 import VideoWriter_fourcc, VideoWriter, cvtColor, COLOR_BGR2RGB
import numpy as np
from pyautogui import screenshot
from threading import Thread, Event
from settings.assests import PATH, default_time, SIZE, VIDEO_FILE_ENDING
from time import time
from os.path import isfile


class VideoRecorderClass:
    
    def __init__(self, screen_size=SIZE, max_time=default_time, path=PATH, name="my_recording"):
        print("max_time:", max_time)
        self._size = screen_size
        self._max_time = max_time
        self._record = False
        self._file = None
        self._path = path
        self._name = self._find_usable_name(name)
        self._not_pause = Event()  # false by default
        self._not_pause.set()  # true

    def start_recording(self):
        self._record = True
        Thread(target=self._recording).start()

    def _recording(self):
        start = time()

        # create the video write object
        self._file = VideoWriter(self._name, VideoWriter_fourcc(*"XVID"), 14.3, self._size)

        while self._record and time() - start < self._max_time:
            self._not_pause.wait()  # if paused it waits

            # make a screenshot
            img = screenshot()
            # convert these pixels to a proper numpy array to work with OpenCV
            frame = np.array(img)
            # convert colors from BGR to RGB
            frame = cvtColor(frame, COLOR_BGR2RGB)
            # write the frame
            self._file.write(frame)

        self._file.release()
        self._record = False

    def _find_usable_name(self, name):
        counter = 1
        while isfile(self._path + name + str(counter) + VIDEO_FILE_ENDING):
            counter += 1
        return self._path + name + str(counter) + VIDEO_FILE_ENDING

    def get_path(self):
        return self._name

    def finish(self):
        self._record = False

    def is_recording(self):
        return self._record

    def pause(self):
        self._not_pause.clear()  # false

    def stop_pause(self):
        self._not_pause.set()  # true
