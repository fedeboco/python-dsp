from filters import windows
from filters import graphs
from filters import filters
from mic import mic as mic
import numpy as np
import multiprocessing as mp
import time
from filters import settings
from mic import gui
from mic import filupdater as updater

def plotMyFilter(filter, rate, exitProgram):
    f = np.fft.fft(filter)
    graphs.plotFilterResponse(abs(f), rate, "Multiband Filter")
    graphs.closeAll(exitProgram)

def filterMyMic(speech, updatedFil, updatesAvailable):
    speech.devicesInfo()
    speech.startStream(updatedFil, updatesAvailable)    

def testSettings():
    d = 0.08
    rate = 22050
    k = 1e+3
    f =  [  0, 31.5, 63, 125, 250, 500, 1*k, 2*k, 3*k, 4*k,
            5*k, 6*k, 7*k, 8*k, 9*k, 10*k, 12*k, 13*k    ] # Hz
    delta = [d for n in range(len(f))]
    A = [1 for n in range(int(len(f) / 2) + 1)]
    return settings.filterSettings(f, delta, A, rate)

def GUI(exitProgram, queue):
    gui.runUserGUI(exitProgram, queue)

def updateFilter(exitProgram, queue, filSets, updatedFil, updatesAvailable):
    filUpdater = updater.filterUpdater(queue, filterSettings = filSets)
    filUpdater.update(updatedFil, updatesAvailable)

if __name__ == '__main__':
    exitProgram = mp.Value('b', False)
    queue = mp.Queue(maxsize=int(1))
    updatedFil = mp.Queue(maxsize=int(1))
    updatesAvailable = mp.Value('b', False)
    
    speech = mic.MicFilter( filterSettings = testSettings(), 
                            stopFlag = exitProgram )
    processes = []
    processes.append(mp.Process(target=GUI, args=(  exitProgram, queue, )))
    processes.append(mp.Process(target=filterMyMic, args=(  speech, 
                                                            updatedFil, 
                                                            updatesAvailable, )))
    processes.append(mp.Process(target=updateFilter, args=( exitProgram, 
                                                            queue, 
                                                            testSettings(), 
                                                            updatedFil, 
                                                            updatesAvailable, )))

    for process in processes:
        process.start()

    time.sleep(1)

    while(exitProgram.value == False):
        time.sleep(0.1)

    for process in processes:
        process.join()