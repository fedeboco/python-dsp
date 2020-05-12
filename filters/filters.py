import windows as win
import numpy as np

def chooseWindow(wp, ws, delta1, delta2 = 0):
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
            desiredWindow.M = int(setM(windowType, wp, ws))
            desiredWindow.wc = (wp + ws) / 2
            return desiredWindow

    print("Couldn't choose a proper window in chooseWindow()")
    return []

def createWindow(wp, ws, delta1, delta2 = 0, size = 0):
    window = chooseWindow(wp, ws, delta1, delta2)
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

def setM(window, wp, ws):
    w = abs(wp - ws)
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