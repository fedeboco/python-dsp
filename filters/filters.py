from filters import windows as win
from filters import filmath as fmath
import numpy as np

# stores IDEAL filter properties, stores
# window and computes it's optimal parameters
# for generating the REAL filter in other
# modules

class Filter:
    values = {}
    W = 0
    delta = 0
    filterType = 0
    window = win.Window()
    A = []
    fil = []
    cutFreqs = []
    bandFilters = []
  
    # loads filter specifications from user interface
    def loadValues(self, wVector, deltaVector, ampVector):
        auxList = []
        auxValues = {}
        self.A = ampVector
        self.values = {}
        pi = fmath.pi

        if (len(wVector) != len(deltaVector) or
            len(ampVector) != len(deltaVector) / 2 + 1):
            print("Lengths error: len(W) = len(delta) = 2*len(A) - 2")
            return
        
        # creates unsorted dictionary (w, delta)
        for i in range(0, len(wVector)):
            auxValues[wVector[i] * pi] = deltaVector[i]

        # creates sorted index for dictionary keys
        auxList = sorted(auxValues)     

        # stores dictionary sorted (w, delta)
        for i in range(0,len(auxList)):
           self.values[auxList[i]] = auxValues[auxList[i]]

    # loads specs, computes optimal parameters and window
    def __init__(self, wVector, deltaVector, ampVector):
        self.loadValues(wVector, deltaVector, ampVector)
        self.findLimitingValues()
        self.computeWindow()
        self.printValues()

    # this filter uses 1 window. So it needs to find
    # it's restricting parameters of transition width W
    # and overshoot delta.
    def findLimitingValues(self):
        self.W = findLimitingW(self.values.keys())
        self.delta = findLimitingDelta(self.values.values(), self.A)

    # creates window of length M based on type, transition width W 
    # and overshoot delta
    def computeWindow(self):
        self.window = createWindow(self.filterType, self.W, self.delta)

    # prints (w, delta) dictionary
    def printValues(self):
        print(self.values)

    # returns window
    def getWindow(self):
        return self.window.values

    # returns ideal low pass filter
    # wc: cutoff angular frequency
    def filterLP(self, wc):
        return idealLP(wc, self.window.M)
    
    # returns ideal all pass filter
    def filterAP(self):
        return idealAP(self.window.M)

    # returns ideal high pass filter
    # wc: cutoff angular frequency
    def filterHP(self, wc):
        return idealHP(wc, self.window.M)
    
    # wl: low cutoff angular frequency
    # wh: high cutoff angular frequency
    def filterBP(self, wl, wh):
        return idealBP(wl, wh, self.window.M)

    # builds an ideal multiband filter based on stored specs
    # and computed parameters
    def build(self):
        self.cutFreqs = cutoffFrequencies(list(self.values.keys()))
        amplitude = self.A
        M = self.window.M
        self.bandFilters = []
        win = self.window.values
      
        firstBand = idealLP(self.cutFreqs[0], M, amplitude[0]) * win
        h = firstBand
        self.bandFilters.append(firstBand)

        for i in range(len(self.cutFreqs) - 1):
            band = idealBP(self.cutFreqs[i], self.cutFreqs[i + 1], M, amplitude[i + 1]) * win
            h = h + band
            self.bandFilters.append(band)

        lastBand = idealHP(self.cutFreqs[-1], M, amplitude[-1]) * win
        h = h + lastBand
        self.bandFilters.append(lastBand)

        self.fil = h
        return h

    # returns filter bands of the multiband filter as a matrix
    def getFilterBands(self):
        return self.bandFilters

    # modifies amplitude of ideal filter band with index bandIndex
    def modifyBandAmplitude(self, amplitude, bandIndex):
        i = bandIndex
        band = self.bandFilters[i]
        self.A[i] = amplitude
        freqs = self.cutFreqs
        M = self.window.M
        win = self.window.values

        self.fil = self.fil - band

        if (bandIndex == 0):
            h = idealLP(freqs[0], M, amplitude) * win
        elif (bandIndex == len(self.bandFilters) - 1):
            h = idealHP(freqs[-1], M, amplitude) * win
        else:
            h = idealBP(freqs[i - 1], freqs[i], M, amplitude) * win
        
        self.bandFilters[i] = h
        self.fil = self.fil + h
        return self.fil

# this function computes an ideal low pass filter with cutoff freq
# wc, length M and amplitude A
def idealLP(wc, M, A = 1):
    tau = M / 2.0
    pi = np.pi
    x = np.linspace(wc * (-tau) / pi, wc * (M - tau) / pi, M)
    h = np.sinc(x)
    h = np.multiply(h, A * wc / pi)
    return h

# this function computes an ideal all pass filter with length 
# M and amplitude A
def idealAP(M, A = 1):
    tau = M / 2.0
    x = np.linspace(-tau, M - tau, M)
    h = np.sinc(x)
    h = np.multiply(h, A)
    return h

# this function computes an ideal high pass filter with cutoff freq
# wc, length M and amplitude A
def idealHP(wc, M, A = 1):
    ap = idealAP(M, A)
    lp = idealLP(wc, M, A)
    return ap - lp

