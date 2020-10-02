from tempfile import mktemp
from queue import Queue
from time import time
from sounddevice import InputStream, query_devices
from soundfile import SoundFile
from threading import Thread
from os import rename
from os.path import isfile
from settings.assests import PATH, default_time, AUDIO_FILE_ENDING


class AudioRecorderClass:

    def __init__(self, max_time=default_time, path=PATH, name="my_audio"):
        self._recording_time = max_time
        self._name = name
        self._recording_works = False
        self._path = path
        self._finished = False

        self._file = mktemp(prefix="temp", suffix='.wav', dir=self._path)
        self._queue = Queue()

    def _callback(self, in_data, *_):
        """This is called (from a separate thread) for each audio block."""
        self._queue.put(in_data.copy())

    def _recording(self):
        start = time()
        sample_rate = int(query_devices(None, 'input')['default_samplerate'])
        channels = 1

        # Make sure the file is opened before recording anything:
        with SoundFile(self._file, mode='x', samplerate=sample_rate, channels=channels) as file:
            with InputStream(callback=self._callback, channels=channels):

                while time() - start < self._recording_time:
                    file.write(self._queue.get())

        self._change_name(self._name)
        self._finished = True

    def _change_name(self, new_name: str):
        counter = 1
        while isfile(self._path + new_name + str(counter) + AUDIO_FILE_ENDING):
            counter += 1

        new_name = self._path + new_name + str(counter) + AUDIO_FILE_ENDING
        rename(self._file, new_name)
        self._file = new_name

    def start_recording(self):
        self._recording_works = True
        Thread(target=self._recording).start()

    def stop(self):
        self._recording_time = -1

    def get_path(self):
        return self._file

    def is_recording(self):
        return not self._finished
