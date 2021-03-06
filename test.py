# [deprecated]
# this file serves filter waveform and pyaudio testing purposes
# without processes

from filters import windows
from filters import graphs
from filters import filters
from mic import mic as mic
import numpy as np
import multiprocessing

## filter
wVec = [0, 0.04, 0.5, 0.6] # w/pi
deltaVec = [0.01, 0.02, 0.01, 0.02] # len(W) = len(delta)
ampVec = [0, 1, 1] # len(A) = len(W) / 2 + 1. Must be ordered
filter = filters.Filter(wVec, deltaVec, ampVec)
graphs.plot(filter.getWindow(), "Window")
MB = filter.filterMB()
f = np.fft.fft(MB)
graphs.plotFilterResponse(abs(f), "filter")

## pyaudio
speech = mic.MicFilter(filter = MB)
speech.devicesInfo()
speech.startStream()

# closing all plots when finished
graphs.closeAll()

