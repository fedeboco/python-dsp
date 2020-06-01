from multiprocessing import Queue, Value, Manager
from filters.settings import guiSettings
from filters import filters
from filters.filters import toDiscreteFrequency
import numpy as np

class FilterUpdate():
    rate = 0
    fil = []
    setsChanged = False
    mode = 0

    def load(self, *args, **kwargs):
        if 'rate' in kwargs:
            self.rate = kwargs['rate']
        if 'filter' in kwargs:
            self.fil = kwargs['filter']
        if 'mode' in kwargs:
            self.mode = kwargs['mode']

class filterUpdater():
    queue = Queue()
    guiSettings = guiSettings()
    lastGuiSettings = guiSettings
    fil = []
    updates = FilterUpdate()
    rate = 0
    
    def __init__(self, queue, *args, **kwargs):
        self.queue = queue
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
            self.wVec = self.filterSettings.frequencies
            self.deltaVec = self.filterSettings.deltas
            self.ampVec = self.filterSettings.amplitudes
            self.rate = self.filterSettings.rate
            self.filter = filters.Filter(   self.wVec, 
                                            self.deltaVec, 
                                            self.ampVec )
            self.fil = self.filter.build()

    def getQueue(self):
        return self.queue

    def update(self, updatesQueue, updatesAvailable):
        while ( True ):
            self.guiSettings = self.queue.get()
            if ( self.guiSettings == None ):
                break
            self.guiSettings.printSettings()
            self.sendUpdate(updatesQueue, updatesAvailable)
            self.lastGuiSettings = self.guiSettings

    def updateAmplitudes(self, A, band):
        A = A / 99.0 * 2.0
        self.fil = self.filter.modifyBandAmplitude(A, band)

    def sendUpdate(self, updatesQueue, updatesAvailable):
        if (self.guiSettings.settingsChanged(self.lastGuiSettings)):
            self.guiResolutionToFilter()
            self.updates.load(rate = self.guiRateToFilterRate())
            self.buildFilter()
            self.updates.setsChanged = True
        else:
            self.updates.setsChanged = False
            if (self.guiSettings.filterSelected == 0 or self.guiSettings.filterSelected == 1):
                self.updateAmplitudes(self.guiSettings.handleValue, self.guiSettings.handleSelected)
        self.updates.load(filter = self.fil)

        updatesQueue.put(self.updates)
        updatesAvailable.value = True

    def buildFilter(self):
        if (self.guiSettings.filterSelected == 0):
            self.filter = filters.Filter(   self.wVec, 
                                            self.deltaVec, 
                                            self.filter.A )
            self.fil = self.filter.build()
        elif (self.guiSettings.filterSelected == 2):
            self.fil = [1]
        self.updates.load(mode = self.guiSettings.filterSelected)


    def translateGuiToFilter(self):
        self.rate = self.guiSettings.rate

    def guiRateToFilterRate(self):
        rates = [48000, 44100, 32000, 22050, 11025, 8000]
        return rates[self.guiSettings.rateSelected]

    def guiResolutionToFilter(self):
        transitionWidth = [10, 15, 25, 30, 44]
        deltas = [0.08, 0.1, 0.12, 0.2, 0.5]
        t = transitionWidth[self.guiSettings.resolutionSelected]
        d = deltas[self.guiSettings.resolutionSelected]
        startingFreqs = [30, 75, 150, 400, 750, 1500, 3000, 6000, 1200]
        f = []
        for freq in startingFreqs:
            f.append(freq)
            f.append(freq + t)
        self.wVec = toDiscreteFrequency(f, self.rate)
        self.deltaVec = [d for n in range(len(f))]
