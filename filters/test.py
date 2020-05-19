import windows
import graphs
import filters
import numpy as np
import pyaudio
import time

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
wVec = [0, 0.1, 0.5, 0.6] # w/pi
deltaVec = [0.01, 0.02, 0.01, 0.02] # len(W) = len(delta)
ampVec = [1, 1, 0] # len(A) = len(W) / 2 + 1. Must be ordered
filter = filters.Filter(wVec, deltaVec, ampVec)
graphs.plot(filter.getWindow(), "Window")
MB = filter.filterMB()
f = np.fft.fft(MB)
mySine = np.sin(np.linspace(0, 20 * 2*pi, len(MB)))
ran = [np.random.rand() for i in range(0, len(MB)) ]
y = np.convolve(ran, np.array(MB))
graphs.plot(y, "sine filtered")
graphs.plot(ran, "input")
graphs.plot(MB, "filter")
graphs.plotFilterResponse(abs(f), "filter")

## pyaudio
# pip install PyAudio‑0.2.11‑cp38‑cp38‑win_amd64.whl
# https://people.csail.mit.edu/hubert/pyaudio/#wire-example

WIDTH = 2
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()
queue = list(np.zeros(len(MB)))
fil = np.array(MB[::-1])
L = 1024

def callback(in_data, frame_count, time_info, status):
    amplitude = np.frombuffer(in_data, dtype=np.int16)
    out_data = ()
    for n in range(0, L):
        queue.append(amplitude[n])
        queue.pop(0)
        lastValues = queue[- len(MB):]
        filteredSample = filters.filterSignal(lastValues, fil)
        out_data = np.append(out_data, int(filteredSample))
    return (out_data.astype(np.int16).tostring(), pyaudio.paContinue)

stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                stream_callback=callback)

stream.start_stream()

while stream.is_active():
    time.sleep(0.1)

stream.stop_stream()
stream.close()

p.terminate()

# closing all plots when finished
graphs.closeAll()