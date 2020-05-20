from filters import windows
from filters import graphs
from filters import filters
from mic import mic as mic
import numpy as np
import multiprocessing as mp
import time

def plotCustomFilter(MB, filter, exitProgram):
    f = np.fft.fft(MB)
    graphs.plot(filter.getWindow(), "Window")
    graphs.plotFilterResponse(abs(f), "filter")
    graphs.closeAll(exitProgram)

def filterMyMic(speech):
    speech.devicesInfo()
    speech.startStream()    

if __name__ == '__main__':
    exitProgram = mp.Value('b', False) # might need lock? is atomic?
    wVec = [0, 0.1, 0.5, 0.6] # w/pi
    deltaVec = [0.1, 0.2, 0.1, 0.2] # len(W) = len(delta)
    ampVec = [0, 1, 1] # len(A) = len(W) / 2 + 1. Must be ordered
    filter = filters.Filter(wVec, deltaVec, ampVec)
    MB = filter.filterMB()
    speech = mic.MicFilter(filter = MB, stopFlag = exitProgram)
    processes = []
    processes.append(mp.Process(target=filterMyMic, args=(speech, )))
    processes.append(mp.Process(target=plotCustomFilter, args=(MB, filter, exitProgram)))

    for process in processes:
        process.start()

    time.sleep(1)

    while(exitProgram.value == False):
        if (input("quit? (y/n): ") == 'y'):
            exitProgram.value = True 
        time.sleep(0.1)

    for process in processes:
        process.join()