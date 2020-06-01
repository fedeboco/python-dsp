from timeit import default_timer as timer
import pyaudio
import time
import numpy as np
import filters as fil
from filters import settings
from filters import filters

class MicFilter:
    width = 2
    channels = 1
    rate = 22050
    p = pyaudio.PyAudio()
    fil = [1]
    M = 0
    stream = 0
    filterSettings = 0
    stopFiltering = False
    circularArray = 0
    K = 0
    restartFlag = False

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
        self.M = len(self.fil)
        self.circularArray = np.zeros(self.M, dtype = float)
        self.K = 0

    def getFilter(self):
        return self.fil[::-1]

    def getRate(self):
        return self.rate

    def getFilterWindow(self):
        return self.fil.getWindow()

    def newFilter(self, customFilter):
        self.fil = np.array(customFilter[::-1])

    def startStream(self, updatedFil, updatesFlag):
        self.filCallback = self.buildCallback(updatedFil, updatesFlag)
        streamFormat = self.p.get_format_from_width(self.width)
        self.stream = self.p.open(  format = streamFormat,
                                    channels = self.channels,
                                    rate = self.rate,
                                    input = True,
                                    output = True,
                                    stream_callback = self.filCallback)

        self.stream.start_stream()
        self.keepAliveStream()

    def buildCallback(self, updatedFil, updatesFlag):
        return (lambda  inData, 
                        frameCount, 
                        timeInfo, 
                        status, 
                        fil = updatedFil, 
                        ua = updatesFlag : 
                self.filterCallback(inData, frameCount, timeInfo, status, fil, ua))

    def filterCallback(self, inData, frameCount, timeInfo, status, fil, updatesFlag):
        self.updateFilter(updatesFlag, fil)
        signalChunck = np.frombuffer(inData, dtype=np.int16)
        filteredChunck = self.filterChunck(signalChunck, frameCount)
        pyaudioStreamStatus = self.setPyAudioStreamStatus()
        return (filteredChunck, pyaudioStreamStatus)

    def updateFilter(self, updatesFlag, fil):
        if (updatesFlag.value):
            updatesFlag.value = False
            update = fil.get()
            self.fil = update.fil
            if (update.setsChanged):
                self.rate = update.rate
                self.restartFlag = True
            if (len(self.fil) != self.M):
                self.M = len(self.fil)
                self.circularArray = np.zeros(self.M)
                self.K = 0 #circularArray index

    def setPyAudioStreamStatus(self):
        if (self.restartFlag):
            return pyaudio.paComplete
        else:
            return pyaudio.paContinue

    def filterChunck(self, signalChunck, frameCount):
        ran = range(frameCount)
        K = self.K
        M = self.M
        A = np.zeros([frameCount, self.M], dtype = float)
        for n in ran:
            self.circularArray[K] = signalChunck[n]
            A[n, M-K:] = self.circularArray[:K]
            A[n, :M-K] = self.circularArray[K:M]
            K += 1
            if (K == M):
                K = 0
        self.K = K
        return A.dot(self.fil).astype(np.int16).tostring()

    def restartStream(self):
        self.stream.stop_stream()
        self.stream.close()
        streamFormat = self.p.get_format_from_width(self.width)
        self.stream = self.p.open(  format = streamFormat,
                                    channels = self.channels,
                                    rate = self.rate,
                                    input = True,
                                    output = True,
                                    stream_callback = self.filCallback)
        self.stream.start_stream()

    def keepAliveStream(self):
        while (self.stream.is_active() and self.stopFiltering.value == False):
            if (self.restartFlag):
                self.restartStream()
                self.restartFlag = False
            time.sleep(0.1)
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







