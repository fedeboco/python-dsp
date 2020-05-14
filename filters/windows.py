import numpy as np

class Window:
    name = "rectangular"
    values = []
    M = 0
    delta = 0
    Ap = 0
    As = 0

def rectangular(N, size = 0):
    w1 = np.ones(N + 1)
    if (size > N):
        w2 = np.zeros(size - N)
        return np.array(np.concatenate((w1, w2)))
    elif (size != 0):
        print("Invalid size.")
    else:
        return w1

def bartlett(N, size = 0):
    w1 = []
    w2 = []
    isEven = N % 2
    for i in range(0, N, 2):
        w1.append(i / N)
        w2.append((1 - (i + 1 * isEven) / N))
    if (size > N):
        w3 = np.zeros(size - N)
        return np.array(np.concatenate((w1, w2, w3)))
    elif (size != 0 and N != size):
        print("Invalid size.")
    else:
        return np.array(np.concatenate((w1, w2)))

def hann(N, size = 0):
    pi = 3.14159265358979323846
    w = []
    for i in range(0, N):
        w.append(0.5 * (1 - np.cos(2 * pi * i / N)))
    return w

def hamming(N, size = 0):
    pi = 3.14159265358979323846
    w = []
    for i in range(0, N):
        w.append(0.54 - 0.46 * np.cos(2 * pi * i / N))
    return w

def blackman(N, size = 0):
    pi = 3.14159265358979323846
    w = []
    for i in range(0, N+1):
        w.append(0.42 - 0.5 * np.cos(2 * pi * i / N) + 0.08 * np.cos(4 * pi * i / N))
    return w
