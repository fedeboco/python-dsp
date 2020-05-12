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

## different plots
graphs.plot(rect1, "Rectangle [n]")
graphs.plot(bart1, "Bartlett [n]")
graphs.plot(hann1, "Hann [n]")
graphs.plot(hamm1, "Hamming [n]")
graphs.plot(blck1, "Blackman [n]")

## all plots
windowsArray = np.array([rect1, bart1, blck1, hamm1, hann1])
windowsLegends = np.array(["Rectangular, Bartlett, Blackman, Hamming, Hann"])
graphs.multiPlot(windowsArray, 3, 2)

## filter
pi =3.14159
window = filters.createWindow(0.4 * pi, 0.31 * pi, 0.012, 0.03)
graphs.plot(window.values, "WinFilter [n]")

## closing all plots when finished
graphs.closeAll()