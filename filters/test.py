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
wVec = [0.11, 0.12, 0.3, 0.4, 0.5, 0.7, 0.8, 0.9] # w/pi
deltaVec = [0.003, 0.0024, 0.002, 0.003, 0.002, 0.003, 0.003, 0.003] # len(W) = len(delta)
ampVec = [1, 10, 5, 10, 5] # len(A) = len(W) / 2 + 1. Must be ordered
filter = filters.Filter(wVec, deltaVec, ampVec)
graphs.plot(filter.getWindow(), "WinFilter")

## LP
MB = filter.filterMB()
f = np.fft.fft(MB)
graphs.plotFilterResponse(abs(f), "filter")

## closing all plots when finished
graphs.closeAll()