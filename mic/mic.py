from timeit import default_timer as timer
import pyaudio
import time
import numpy as np
import filters as fil
from filters import settings
from filters import filters

# this class creates a mic filter, 
# consisting of an audio I/O interface (PyAudio), 
# a filterUpdater and the filter itself.

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
    filterMode = 0

    # initializes mic filter using arguments. Creates an initial filter
    # creates circular array to receive real time data for better performance.
    # Filter is applied to data in the circular array.
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

    # Gets current sampling rate
    def getRate(self):
        return self.rate

    # Gets current filter's window
    def getFilterWindow(self):
        return self.fil.getWindow()

    # Loads new filter directly from array without processing
    def newFilter(self, customFilter):
        self.fil = np.array(customFilter[::-1])

    # Begins I/O audio stream from default windows devices and filters it.
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

    # Returns a callback used for stream filtering
    def buildCallback(self, updatedFil, updatesFlag):
        return (lambda  inData, 
                        frameCount, 
                        timeInfo, 
                        status, 
                        fil = updatedFil, 
                        ua = updatesFlag : 
                self.filterCallback(inData, frameCount, timeInfo, status, fil, ua))

    # Callback used for streaming. Gets a raw input and outputs the filtered audio
    def filterCallback(self, inData, frameCount, timeInfo, status, fil, updatesFlag):
        self.updateFilter(updatesFlag, fil)
        signalChunck = np.frombuffer(inData, dtype=np.int16)
        filteredChunck = self.filterChunck(signalChunck, frameCount)
        pyaudioStreamStatus = self.setPyAudioStreamStatus()
        return (filteredChunck, pyaudioStreamStatus)

    # Gets updates from the filter-updater: data from handles 
    # and GUI info (e.g: sampling rate).
    # 'fil' is a blocking queue (from Python's Multiprocessing's module),
    # with the updated filter, rate and mode.
    def updateFilter(self, updatesFlag, fil):
        if (updatesFlag.value):
            updatesFlag.value = False
            update = fil.get()
            self.fil = update.fil
            if (update.setsChanged):
                self.rate = update.rate
                self.restartFlag = True
                self.filterMode = update.mode
            if (len(self.fil) != self.M):
                self.M = len(self.fil)
                self.circularArray = np.zeros(self.M)
                self.K = 0 #circularArray index

    # Restarts stream if necessary (e.g: sampling rate changed)
    def setPyAudioStreamStatus(self):
        if (self.restartFlag):
            return pyaudio.paComplete
        else:
            return pyaudio.paContinue

    # Applies filter to current signal chunck.
    # Preprocessing is made to adapt the chunck (e.g: if
    # devil mode is selected, input samples must be redistributed).
    # Formatting (e.g: astype(np.int16)) is necessary for PyAudio's compatibility
    def filterChunck(self, signalChunck, frameCount):
        ran = range(frameCount)
        K = self.K
        M = self.M
        A = np.zeros([frameCount, self.M], dtype = float)

        if (self.filterMode == 0):
            sig = signalChunck

        elif (self.filterMode == 2):
            sig = np.zeros(len(signalChunck))
            n = 2
            for i in range(n):
                sig[i::n] = signalChunck[:int(frameCount/n):]

        for n in ran:
            self.circularArray[K] = sig[n]
            A[n, M-K:] = self.circularArray[:K]
            A[n, :M-K] = self.circularArray[K:M]
            K += 1
            if (K == M):
                K = 0
        self.K = K
        return A.dot(self.fil).astype(np.int16).tostring()

    # Restarts stream if specific parameters have changed.
    # e.g: sampling rate changed.
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

    # Keeps stream and process running and detects 
    # restart or stop flags (from other processes)
    def keepAliveStream(self):
        while (self.stream.is_active() and self.stopFiltering.value == False):
            if (self.restartFlag):
                self.restartStream()
                self.restartFlag = False
            time.sleep(0.1)
        self.stopStream()

    # Properly stops stream
    def stopStream(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    # Gets info from all available devices in Windows
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







