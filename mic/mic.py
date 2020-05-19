import pyaudio
import time
import numpy as np
from filters import filters

# pip install PyAudio‑0.2.11‑cp38‑cp38‑win_amd64.whl

class MicFilter:
    WIDTH = 2
    CHANNELS = 1
    RATE = 22050
    p = pyaudio.PyAudio()
    MB = [1]
    queue = list(np.zeros(len(MB)))

    def __init__(self, fil = [1]):
        self.MB = np.array(fil[::-1])
        self.queue = list(np.zeros(len(self.MB)))

    def startStream(self):
        stream = self.p.open(format=self.p.get_format_from_width(self.WIDTH),
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        output=True,
                        stream_callback=self.callback)

        stream.start_stream()
        while stream.is_active():
            time.sleep(0.1)
        stream.stop_stream()
        stream.close()
        self.p.terminate()

    def callback(self, in_data, frame_count, time_info, status):
        amplitude = np.frombuffer(in_data, dtype=np.int16)
        out_data = ()
        ran = range(0, frame_count, 1)
        for n in ran:
            self.queue.append(amplitude[n])
            self.queue.pop(0)
            filteredSample = filters.filterSignal(self.queue[- len(self.MB):], self.MB)
            out_data = np.append(out_data, int(filteredSample))
        return (out_data.astype(np.int16).tostring(), pyaudio.paContinue)










