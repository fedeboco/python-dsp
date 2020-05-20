from filters import windows
from filters import graphs
from filters import filters
from mic import mic as mic
import numpy as np
import multiprocessing as mp
import time
from filters import settings

def plotMyFilter(filter, rate, exitProgram):
    f = np.fft.fft(filter)
    graphs.plotFilterResponse(abs(f), rate, "Multiband Filter")
    graphs.closeAll(exitProgram)

def filterMyMic(speech):
    speech.devicesInfo()
    speech.startStream()    

def testSettings():
    d = 0.08
    rate = 22050
    f =  [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000] # Hz
    delta = [d for n in range(len(f))]
    A = [0, 1, 0.8, 0, 1, 0.3]
    return settings.filterSettings(f, delta, A, rate)

if __name__ == '__main__':
    exitProgram = mp.Value('b', False)

    speech = mic.MicFilter( filterSettings = testSettings(), 
                            stopFlag = exitProgram )
    processes = []
    processes.append(mp.Process(target=filterMyMic, args=(speech, )))
    processes.append(mp.Process(target=plotMyFilter, args=(speech.getFilter(), speech.getRate(), exitProgram)))

    for process in processes:
        process.start()

    time.sleep(1)

    while(exitProgram.value == False):
        if (input("quit? (y/n): ") == 'y'):
            exitProgram.value = True 
        time.sleep(0.1)

    for process in processes:
        process.join()