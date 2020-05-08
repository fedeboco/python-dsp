import numpy as np

def rectangular(stop, start = 0, size = 0):
    w1 = np.zeros(start)
    w2 = np.ones(stop - start + 1)
    if (size > stop):
        w3 = np.zeros(size - stop)
    elif (size != 0):
        print("Invalid size.")
    return np.array(np.concatenate((w1, w2, w3)))

def bartlett(stop, start = 0, size = 0):
    N = stop - start
    w1 = np.zeros(start)
    w2 = []
    w3 = []
    isEven = N % 2
    for i in range(0, N, 2):
        w2.append(i / N)
        w3.append((1 - (i + 1 * isEven) / N))
    if (size > stop):
        w4 = np.zeros(size - stop)
        return np.array(np.concatenate((w1, w2, w3, w4)))
    elif (size != 0 and stop != size):
        print("Invalid size.")
    else:
        return np.array(np.concatenate((w1, w2, w3)))

