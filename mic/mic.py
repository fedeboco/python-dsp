import pyaudio
import time
import numpy as np
import filters as fil
from filters import settings
from filters import filters
from collections import deque

class MicFilter:
    width = 2
    channels = 1
    rate = 22050
    p = pyaudio.PyAudio()
    fil = [1]
    queue = deque(list(np.zeros(len(fil))))
    stream = 0
    filterSettings = 0
    stopFiltering = False

    def __init__(self, *args, **kwargs):
        if  'filter' in kwargs:
            fil = kwargs['filter']
            self.fil = np.array(fil[::-1])
        if 'channels' in kwargs:
            self.channels = kwargs['channels']
        if 'width' in kwargs:
            self.width = kwargs['width']
        if 'stopFlag' in kwargs:
            self.stopFiltering = kwargs['stopFlag']
        if 'filterSettings' in kwargs:
            self.filterSettings = kwargs['filterSettings']
            wVec = self.filterSettings.frequencies
            deltaVec = self.filterSettings.deltas
            ampVec = self.filterSettings.amplitudes
            self.rate = self.filterSettings.rate
            filter = filters.Filter(wVec, deltaVec, ampVec)
            self.fil = filter.filterMB()
        self.queue = deque(list(np.zeros(len(self.fil))))

    def getFilter(self):
        return self.fil[::-1]

    def getRate(self):
        return self.rate

    def getFilterWindow(self):
        return self.fil.getWindow()

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
        self.keepAliveStream()

    def callback(self, inData, frameCount, timeInfo, status):
        signalChunck = np.frombuffer(inData, dtype=np.int16)
        filteredChunck = ()
        ran = range(0, frameCount, 1)
        for n in ran:
            self.queue.append(signalChunck[n])
            self.queue.popleft()
            filteredSample = filters.filterSignal(self.queue, self.fil)
            filteredChunck = np.append(filteredChunck, filteredSample)
        return (filteredChunck.astype(np.int16).tostring(), pyaudio.paContinue)

    def keepAliveStream(self):
        while (self.stream.is_active() and self.stopFiltering.value == False):
            time.sleep(1)
        self.stopStream()

    def stopStream(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def devicesInfo(self):
        for i in range(self.p.get_device_count()):
            device = self.p.get_device_info_by_index(i)
            inputs = device.get('maxInputChannels', 0)
            if inputs > 0:
                name = device.get('name')
                rate = device.get('defaultSampleRate')
                print("Device {i}: {name} (Max Channels: {inputs}, {rate} Hz)".format(
                    i=i, name=name, inputs=inputs, rate=int(rate)
                ))







