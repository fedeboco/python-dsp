from timeit import default_timer as timer
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
    circularArray = 0
    K = 0

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
            self.fil = filter.build()
        self.queue = deque(list(np.zeros(len(self.fil))))
        self.circularArray = np.zeros(len(self.fil), dtype = float)
        self.K = 0

    def getFilter(self):
        return self.fil[::-1]

    def getRate(self):
        return self.rate

    def getFilterWindow(self):
        return self.fil.getWindow()

    def newFilter(self, customFilter):
        self.fil = np.array(customFilter[::-1])

    def startStream(self, updatedFil, updatesAvailable):
        call = (lambda i, f, t, st, fil = updatedFil, ua = updatesAvailable : 
                self.filterCallback(i, f, t, st, fil, ua))
        self.stream = self.p.open(format=self.p.get_format_from_width(self.width),
                        channels=self.channels,
                        rate=self.rate,
                        input=True,
                        output=True,
                        stream_callback = call)

        self.stream.start_stream()
        self.keepAliveStream()

    def filterCallback(self, inData, frameCount, timeInfo, status, fil, ua):
        updatesAvailable = ua.value
        if (updatesAvailable):
            ua.value = False
            self.fil = list(fil)
            self.queue = deque(list(np.zeros(len(self.fil))))
            self.circularArray = np.zeros(len(self.fil))
            self.K = 0 #circularArray index
        signalChunck = np.frombuffer(inData, dtype=np.int16)
        filteredChunck = np.zeros(len(signalChunck), dtype = float)
        ran = range(frameCount)
        K = self.K
        M = len(self.circularArray)
        A = np.zeros([len(signalChunck), len(self.fil)], dtype = float)
        for n in ran:
            self.circularArray[K] = signalChunck[n]
            A[n, M-K:] = self.circularArray[:K]
            A[n, :M-K] = self.circularArray[K:M]
            if (K == len(self.circularArray) - 1):
                K = 0
            else:
                K += 1
        filteredChunck = A.dot(self.fil)
        self.K = K
        return (filteredChunck.astype(np.int16).tostring(), pyaudio.paContinue)

    def filterCallbackOld2(self, inData, frameCount, timeInfo, status, fil, ua):
        updatesAvailable = ua.value
        if (updatesAvailable):
            ua.value = False
            self.fil = list(fil)
            self.queue = deque(list(np.zeros(len(self.fil))))
            self.circularArray = np.zeros(len(self.fil))
            self.K = 0 #circularArray index
        signalChunck = np.frombuffer(inData, dtype=np.int16)
        filteredChunck = np.zeros(len(signalChunck))
        ran = range(frameCount)
        K = self.K
        M = len(self.circularArray)
        c = time.time()
        s1 = 0; s2 = 0; s3 = 0; s4 = 0; s5 = 0; 
        for n in ran:
            c1 = time.time() * 1000000
            self.circularArray[K] = signalChunck[n]
            c2 = time.time() * 1000000
            s1 = s1 + c2 - c1
            y1 = np.dot(self.circularArray[ :K ], self.fil[ M-K : M ])
            y2 = np.dot(self.circularArray[ K:M ], self.fil[ :M-K ])
            c3 = time.time() * 1000000
            s2 = s2 + c3 - c2
            filteredSample = y1 + y2
            c4 = time.time() * 1000000
            s3 = s3 + c4 - c3
            filteredChunck[n] = filteredSample
            c5 = time.time() * 1000000
            s4 = s4 + c5 - c4
            if (K == len(self.circularArray) - 1):
                K = 0
            else:
                K += 1
            c6 = time.time() * 1000000
            s5 = s5 + c6 - c5
            print(c3 - c2, filteredSample, K, n)
        self.K = K
        print("time:", (time.time() - c) * 1000000, s1, s2, s3, s4, s5)
        return (filteredChunck.astype(np.int16).tostring(), pyaudio.paContinue)

    def filterCallbackOld(self, inData, frameCount, timeInfo, status, fil, ua):
        # start = time.time() * 1000000
        updatesAvailable = ua.value
        # a = time.time() * 1000000
        if (updatesAvailable):
            ua.value = False
            self.fil = list(fil)
            self.queue = deque(list(np.zeros(len(self.fil))))  #crashes if commented
        # b = time.time() * 1000000
        signalChunck = np.frombuffer(inData, dtype=np.int16)
        filteredChunck = ()
        ran = range(0, frameCount, 1)
        # c = time.time() * 1000000
        # s2 = 0; s3 = 0; s4 = 0; s5 = 0
        for n in ran:
            # c1 = time.time() * 1000000
            self.queue.append(signalChunck[n])
            # c2 = time.time() * 1000000
            # s2 = s2 + c2 - c1
            self.queue.popleft()
            # c3 = time.time() * 1000000
            # s3 = s3 + c3 - c2
            filteredSample = filters.filterSignal(self.queue, self.fil)
            # c4 = time.time() * 1000000
            # s4 = s4 + c4 - c3
            filteredChunck = np.append(filteredChunck, filteredSample)
            # c5 = time.time() * 1000000
            # s5 = s5 + c5 - c4
        # d = time.time() * 1000000
        #print("[", a-start, b-a, c-b, d-c, "] [", s2, s3, s4, s5, "]")
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







