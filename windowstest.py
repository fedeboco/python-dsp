from filters import windows
from filters import graphs
from filters import filters
from mic import mic as mic
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