from multiprocessing import Queue, Value, Manager
from filters.settings import guiSettings
from filters import filters
import numpy as np

class filterUpdater():
    queue = Queue()
    guiSettings = guiSettings()
    fil = []
    
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
            wVec = self.filterSettings.frequencies
            deltaVec = self.filterSettings.deltas
            ampVec = self.filterSettings.amplitudes
            self.rate = self.filterSettings.rate
            self.filter = filters.Filter(wVec, deltaVec, ampVec)
            self.fil = self.filter.build()

    def getQueue(self):
        return self.queue

    def update(self, updatedFil, updatesAvailable):
        while ( True ):
            self.guiSettings = self.queue.get()
            if ( self.guiSettings == None ):
                break
            self.guiSettings.printSettings()
            self.newFilter(self.guiSettings.handleValue, self.guiSettings.handleSelected)
            updatedFil.put(self.fil)
            updatesAvailable.value = True

    def newFilter(self, A, band):
        A = A / 99.0 * 2.0
        self.fil = self.filter.modifyBandAmplitude(A, band)