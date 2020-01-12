# copyright: https://people.csail.mit.edu/hubert/pyaudio/docs/
"""PyAudio Example: Play a wave file (callback version)."""

import pyaudio
import wave
import time


class Play():
    def __init__(self,filename):
        self.wf = wave.open(filename, 'rb')

        # instantiate PyAudio (1)
        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(self.wf.getsampwidth()),
                        channels=self.wf.getnchannels(),
                        rate=self.wf.getframerate(),
                        output=True,
                        stream_callback=self.callback)

        # start the stream (4)
        stream.start_stream()

        # wait for stream to finish (5)
        while stream.is_active():
            time.sleep(0.1)

        # stop stream (6)
        stream.stop_stream()
        stream.close()
        self.wf.close()

        # close PyAudio (7)
        p.terminate()

        # define callback (2)
    def callback(self, in_data, frame_count, time_info, status):
        data = self.wf.readframes(frame_count)
        return (data, pyaudio.paContinue)

        # open stream using callback (3)

if __name__ == '__main__':
    Play('audio/busch/ballade1.wav')