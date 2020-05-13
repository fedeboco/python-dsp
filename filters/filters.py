import windows as win
import numpy as np

class Filter:
    values = {}
    def loadValues(self, wVector, deltaVector):
        auxList = []
        auxValues = {}

        if (len(wVector) != len(deltaVector)):
            print("w vector length differs from delta vector length")
            return
        
        # creates unsorted dictionary (w, delta)
        for i in range(0, len(wVector)):
            auxValues[wVector[i]] = deltaVector[i]

        # creates sorted index for dictionary keys
        auxList = sorted(auxValues)     

        # stores dictionary sorted (w, delta)
        for i in range(0,len(auxList)):
           self.values[auxList[i]] = auxValues[auxList[i]]

    def __init__(self, wVector, deltaVector):
        self.loadValues(wVector, deltaVector)

    def printValues(self):
        print(self.values)

# wVector sorted in increasing order
def findLimitingW(wVector):
    W = np.inf
    for i in range(0, len(wVector), 2):
        if (wVector[i + 1] - wVector[i] < W):
            W = wVector[i + 1] - wVector[i]
    print(W)

def findLimitingValues(wVector, deltaVector):
    print("do something")

def chooseWindow(w1, w2, delta1, delta2 = 0):
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
            desiredWindow.M = int(setM(windowType, w1, w2))
            desiredWindow.wc = (w1 + w2) / 2
            return desiredWindow

    print("Couldn't choose a proper window in chooseWindow()")
    return []

def createWindow(w1, w2, delta1, delta2 = 0, size = 0):
    window = chooseWindow(w1, w2, delta1, delta2)
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

def minDelta(delta1, delta2):
    if (delta2 == 0 or delta1 < delta2):
        return delta1
    else:
        return delta2

def isGoodWindow(deltaWindow, deltaDesired):
    return deltaWindow < deltaDesired

def setM(window, w1, w2):
    w = abs(w1 - w2)
    pi = 3.14159265358979323846
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
    return M