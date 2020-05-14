import windows
import graphs
import filters
import numpy as np

## different windows
rect1 = windows.rectangular(5, 10)
bart1 = windows.bartlett(12, 24) 
hann1 = windows.hann(120)
hamm1 = windows.hamming(80)
blck1 = windows.blackman(80)
windowsArray = np.array([rect1, bart1, blck1, hamm1, hann1])
windowsLegends = np.array(["Rectangular, Bartlett, Blackman, Hamming, Hann"])
graphs.multiPlot(windowsArray, 3, 2)

## filter
pi = 3.14159
wVec = [0.31, 0.4, 0.6, 0.8] # w/pi
deltaVec = [0.012, 0.03, 0.03, 0.01] # len(W) = len(delta)
ampVec = [0, 2, 4/5] # len(A) = len(W) / 2 + 1. Must be ordered
filter = filters.Filter(wVec, deltaVec, ampVec)
graphs.plot(filter.getWindow(), "WinFilter")

## closing all plots when finished
graphs.closeAll()