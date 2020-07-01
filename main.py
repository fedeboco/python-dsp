# [important changes pending]
# this file serves for testing purposes
# functions will be moved to another module / class

from filters import windows, graphs, filters, settings

import numpy as np
import multiprocessing as mp
import time

from mic import mic as mic
from mic import filupdater as updater
from mic import gui

# plots graph of filter response
def plotMyFilter(filter, rate, exitProgram):
    f = np.fft.fft(filter)
    graphs.plotFilterResponse(abs(f), rate, "Multiband Filter")
    graphs.closeAll(exitProgram)

# starts pyaudio and mic
def filterMyMic(speech, updatesQueue, updatesFlag):
    speech.devicesInfo()
    speech.startStream(updatesQueue, updatesFlag)    

# creates filter
def testSettings():
    d = 0.08
    rate = 22050
    f =  [  30, 55, 75, 100, 150, 175, 400, 425, 750, 775,
            1500, 1525, 3000, 3025, 6000, 6025, 1200, 1225    ] # Hz
    delta = [d for n in range(len(f))]
    A = [1 for n in range(int(len(f) / 2) + 1)]
    return settings.filterSettings(f, delta, A, rate)

def GUI(exitProgram, queue):
    gui.runUserGUI(exitProgram, queue)

# checks for updates sent from gui
def updateFilter(exitProgram, queue, filSets, updatesQueue, updatesFlag):
    filUpdater = updater.filterUpdater(queue, filterSettings = filSets)
    filUpdater.update(updatesQueue, updatesFlag)

# launchs processes
def runMicFilterWithGUI():
    exitProgram = mp.Value('b', False)
    queue = mp.Queue(maxsize=int(1))
    updatesQueue = mp.Queue(maxsize=int(1))
    updatesFlag = mp.Value('b', False)
    
    speech = mic.MicFilter( filterSettings = testSettings(), 
                            stopFlag = exitProgram )
    processes = []
    processes.append(mp.Process(target=GUI, args=(  exitProgram, queue, )))
    processes.append(mp.Process(target=filterMyMic, args=(  speech, 
                                                            updatesQueue, 
                                                            updatesFlag, )))
    processes.append(mp.Process(target=updateFilter, args=( exitProgram, 
                                                            queue, 
                                                            testSettings(), 
                                                            updatesQueue, 
                                                            updatesFlag, )))

    for process in processes:
        process.start()

    time.sleep(1)

    while(exitProgram.value == False):
        time.sleep(0.1)

    for process in processes:
        process.join()

if __name__ == '__main__':
    runMicFilterWithGUI()