from filters.filters import toDiscreteFrequency
from multiprocessing import Lock

class filterSettings:
    frequencies = []
    deltas = []
    amplitudes = []
    rate = 22050 # sampling rate

    def update(self, f, d, a, rate):

        if( len(f) != len(d) ):
            print("frequencies and delta vectors should have same length.")

        if ( len(a)!= len(f) / 2 + 1 ):
            print("amplitudes vector should have 'len(freqs) / 2 + 1' length.")

        self.frequencies = toDiscreteFrequency(f, rate)
        self.deltas = d
        self.amplitudes = a
        self.rate = rate

    def __init__(self, f, d, a, rate):
        self.update(f, d, a, rate)

class guiSettings:
    filterSelected = 0
    resolutionSelected = 0
    rateSelected = 0
    handleSelected = 0
    handleValue = 0

    def __init__(self, *args, **kwargs):
        if 'initValues' in kwargs:
            init = kwargs['initValues']
            self.filterSelected = init[0]
            self.resolutionSelected = init[1]
            self.rateSelected = init[2]
            self.handleSelected = init[3]
            self.handleValue = init[4]      

    def printSettings(self):
        print("filType:", self.filterSelected, end=", ")
        print("res:", self.resolutionSelected, end=", ")
        print("rate:", self.rateSelected, end=", ")
        print("handle: [", self.handleSelected, end=", ")      
        print(self.handleValue, "]")

    def settingsChanged(self, oldSettings):
        a = self.filterSelected != oldSettings.filterSelected
        b = self.resolutionSelected != oldSettings.resolutionSelected
        c = self.rateSelected != oldSettings.rateSelected
        return a or b or c
