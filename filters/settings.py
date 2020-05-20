from filters.filters import toDiscreteFrequency

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