# this function computes an ideal band pass filter with cutoff freqs
# wl (low) and wh (high), length M and amplitude A
def idealBP(wl, wh, M, A = 1):
    lp1 = idealLP(wh, M, A)
    lp2 = idealLP(wl, M, A)
    return lp1 - lp2

# this function computes an ideal multiband filter with cutoff frequencies
# wVector, length M and amplitude A
def idealMB(wVector, amplitude, M, iBP):
    wVector = cutoffFrequencies(wVector)
    h = idealLP(wVector[0], M, amplitude[0])
    aux = idealHP(wVector[-1], M, amplitude[-1])
    h = h + aux
    iBP = []
    for i in range(len(wVector) - 1):
        iBP.append(idealBP(wVector[i], wVector[i + 1], M, amplitude[i + 1]))
        h =  h + iBP[-1]
    return h

# computes cutoff frequencies from transition start and transition end scalar frequencies
def cutoffFrequencies(wVector):
    return [ (wVector[i] + wVector[i + 1]) / 2.0 for i in range(0, len(wVector) - 1, 2)]

# wVector sorted in increasing order
def findLimitingW(wVector):
    wVector = list(wVector)
    W = np.inf

    for i in range(0, len(wVector), 2):
        if (wVector[i + 1] - wVector[i] < W):
            W = wVector[i + 1] - wVector[i]
    return W

#finds delta limitation based on amplitude difference
def findLimitingDelta(deltaVector, A):
    deltaVector = list(deltaVector)
    minDelta = np.inf
    j = -1

    for i in range(0, len(deltaVector)):
        if (i % 2 == 0):
            j = j + 1
        dA = A[j + 1] - A[j]
        if (dA != 0):
            auxDelta = deltaVector[i] / abs(dA)
            if (auxDelta < minDelta):
                minDelta = auxDelta

    return minDelta

# determine filter type
def filterType(fType = 0, aStart = -1, aEnd = -1):
    if (fType > 0 and fType < 5):
        return fType
    if (aStart == 0 and aEnd == 0):
        return 3
    elif (aStart == 0):
        return 4
    elif (aEnd == 0):
        return 2
    else:
        return 1

# determines window to use
# if one delta is provided, assumes minimal delta is
# already determined. Otherwise, in can receive 2 and
# determine it
def chooseWindow(fType, W, delta1, delta2 = 0):
    windows = {
        "dRect": 0.09,
        "dBartlett": 0.05,
        "dHann": 0.0063,
        "dHamming": 0.0022,
        "dBlackman": 0.00022
    }

    desiredWindow = win.Window()
    desiredWindow.delta = minDelta(delta1, delta2)

    for windowType, deltaWindow in windows.items():
        if (isGoodWindow(deltaWindow, desiredWindow.delta)):
            desiredWindow.name = windowType
            desiredWindow.M = int(setM(fType, windowType, W))
            return desiredWindow

    print("Couldn't choose a proper window in chooseWindow()")
    return []

# computes window waveform based on type, name, and length.
# size param provides a way to generate larger vectors for later products
def createWindow(fType, W, delta1, delta2 = 0, size = 0):
    window = chooseWindow(fType, W, delta1, delta2)
    if (window == []):
        return []

    print("M =", window.M,"| Window:",  window.name, "| delta =", window.delta)
    
    if (window.name == "dRect"):
        window.values = win.rectangular(window.M, size)
    if (window.name == "dBartlett"):
        window.values = win.bartlett(window.M, size)
    if (window.name == "dHann"):
        window.values = win.hann(window.M, size)
    if (window.name == "dHamming"):
        window.values = win.hamming(window.M, size)
    if (window.name == "dBlackman"):
        window.values = win.blackman(window.M, size)

    return window

# decides which delta is smaller between 2 values
def minDelta(delta1, delta2):
    if (delta2 == 0 or delta1 < delta2):
        return delta1
    else:
        return delta2

# determines if available window satisfies user 
# specifications
def isGoodWindow(deltaWindow, deltaDesired):
    return deltaWindow < deltaDesired

# determins window length based on type and name of win
def setM(filterType, window, w):
    pi = 3.14159265358979323846
    odd = True
    if (filterType == 1 or filterType == 3):
        odd = False
    if (window == "dRect"):
        M = np.ceil(4 * pi / w - 1)
    elif (window == "dBartlett"):
        M = np.ceil(8 * pi / w)
    elif (window == "dHann"):
        M = np.ceil(8 * pi / w)
    elif (window == "dHamming"):
        M = np.ceil(8 * pi / w)
    elif (window == "dBlackman"):
        M = np.ceil(12 * pi / w)
    M = setParity(M, odd)
    return M

# decides if window should have odd length or not
def setParity(M, odd):
    if (M % 2 == 0 and odd):
        return M + 1
    elif (M % 2 == 1 and not(odd)):
        return M + 1
    else:
        return M

# applies any filter 'fil' to signal 's'
def filterSignal(s, fil):
    s = np.array(s)
    y = np.dot(s, fil)
    return y

# returns discrete frequency vector normalized (Hz to rads/pi)
def toDiscreteFrequency(frequencies, fsampling):
    return [2 * f / fsampling for f in frequencies]