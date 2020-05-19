import pyaudio
import time
import numpy as np
from filters import filters

# pip install PyAudio‑0.2.11‑cp38‑cp38‑win_amd64.whl

class MicFilter:
    width = 2
    channels = 1
    rate = 22050
    p = pyaudio.PyAudio()
    fil = [1]
    queue = list(np.zeros(len(fil)))
    stream = 0

    def __init__(self, *args, **kwargs):
        if  'filter' in kwargs:
            fil = kwargs['filter']
            self.fil = np.array(fil[::-1])
        if 'channels' in kwargs:
            self.channels = kwargs['channels']
        if 'width' in kwargs:
            self.width = kwargs['width']
        self.queue = list(np.zeros(len(self.fil)))

    def newFilter(self, filter):
        self.fil = np.array(filter[::-1])

    def startStream(self):
        self.stream = self.p.open(format=self.p.get_format_from_width(self.width),
                        channels=self.channels,
                        rate=self.rate,
                        input=True,
                        output=True,
                        stream_callback=self.callback)

        self.stream.start_stream()
        self.blockStreaming()
        self.stopStream()


    def callback(self, inData, frameCount, timeInfo, status):
        signalChunck = np.frombuffer(inData, dtype=np.int16)
        filteredChunck = ()
        ran = range(0, frameCount, 1)
        for n in ran:
            self.updateQueue(signalChunck[n])
            filteredSample = filters.filterSignal(self.queue[-len(self.fil):], self.fil)
            filteredChunck = np.append(filteredChunck, filteredSample)
        return (filteredChunck.astype(np.int16).tostring(), pyaudio.paContinue)

    def blockStreaming(self):
        while self.stream.is_active():
            time.sleep(0.1)

    def updateQueue(self, amplitudeValue):
        self.queue.append(amplitudeValue)
        self.queue.pop(0)

    def stopStream(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()









