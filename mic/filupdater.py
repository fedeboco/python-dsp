from multiprocessing import Queue, Value, Manager
from filters.settings import guiSettings
from filters import filters
import numpy as np

class FilterUpdate():
    rate = 0
    fil = []
    setsChanged = False

    def load(self, *args, **kwargs):
        if 'rate' in kwargs:
            self.rate = kwargs['rate']
        if 'filter' in kwargs:
            self.fil = kwargs['filter']

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
            self.updates.load(rate = self.guiRateToFilterRate())
            self.filter = filters.Filter(   self.wVec, 
                                            self.deltaVec, 
                                            self.ampVec )
            self.fil = self.filter.build()
            self.updates.setsChanged = True
        else :
            self.updateAmplitudes(self.guiSettings.handleValue, self.guiSettings.handleSelected)
            self.updates.setsChanged = False
        self.updates.load(filter = self.fil)

        updatesQueue.put(self.updates)
        updatesAvailable.value = True

    def translateGuiToFilter(self):
        self.rate = self.guiSettings.rate

    def guiRateToFilterRate(self):
        rates = [48000, 44100, 32000, 22050, 11025, 8000]
        return rates[self.guiSettings.rateSelected]

